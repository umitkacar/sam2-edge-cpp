"""Pytest configuration and fixtures."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
import pytest

if TYPE_CHECKING:
    from numpy.typing import NDArray


@pytest.fixture
def sample_image() -> NDArray[np.uint8]:
    """Create a sample test image.

    Returns:
        Sample BGR image (256x256x3).
    """
    return np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)


@pytest.fixture
def models_dir() -> Path:
    """Get path to models directory.

    Returns:
        Path to models directory.
    """
    return Path(__file__).parent.parent / "models"


@pytest.fixture
def encoder_path(models_dir: Path) -> Path:
    """Get path to encoder model.

    Args:
        models_dir: Models directory fixture.

    Returns:
        Path to encoder model.
    """
    return models_dir / "edge_sam_3x_encoder.onnx"


@pytest.fixture
def decoder_path(models_dir: Path) -> Path:
    """Get path to decoder model.

    Args:
        models_dir: Models directory fixture.

    Returns:
        Path to decoder model.
    """
    return models_dir / "edge_sam_3x_decoder.onnx"


@pytest.fixture
def point_coords() -> NDArray[np.float32]:
    """Create sample point coordinates.

    Returns:
        Sample point coordinates.
    """
    return np.array([[512.0, 512.0]], dtype=np.float32)


@pytest.fixture
def point_labels() -> NDArray[np.float32]:
    """Create sample point labels.

    Returns:
        Sample point labels.
    """
    return np.array([1.0], dtype=np.float32)
