"""EdgeSAM segmentation implementation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import cv2
import numpy as np
import onnxruntime as ort
from numpy.typing import NDArray


class EdgeSAMSegmenter:
    """High-performance image segmentation using EdgeSAM model.

    This class provides an interface to the EdgeSAM model for efficient
    image segmentation on edge devices using ONNX Runtime.

    Attributes:
        encoder_path: Path to the encoder ONNX model.
        decoder_path: Path to the decoder ONNX model.
        providers: ONNX Runtime execution providers.
    """

    def __init__(
        self,
        encoder_path: str | Path,
        decoder_path: str | Path,
        providers: list[str] | None = None,
    ) -> None:
        """Initialize the EdgeSAM segmenter.

        Args:
            encoder_path: Path to the encoder ONNX model file.
            decoder_path: Path to the decoder ONNX model file.
            providers: List of ONNX Runtime execution providers.
                Defaults to ['CPUExecutionProvider'].

        Raises:
            FileNotFoundError: If model files don't exist.
            RuntimeError: If ONNX Runtime session creation fails.
        """
        self.encoder_path = Path(encoder_path)
        self.decoder_path = Path(decoder_path)

        if not self.encoder_path.exists():
            msg = f"Encoder model not found: {self.encoder_path}"
            raise FileNotFoundError(msg)

        if not self.decoder_path.exists():
            msg = f"Decoder model not found: {self.decoder_path}"
            raise FileNotFoundError(msg)

        if providers is None:
            providers = ["CPUExecutionProvider"]

        self.providers = providers

        # Create ONNX Runtime sessions
        sess_options = ort.SessionOptions()
        sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

        self.encoder_session = ort.InferenceSession(
            str(self.encoder_path),
            sess_options,
            providers=self.providers,
        )

        self.decoder_session = ort.InferenceSession(
            str(self.decoder_path),
            sess_options,
            providers=self.providers,
        )

        # Get model metadata
        self._encoder_input_name = self.encoder_session.get_inputs()[0].name
        self._encoder_output_name = self.encoder_session.get_outputs()[0].name
        self._decoder_input_names = [inp.name for inp in self.decoder_session.get_inputs()]
        self._decoder_output_name = self.decoder_session.get_outputs()[0].name

    def preprocess_image(
        self,
        image: NDArray[np.uint8],
        target_size: tuple[int, int] = (1024, 1024),
    ) -> tuple[NDArray[np.float32], tuple[int, int]]:
        """Preprocess image for model input.

        Args:
            image: Input image in BGR format (HxWxC).
            target_size: Target size for resizing (height, width).

        Returns:
            Tuple of (preprocessed image, original size).
        """
        original_size = image.shape[:2]

        # Resize image
        resized = cv2.resize(image, target_size[::-1], interpolation=cv2.INTER_LINEAR)

        # Convert BGR to RGB
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

        # Normalize to [0, 1] and convert to float32
        normalized = rgb.astype(np.float32) / 255.0

        # Transpose to CHW format and add batch dimension
        preprocessed = np.transpose(normalized, (2, 0, 1))[np.newaxis, ...]

        return preprocessed, original_size

    def encode(self, image: NDArray[np.float32]) -> NDArray[Any]:
        """Encode image using the encoder model.

        Args:
            image: Preprocessed image tensor (1xCxHxW).

        Returns:
            Encoded features from the encoder model.
        """
        encoder_outputs = self.encoder_session.run(
            [self._encoder_output_name],
            {self._encoder_input_name: image},
        )
        return encoder_outputs[0]

    def decode(
        self,
        features: NDArray[Any],
        point_coords: NDArray[np.float32] | None = None,
        point_labels: NDArray[np.float32] | None = None,
    ) -> NDArray[np.float32]:
        """Decode features to generate segmentation mask.

        Args:
            features: Encoded features from encoder.
            point_coords: Point coordinates for prompting (Nx2).
            point_labels: Point labels (N,). 1 for foreground, 0 for background.

        Returns:
            Segmentation mask.
        """
        # Create default prompts if not provided
        if point_coords is None:
            point_coords = np.array([[512.0, 512.0]], dtype=np.float32)

        if point_labels is None:
            point_labels = np.array([1.0], dtype=np.float32)

        # Prepare decoder inputs
        decoder_inputs = {
            self._decoder_input_names[0]: features,
            self._decoder_input_names[1]: point_coords[np.newaxis, ...],
            self._decoder_input_names[2]: point_labels[np.newaxis, ...],
        }

        # Run decoder
        decoder_outputs = self.decoder_session.run(
            [self._decoder_output_name],
            decoder_inputs,
        )

        return decoder_outputs[0]

    def segment(
        self,
        image_path: str | Path,
        point_coords: NDArray[np.float32] | None = None,
        point_labels: NDArray[np.float32] | None = None,
    ) -> tuple[NDArray[np.uint8], NDArray[np.float32]]:
        """Segment an image.

        Args:
            image_path: Path to input image.
            point_coords: Optional point coordinates for prompting.
            point_labels: Optional point labels.

        Returns:
            Tuple of (original image, segmentation mask).

        Raises:
            FileNotFoundError: If image file doesn't exist.
        """
        image_path = Path(image_path)
        if not image_path.exists():
            msg = f"Image not found: {image_path}"
            raise FileNotFoundError(msg)

        # Read image
        image = cv2.imread(str(image_path))
        if image is None:
            msg = f"Failed to read image: {image_path}"
            raise RuntimeError(msg)

        # Preprocess
        preprocessed, original_size = self.preprocess_image(image)

        # Encode
        features = self.encode(preprocessed)

        # Decode
        mask = self.decode(features, point_coords, point_labels)

        # Resize mask to original size
        mask_resized = cv2.resize(
            mask[0, 0],
            (original_size[1], original_size[0]),
            interpolation=cv2.INTER_LINEAR,
        )

        return image, mask_resized

    def save_result(
        self,
        image: NDArray[np.uint8],
        mask: NDArray[np.float32],
        output_path: str | Path,
        threshold: float = 0.5,
    ) -> None:
        """Save segmentation result.

        Args:
            image: Original image.
            mask: Segmentation mask.
            output_path: Path to save the result.
            threshold: Threshold for binary mask.
        """
        # Apply threshold to create binary mask
        binary_mask = (mask > threshold).astype(np.uint8) * 255

        # Create colored overlay
        overlay = image.copy()
        overlay[binary_mask > 0] = [0, 255, 0]  # Green overlay

        # Blend original and overlay
        result = cv2.addWeighted(image, 0.7, overlay, 0.3, 0)

        # Save result
        cv2.imwrite(str(output_path), result)

    def __repr__(self) -> str:
        """Return string representation."""
        return (
            f"EdgeSAMSegmenter("
            f"encoder={self.encoder_path.name}, "
            f"decoder={self.decoder_path.name}, "
            f"providers={self.providers})"
        )
