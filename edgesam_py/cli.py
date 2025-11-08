"""Command-line interface for EdgeSAM."""

from __future__ import annotations

import argparse
import sys
import traceback
from pathlib import Path

import numpy as np

from edgesam_py import __version__
from edgesam_py.segmentation import EdgeSAMSegmenter


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="EdgeSAM - Ultra-fast image segmentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"EdgeSAM {__version__}",
    )

    parser.add_argument(
        "-e",
        "--encoder",
        type=Path,
        default=Path("models/edge_sam_3x_encoder.onnx"),
        help="Path to encoder ONNX model (default: models/edge_sam_3x_encoder.onnx)",
    )

    parser.add_argument(
        "-d",
        "--decoder",
        type=Path,
        default=Path("models/edge_sam_3x_decoder.onnx"),
        help="Path to decoder ONNX model (default: models/edge_sam_3x_decoder.onnx)",
    )

    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        required=True,
        help="Path to input image",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Path to output image (default: input_path_segmented.png)",
    )

    parser.add_argument(
        "--point-x",
        type=float,
        help="X coordinate of prompt point",
    )

    parser.add_argument(
        "--point-y",
        type=float,
        help="Y coordinate of prompt point",
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Threshold for binary mask (default: 0.5)",
    )

    parser.add_argument(
        "--gpu",
        action="store_true",
        help="Use GPU acceleration if available",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose output",
    )

    return parser.parse_args()


def main() -> int:  # noqa: C901
    """Main entry point.

    Returns:
        Exit code.
    """
    args = parse_args()

    # Determine output path
    if args.output is None:
        args.output = args.input.with_stem(f"{args.input.stem}_segmented")

    if args.verbose:
        print(f"EdgeSAM v{__version__}")  # noqa: T201
        print(f"Encoder: {args.encoder}")  # noqa: T201
        print(f"Decoder: {args.decoder}")  # noqa: T201
        print(f"Input: {args.input}")  # noqa: T201
        print(f"Output: {args.output}")  # noqa: T201

    # Determine execution providers
    providers = ["CPUExecutionProvider"]
    if args.gpu:
        providers = [
            "CUDAExecutionProvider",
            "TensorrtExecutionProvider",
            "CPUExecutionProvider",
        ]
        if args.verbose:
            print("GPU acceleration enabled")  # noqa: T201

    try:
        # Initialize segmenter
        segmenter = EdgeSAMSegmenter(
            encoder_path=args.encoder,
            decoder_path=args.decoder,
            providers=providers,
        )

        if args.verbose:
            print(f"Initialized: {segmenter}")  # noqa: T201

        # Prepare prompt points
        point_coords = None
        point_labels = None

        if args.point_x is not None and args.point_y is not None:
            point_coords = np.array([[args.point_x, args.point_y]], dtype=np.float32)
            point_labels = np.array([1.0], dtype=np.float32)

            if args.verbose:
                print(f"Using prompt point: ({args.point_x}, {args.point_y})")  # noqa: T201

        # Segment image
        if args.verbose:
            print("Processing image...")  # noqa: T201

        image, mask = segmenter.segment(
            image_path=args.input,
            point_coords=point_coords,
            point_labels=point_labels,
        )

        # Save result
        if args.verbose:
            print(f"Saving result to {args.output}...")  # noqa: T201

        segmenter.save_result(
            image=image,
            mask=mask,
            output_path=args.output,
            threshold=args.threshold,
        )

        if args.verbose:
            print("Done!")  # noqa: T201

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)  # noqa: T201
        return 1

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)  # noqa: T201
        if args.verbose:
            traceback.print_exc()
        return 2


if __name__ == "__main__":
    sys.exit(main())
