
# EdgeSAM - Onnxruntime - C++

🚀 **Ultra-Modern AI-Powered Image Segmentation**

This project implements the EdgeSAM (Segmentation-Anything Model) using ONNX Runtime and OpenCV in C++.

## 🌐 Web Interface

Visit our ultra-modern web interface by opening `index.html` in your browser to explore:
- 🎨 Interactive demo with animations
- ⚡ Feature showcase with glassmorphism design
- 📚 Quick installation guide
- 🎯 Technology stack overview

**Features:**
- Modern, responsive design
- Smooth animations and transitions
- Interactive UI elements
- Dark theme with gradient effects

## Paper

- [EdgeSAM: Prompt-In-the-Loop Distillation for On-Device Deployment of SAM](https://arxiv.org/pdf/2312.06660.pdf)

## Features

- Uses Edge SAM model for segmentation, which includes a preprocessing model and a SAM model.
- Image preprocessing and segmentation with ONNX Runtime and OpenCV.
- Efficient handling of image inputs and outputs.
- Customizable for different segmentation tasks.

## Model Compatibility

- This implementation is compatible with the Edge SAM model in ONNX format. The model paths are specified in the parameters and expected to be in the ONNX format.

## Installation

Before running the project, ensure that the following libraries are installed:

- C++ Compiler (supporting C++17 or later)
- OpenCV (4.8.0)
- ONNX Runtime (1.12.1)

These libraries can typically be installed via `pip` or your system's package manager.

## Usage

- Place your ONNX model files in the models directory.
- Place the images for processing in the images directory.
- Compile the code using a C++ compiler.
- Run the executable. The program processes the image using the EdgeSAM model and outputs the results.

```bash
. ./build.sh
./edgeSamOrtCpp ../images/xxx.png
```

## Input Format

The application expects the following input format:

- Model path: "../models/edge_sam_3x_encoder.onnx" or "../models/edge_sam_3x_decoder.onnx"
- Image path: "../images/xxx.png"

## Output

The program outputs the segmented image with applied masks. Additional information like image resizing and processing steps are logged to the console.

---

## 🐍 Python Package

EdgeSAM now includes a comprehensive Python package with modern development tooling!

### Installation

```bash
# Install from source
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"

# Install with all optional dependencies
pip install -e ".[all]"
```

### Quick Start (Python)

```python
from edgesam_py import EdgeSAMSegmenter
import numpy as np

# Initialize segmenter
segmenter = EdgeSAMSegmenter(
    encoder_path="models/edge_sam_3x_encoder.onnx",
    decoder_path="models/edge_sam_3x_decoder.onnx"
)

# Segment an image
image, mask = segmenter.segment("path/to/image.png")

# Save result
segmenter.save_result(image, mask, "output.png")
```

### Command Line Interface

```bash
# Basic usage
edgesam -i input.png

# With custom prompt point
edgesam -i input.png --point-x 512 --point-y 512

# With GPU acceleration
edgesam -i input.png --gpu

# Full options
edgesam -i input.png -o output.png \
  -e models/encoder.onnx \
  -d models/decoder.onnx \
  --threshold 0.7 \
  --verbose
```

## 🛠️ Development Tools

This project uses ultra-modern Python development tooling:

### Core Tools

- **[Hatch](https://hatch.pypa.io/)** - Modern Python project manager
- **[Ruff](https://github.com/astral-sh/ruff)** - Ultra-fast Python linter & formatter
- **[Black](https://github.com/psf/black)** - Uncompromising code formatter
- **[MyPy](https://mypy-lang.org/)** - Static type checker
- **[Pytest](https://pytest.org/)** - Testing framework with coverage
- **[Pre-commit](https://pre-commit.com/)** - Git hook framework

### Quick Commands

```bash
# Setup development environment
make dev

# Run tests
make test

# Run tests with coverage
make test-cov

# Run linters
make lint

# Auto-format code
make format

# Run pre-commit hooks
make pre-commit

# Build C++ project
make build-cpp

# Build Python package
make build

# Clean build artifacts
make clean

# Run all CI checks locally
make ci
```

### Using Hatch

```bash
# Run tests
hatch run test:test

# Run tests with coverage
hatch run test:test-cov

# Run linters
hatch run lint:all

# Format code
hatch run lint:fmt

# Type checking
hatch run lint:typing
```

### Pre-commit Hooks

Install pre-commit hooks:

```bash
pre-commit install
```

Run on all files:

```bash
pre-commit run --all-files
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run benchmarks
pytest -m benchmark
```

## 📊 Code Quality

- **Type Hints**: Full type coverage with MyPy
- **Linting**: Comprehensive linting with Ruff
- **Formatting**: Consistent style with Black
- **Testing**: High test coverage with Pytest
- **Security**: Automated security checks with Bandit
- **Pre-commit**: Automated checks on every commit
- **CI/CD**: GitHub Actions for continuous integration

## 🏗️ Project Structure

```
edgeSAM-onnxruntime-cpp/
├── edgesam_py/              # Python package
│   ├── __init__.py
│   ├── segmentation.py      # Core segmentation logic
│   └── cli.py               # Command-line interface
├── tests/                   # Test suite
│   ├── conftest.py          # Pytest fixtures
│   ├── test_segmentation.py
│   └── test_cli.py
├── src/                     # C++ source code
├── include/                 # C++ headers
├── models/                  # ONNX model files
├── .github/workflows/       # CI/CD workflows
├── pyproject.toml           # Python project configuration
├── .pre-commit-config.yaml  # Pre-commit hooks
├── Makefile                 # Development commands
└── README.md
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies (`make dev`)
4. Make your changes
5. Run tests and linters (`make check`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

All commits must pass:
- ✅ Ruff linting
- ✅ Black formatting
- ✅ MyPy type checking
- ✅ Pytest tests
- ✅ Pre-commit hooks

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
