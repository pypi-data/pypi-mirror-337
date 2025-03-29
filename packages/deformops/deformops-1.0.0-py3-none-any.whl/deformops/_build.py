r"""
C++/CUDA extensions for deformable operations.
"""

import functools
import pathlib
import typing
import importlib.resources
import torch.utils.cpp_extension

__all__: list[str] = []


def load_extension(
    name: str,
    /,
    *,
    debug: bool = False,
    with_cuda: bool = True,
    extra_cflags: typing.Iterable[str] = (),
    extra_cuda_cflags: typing.Iterable[str] = (),
    extra_sources: typing.Iterable[str | pathlib.Path] = (),
    extra_include_paths: typing.Iterable[str | pathlib.Path] = (),
) -> None:
    r"""
    Build an extension just-in-time (JIT) using the provided arguments.
    """

    root = importlib.resources.files("deformops.include")
    opt_level = "0" if debug else "2"
    sources = [root / f"{name}.cpp"] + [root / p for p in extra_sources]
    extra_include_paths = [root / p for p in extra_include_paths]
    extra_cflags = [
        "-fdiagnostics-color=always",
        "-std=c++17",
        "-DPy_LIMITED_API=0x03012000",
        f"-O{opt_level}",
        *extra_cflags,
    ]
    extra_cuda_cflags = [
        "--std=c++17",
        f"-O{opt_level}",
        *extra_cuda_cflags,
    ]

    if with_cuda:
        # if CUDA_HOME is None or not pathlib.Path(CUDA_HOME).is_dir():
        #     msg = f"CUDA is not available. Found {CUDA_HOME=}"
        #     raise RuntimeError(msg)
        sources.append(root / "cuda" / f"{name}.cu")
        extra_include_paths.append(root / "cuda")

    torch.utils.cpp_extension.load(
        name=name,
        with_cuda=with_cuda,
        sources=list(map(str, sources)),
        extra_include_paths=list(map(str, extra_include_paths)),
        extra_cflags=extra_cflags,
        extra_cuda_cflags=extra_cuda_cflags,
        keep_intermediates=False,
        is_python_module=False,
        is_standalone=False,
        verbose=True,
    )
