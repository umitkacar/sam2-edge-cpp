"""Tests for CLI module."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from edgesam_py import __version__
from edgesam_py.cli import main, parse_args


class TestCLI:
    """Tests for CLI functionality."""

    def test_version_flag(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test --version flag.

        Args:
            capsys: Pytest capture fixture.
        """
        with pytest.raises(SystemExit) as exc_info:
            with patch("sys.argv", ["edgesam", "--version"]):
                parse_args()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert __version__ in captured.out

    def test_parse_args_minimal(self) -> None:
        """Test parsing minimal arguments."""
        with patch("sys.argv", ["edgesam", "-i", "test.png"]):
            args = parse_args()

        assert args.input == Path("test.png")
        assert args.encoder == Path("models/edge_sam_3x_encoder.onnx")
        assert args.decoder == Path("models/edge_sam_3x_decoder.onnx")
        assert args.threshold == 0.5
        assert not args.gpu
        assert not args.verbose

    def test_parse_args_full(self) -> None:
        """Test parsing all arguments."""
        with patch(
            "sys.argv",
            [
                "edgesam",
                "-i",
                "input.png",
                "-o",
                "output.png",
                "-e",
                "encoder.onnx",
                "-d",
                "decoder.onnx",
                "--point-x",
                "100",
                "--point-y",
                "200",
                "--threshold",
                "0.7",
                "--gpu",
                "-v",
            ],
        ):
            args = parse_args()

        assert args.input == Path("input.png")
        assert args.output == Path("output.png")
        assert args.encoder == Path("encoder.onnx")
        assert args.decoder == Path("decoder.onnx")
        assert args.point_x == 100.0
        assert args.point_y == 200.0
        assert args.threshold == 0.7
        assert args.gpu
        assert args.verbose

    def test_main_missing_input(self) -> None:
        """Test main with missing input file."""
        with patch("sys.argv", ["edgesam", "-i", "nonexistent.png"]):
            exit_code = main()

        assert exit_code == 1

    @patch("edgesam_py.cli.EdgeSAMSegmenter")
    def test_main_success(
        self,
        mock_segmenter: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Test successful main execution.

        Args:
            mock_segmenter: Mocked segmenter class.
            tmp_path: Temporary directory fixture.
        """
        # Create dummy input file
        input_file = tmp_path / "test.png"
        input_file.touch()

        # Create dummy model files
        encoder_file = tmp_path / "encoder.onnx"
        decoder_file = tmp_path / "decoder.onnx"
        encoder_file.touch()
        decoder_file.touch()

        # Mock segmenter instance
        mock_instance = MagicMock()
        mock_segmenter.return_value = mock_instance

        with patch(
            "sys.argv",
            [
                "edgesam",
                "-i",
                str(input_file),
                "-e",
                str(encoder_file),
                "-d",
                str(decoder_file),
            ],
        ):
            exit_code = main()

        assert exit_code == 0
        mock_segmenter.assert_called_once()
        mock_instance.segment.assert_called_once()
        mock_instance.save_result.assert_called_once()
