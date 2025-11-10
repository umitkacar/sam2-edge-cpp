"""Tests for segmentation module."""

from __future__ import annotations

from typing import TYPE_CHECKING

import cv2
import numpy as np
import pytest

from edgesam_py.segmentation import EdgeSAMSegmenter


if TYPE_CHECKING:
    from pathlib import Path

    from numpy.typing import NDArray


class TestEdgeSAMSegmenter:
    """Tests for EdgeSAMSegmenter class."""

    def test_init_with_invalid_encoder_path(self, decoder_path: Path) -> None:
        """Test initialization with invalid encoder path.

        Args:
            decoder_path: Decoder path fixture.
        """
        with pytest.raises(FileNotFoundError, match="Encoder model not found"):
            EdgeSAMSegmenter(
                encoder_path="invalid_path.onnx",
                decoder_path=decoder_path,
            )

    def test_init_with_invalid_decoder_path(self, encoder_path: Path) -> None:
        """Test initialization with invalid decoder path.

        Args:
            encoder_path: Encoder path fixture.
        """
        with pytest.raises(FileNotFoundError, match="Decoder model not found"):
            EdgeSAMSegmenter(
                encoder_path=encoder_path,
                decoder_path="invalid_path.onnx",
            )

    def test_preprocess_image(
        self,
        encoder_path: Path,
        decoder_path: Path,
        sample_image: NDArray[np.uint8],
    ) -> None:
        """Test image preprocessing.

        Args:
            encoder_path: Encoder path fixture.
            decoder_path: Decoder path fixture.
            sample_image: Sample image fixture.
        """
        # Skip if models don't exist
        if not encoder_path.exists() or not decoder_path.exists():
            pytest.skip("Model files not found")

        segmenter = EdgeSAMSegmenter(
            encoder_path=encoder_path,
            decoder_path=decoder_path,
        )

        preprocessed, original_size = segmenter.preprocess_image(sample_image)

        # Check output shape
        assert preprocessed.shape == (1, 3, 1024, 1024)
        assert preprocessed.dtype == np.float32
        assert original_size == (256, 256)

        # Check value range
        assert preprocessed.min() >= 0.0
        assert preprocessed.max() <= 1.0

    def test_preprocess_image_custom_size(
        self,
        encoder_path: Path,
        decoder_path: Path,
        sample_image: NDArray[np.uint8],
    ) -> None:
        """Test image preprocessing with custom size.

        Args:
            encoder_path: Encoder path fixture.
            decoder_path: Decoder path fixture.
            sample_image: Sample image fixture.
        """
        if not encoder_path.exists() or not decoder_path.exists():
            pytest.skip("Model files not found")

        segmenter = EdgeSAMSegmenter(
            encoder_path=encoder_path,
            decoder_path=decoder_path,
        )

        target_size = (512, 512)
        preprocessed, _ = segmenter.preprocess_image(sample_image, target_size)

        assert preprocessed.shape == (1, 3, 512, 512)

    def test_repr(self, encoder_path: Path, decoder_path: Path) -> None:
        """Test string representation.

        Args:
            encoder_path: Encoder path fixture.
            decoder_path: Decoder path fixture.
        """
        if not encoder_path.exists() or not decoder_path.exists():
            pytest.skip("Model files not found")

        segmenter = EdgeSAMSegmenter(
            encoder_path=encoder_path,
            decoder_path=decoder_path,
        )

        repr_str = repr(segmenter)

        assert "EdgeSAMSegmenter" in repr_str
        assert "encoder" in repr_str
        assert "decoder" in repr_str


@pytest.mark.slow
@pytest.mark.integration
class TestEdgeSAMIntegration:
    """Integration tests for EdgeSAM."""

    def test_full_pipeline(
        self,
        encoder_path: Path,
        decoder_path: Path,
        sample_image: NDArray[np.uint8],
        point_coords: NDArray[np.float32],
        point_labels: NDArray[np.float32],
        tmp_path: Path,
    ) -> None:
        """Test full segmentation pipeline.

        Args:
            encoder_path: Encoder path fixture.
            decoder_path: Decoder path fixture.
            sample_image: Sample image fixture.
            point_coords: Point coordinates fixture.
            point_labels: Point labels fixture.
            tmp_path: Temporary directory fixture.
        """
        if not encoder_path.exists() or not decoder_path.exists():
            pytest.skip("Model files not found")

        # Save sample image
        image_path = tmp_path / "test_image.png"
        cv2.imwrite(str(image_path), sample_image)

        # Initialize segmenter
        segmenter = EdgeSAMSegmenter(
            encoder_path=encoder_path,
            decoder_path=decoder_path,
        )

        # Segment image
        image, mask = segmenter.segment(
            image_path=image_path,
            point_coords=point_coords,
            point_labels=point_labels,
        )

        # Verify outputs
        assert image.shape == sample_image.shape
        assert mask.shape == sample_image.shape[:2]
        assert mask.dtype == np.float32

        # Save result
        output_path = tmp_path / "result.png"
        segmenter.save_result(image, mask, output_path)

        assert output_path.exists()
