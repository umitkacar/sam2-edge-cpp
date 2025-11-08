"""EdgeSAM - Ultra-fast image segmentation with ONNX Runtime.

This package provides Python bindings for the EdgeSAM C++ implementation,
offering high-performance image segmentation on edge devices.
"""

from typing import TYPE_CHECKING

from edgesam_py.segmentation import EdgeSAMSegmenter


try:
    from edgesam_py._version import __version__
except ImportError:
    __version__ = "0.0.0+unknown"


__all__ = [
    "EdgeSAMSegmenter",
    "__version__",
]
