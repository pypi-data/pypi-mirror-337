import enum as E
import typing

import torch
import torch.nn
import torch.nn.init

import deformops.deform2d_multiscale
import deformops.deform2d_multiscale_fused

from ._sanitize import CHECK_2POWER, CHECK_DIVISIBLE


class FusedMSDeformAttn2d(torch.nn.Module):
    r"""
    Multi-scale deformable attention layer, with fused softmax in the forward pass.
    """

    im2col_step: int

    def __init__(
        self,
        dim: int,
        dim_value: int | None = None,
        dim_output: int | None = None,
        *,
        num_heads: int,
        num_levels: int,
        num_points: int = 4,
        projection: type[torch.nn.Module] = torch.nn.Linear,
        **kwargs,
    ):
        r"""
        Parameters
        ----------
        dim
            Amount of hidden dimension.
        dim_value
            Amount of value dimension, projected to `dim`.
        dim_output
            Amount of output dimensions, projected from `dim`.
        levels
            Amount of feature levels.
        num_heads
            Amount of attention num_heads.
        points
            Amount of sampling points per attention head per feature level.
        """
        super().__init__(**kwargs)

        d_per_head = dim // num_heads

        CHECK_DIVISIBLE(dim, num_heads)
        CHECK_2POWER(d_per_head)

        if dim_value is None:
            dim_value = dim
        if dim_output is None:
            dim_output = dim

        self.im2col_step = 64

        self.dim = dim
        self.dim_value = dim_value
        self.dim_output = dim_output
        self.levels = num_levels
        self.num_heads = num_heads
        self.points = num_points

        self.proj_offset = torch.nn.Linear(dim, num_heads * num_levels * num_points * 2)
        self.proj_weights = torch.nn.Linear(dim, num_heads * num_levels * num_points)
        self.proj_value = projection(dim_value, dim)
        self.proj_output = projection(dim, dim_output)

        self.reset_parameters()

    def reset_parameters(self):
        torch.nn.init.constant_(self.proj_offset.weight.data, 0.0)
        thetas = torch.arange(self.num_heads, dtype=torch.float32) * (
            2.0 * torch.pi / self.num_heads
        )
        grid_init = torch.stack([thetas.cos(), thetas.sin()], -1)
        grid_init = (
            (grid_init / grid_init.abs().max(-1, keepdim=True)[0])
            .view(self.num_heads, 1, 1, 2)
            .repeat(1, self.levels, self.points, 1)
        )
        for i in range(self.points):
            grid_init[:, :, i, :] *= i + 1
        grid_init = grid_init.reshape(-1)
        with torch.no_grad():
            self.proj_offset.bias.data.copy_(grid_init)
        torch.nn.init.constant_(self.proj_weights.weight.data, 0.0)
        torch.nn.init.constant_(self.proj_weights.bias.data, 0.0)
        torch.nn.init.xavier_uniform_(self.proj_value.weight.data)
        torch.nn.init.constant_(self.proj_value.bias.data, 0.0)
        torch.nn.init.xavier_uniform_(self.proj_output.weight.data)
        torch.nn.init.constant_(self.proj_output.bias.data, 0.0)

    @typing.override
    def forward(
        self,
        q: torch.Tensor,
        p: torch.Tensor,
        v: torch.Tensor,
        shapes: torch.Tensor,
        level_index: torch.Tensor,
        padding_mask: torch.Tensor | None = None,
    ):
        """
        Parameters
        ----------
        q: torch.Tensor[N, Q, C]
            Query tensor
        p: torch.Tensor[N, Q, L, 2] | torch.Tensor[N, Q, L, 4]
            Reference points for each query point, in the format of
            (top-left, bottom-right) or (top, left, h, w)
        v: torch.Tensor[N, H*W, C]
            Flattened input tensor
        shapes: torch.Tensor[L, 2]
            Spatial shapes of each level
        level_index: torch.Tensor[L]
            Start index of each level in the flattened input tensor
        padding_mask: torch.Tensor[N, H*W]
            Padding mask for the input tensor

        Returns
        -------
        output : torch.Tensor[N, Q, C]
            The output tensor.
        """
        d_batch, d_q, _ = q.shape
        d_batch, d_in, _ = v.shape
        assert (shapes[:, 0] * shapes[:, 1]).sum() == d_in

        v = self.proj_value(v)
        if padding_mask is not None:
            v = v.masked_fill(padding_mask[..., None], float(0))
        v = v.view(d_batch, d_in, self.num_heads, self.dim // self.num_heads)
        attn = self.proj_weights(q).view(
            d_batch, d_q, self.num_heads, self.levels * self.points
        )
        loc_off = self.proj_offset(q).view(
            d_batch, d_q, self.num_heads, self.levels, self.points, 2
        )
        if p.shape[-1] == 2:  # noqa: PLR2004
            loc_norm = torch.stack([shapes[..., 1], shapes[..., 0]], -1)
            loc = (
                p[:, :, None, :, None, :]
                + loc_off / loc_norm[None, None, None, :, None, :]
            )
        elif p.shape[-1] == 4:  # noqa: PLR2004
            loc = (
                p[:, :, None, :, None, :2]
                + loc_off / self.points * p[:, :, None, :, None, 2:] * 0.5
            )
        else:
            msg = f"Last dim ({p.shape[-1]}) of points must be 2 or 4."
            raise ValueError(msg)
        out = self._forward_op(v, shapes, level_index, loc, attn)
        return self.proj_output(out)

    def _forward_op(
        self,
        v: torch.Tensor,
        shapes: torch.Tensor,
        level_index: torch.Tensor,
        loc: torch.Tensor,
        attn: torch.Tensor,
    ) -> torch.Tensor:
        return deformops.deform2d_multiscale_fused.forward(
            v,
            shapes,
            level_index,
            loc,
            attn,
            self.im2col_step,
            self.points,
        )

    if typing.TYPE_CHECKING:
        __call__ = forward


class MSDeformAttn2d(FusedMSDeformAttn2d):
    r"""
    Uses the legacy implementation from the `unipercept` library, which has slightly
    different results due to the sampling algorithm used.
    """

    class Method(E.StrEnum):
        r"""
        Attention modes for the deformable attention layer.
        """

        LINEAR = E.auto()
        SOFTMAX = E.auto()
        RECTIFIED = E.auto()

    type MethodType = (
        Method
        | typing.Literal["linear", "softmax", "rectified"]
        | typing.Callable[[torch.Tensor], torch.Tensor]
        | torch.nn.Module
    )

    method: typing.Final[MethodType]

    def __init__(
        self,
        *args,
        method: MethodType = Method.SOFTMAX,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.im2col_step = 128
        self.method = method

    def _generate_attn(self, attn: torch.Tensor) -> torch.Tensor:
        match self.method:
            case self.Method.LINEAR:
                pass
            case self.Method.SOFTMAX:
                attn = torch.nn.functional.softmax(attn, -1)
            case self.Method.RECTIFIED:
                attn = torch.nn.functional.relu(attn)
                attn = attn / (attn.sum(dim=-1, keepdim=True) + 1e-6)
            case fn if callable(fn):
                attn = fn(attn)
            case _:
                msg = f"Unsupported attention mode {self.method!r}!"
                raise NotImplementedError(msg)
        return attn.unflatten(-1, (self.levels, self.points))

    @typing.override
    def _forward_op(
        self,
        v: torch.Tensor,
        shapes: torch.Tensor,
        level_index: torch.Tensor,
        loc: torch.Tensor,
        attn: torch.Tensor,
    ) -> torch.Tensor:
        return deformops.deform2d_multiscale.forward(
            v,
            shapes,
            level_index,
            loc,
            self._generate_attn(attn),
            self.im2col_step,
        )
