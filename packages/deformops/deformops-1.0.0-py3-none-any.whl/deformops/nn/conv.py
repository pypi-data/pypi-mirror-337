import math
import typing

import torch
import torch.nn
import torch.nn.init

import deformops.deform2d


class _ScaleLinear(torch.nn.Module):
    r"""
    Simple wrapper around a linear layer for the purpose of having weight and bias
    parameters that are not named "weight" and "bias" to prevent these parameters
    from being picked up by the optimizer for applying weight decay or other
    transformations.

    The output is passed through a sigmoid function to ensure that the scale is
    between 0 and 1.
    """

    def __init__(self, dims: int, group: int, **kwargs):
        super().__init__(**kwargs)

        self.scale_weight = torch.nn.Parameter(
            torch.zeros((group, dims), dtype=torch.float32)
        )
        self.scale_bias = torch.nn.Parameter(torch.zeros((group,), dtype=torch.float32))

    @typing.override
    def forward(self, query: torch.Tensor) -> torch.Tensor:
        return torch.nn.functional.linear(
            query,
            weight=self.scale_weight,
            bias=self.scale_bias,
        ).sigmoid()


class DeformConv2d(torch.nn.Module):
    r"""
    Deformable convolutional layer.
    """

    def __init__(
        self,
        dims,
        kernel_size: int = 3,
        *,
        stride: int = 1,
        padding: int | typing.Literal["same"] = "same",
        dilation: int = 1,
        groups: int = 4,
        offset_scale: float = 1.0,
        center_feature_scale: bool = False,
        remove_center: bool = False,
        project: type[torch.nn.Module] | None = torch.nn.Linear,
        softmax: bool = False,
        norm: torch.nn.Module | None = None,
        activation: torch.nn.Module | None = None,
        **kwargs,
    ):
        """
        Parameters
        ----------
        dims : int
            Number of input dims
        kernel_size : int
            Size of the convolving kernel
        stride : int
            Stride of the convolution
        padding : int
            Padding added to both sides of the input
        padding_mode : str
            Padding mode for the convolutions, currently only "zeros" is supported.
        dilation : int
            Spacing between kernel elements
        groups : int
            Number of blocked cotorch.nnections from input dims to output dims
        offset_scale : float
            Scale of the offset
        center_feature_scale : bool
            Whether to use center feature scale
        remove_center : bool
            Whether to remove the center of the kernel
        bias : bool
            Whether to use bias in the output projection
        project : torch.nn.Module
            Projection layer. Defaults to ``torch.nn.Linear``.
        softmax : bool
            Whether to use softmax in the deformable convolution, defaults to False.
        """
        super().__init__(**kwargs)
        if dims % groups != 0:
            msg = f"{dims=} must be divisible by {groups=}"
            raise ValueError(msg)
        if (dims_per_group := dims // groups) % 16 != 0:  # noqa: PLR2004
            msg = f"dims per group ({dims_per_group}) must be divisible by 16"
            raise ValueError(msg)

        self.offset_scale = offset_scale
        self.dims = dims
        self.kernel_size = kernel_size
        self.stride = stride
        self.dilation = dilation
        if padding == "same":
            padding = kernel_size // 2
        self.padding = padding
        self.groups = groups
        self.group_dims = dims // groups
        self.offset_scale = offset_scale
        self.center_feature_scale = center_feature_scale
        self.remove_center = remove_center
        self.softmax = softmax
        self.offset_depthwise = torch.nn.Conv2d(
            dims,
            dims,
            self.kernel_size,
            stride=1,
            padding=self.padding,
            padding_mode="zeros",
            groups=dims,
        )
        kernel_numel = self.groups * (
            self.kernel_size * self.kernel_size - int(self.remove_center)
        )
        self.offset_pointwise = torch.nn.Linear(
            dims, int(math.ceil((kernel_numel * 3) / 8) * 8)
        )

        if project is not None:
            self.proj_input = project(dims, dims)
            self.proj_output = project(dims, dims)
        else:
            self.register_module("proj_input", None)
            self.register_module("proj_output", None)

        self.reset_parameters()

        if center_feature_scale:
            self.center_scale = _ScaleLinear(dims, groups)
        else:
            self.register_module("center_scale", None)

        if norm is None:
            self.register_module("norm", None)
        else:
            self.norm = norm

        if activation is None:
            self.register_module("activation", None)
        else:
            self.activation = activation

    def reset_parameters(self):
        # Initialize the offset layers
        for mod in [self.offset_depthwise, self.offset_pointwise]:
            if mod is None:
                continue
            if mod.bias is not None:
                torch.nn.init.zeros_(mod.bias.data)
            torch.nn.init.zeros_(mod.weight.data)

        # Initialize the projection layers
        for mod in [self.proj_input, self.proj_output]:
            if mod is None:
                continue
            if hasattr(mod, "reset_parameters"):
                mod.reset_parameters()
            else:
                if mod.bias is not None:
                    torch.nn.init.zeros_(mod.bias.data)
                torch.nn.init.xavier_uniform_(mod.weight.data)

    def _forward_deform(
        self, out: torch.Tensor, offset_mask: torch.Tensor
    ) -> torch.Tensor:
        return deformops.deform2d.forward(
            out,
            offset_mask,
            self.kernel_size,
            self.kernel_size,
            self.stride,
            self.stride,
            self.padding,
            self.padding,
            self.dilation,
            self.dilation,
            self.groups,
            self.group_dims,
            self.offset_scale,
            256,
            self.remove_center,
            self.softmax,
        )

    @typing.override
    def forward(
        self, input: torch.Tensor, shape: torch.Size | None = None
    ) -> torch.Tensor:
        """
        Parameters
        ----------
        input : torch.Tensor[N, L, C]
            The input tensor, where N is the batch size, L is the sequence length.
        shape : tuple[H,W]
            Shape of the input tensor if input is in the form of torch.Tensor[N, L, C].
            Optional when the input is in the form of torch.Tensor[N, C, H, W].

        Returns
        -------
        torch.Tensor[N, L, C] or torch.Tensor[N, C, H, W]
            Result of the deformable convolution
        """

        ndim_input = input.ndim
        if ndim_input == 4:  # noqa: PLR2004
            assert shape is None
            shape = input.shape[-2:]
            input = input.flatten(2).permute(0, 2, 1).contiguous()

        N, L, C = input.shape
        assert shape is not None, "shape must be provided"
        H, W = shape

        out = input
        if self.proj_input is not None:
            out = self.proj_input(out)
        out = out.reshape(N, H, W, -1)

        if self.offset_depthwise is not None:
            offset_mask_input = self.offset_depthwise(
                input.view(N, H, W, C).permute(0, 3, 1, 2)
            )
            offset_mask_input = offset_mask_input.permute(0, 2, 3, 1).view(N, L, C)
        else:
            offset_mask_input = input
        offset_mask = self.offset_pointwise(offset_mask_input).reshape(N, H, W, -1)

        out_ante = out
        out = self._forward_deform(out, offset_mask)

        if self.center_scale is not None:
            center_feature_scale = self.center_scale(out)
            center_feature_scale = (
                center_feature_scale[..., None]
                .repeat(1, 1, 1, 1, self.dims // self.groups)
                .flatten(-2)
            )
            out = out * (1 - center_feature_scale) + out_ante * center_feature_scale
        out = out.view(N, L, -1)

        if self.proj_output is not None:
            out = self.proj_output(out)
        if ndim_input == 4:  # noqa: PLR2004
            out = out.permute(0, 2, 1).unflatten(2, shape).contiguous()
        if self.norm is not None:
            out = self.norm(out)
        if self.activation is not None:
            out = self.activation(out)

        return out

    if typing.TYPE_CHECKING:
        __call__ = forward
