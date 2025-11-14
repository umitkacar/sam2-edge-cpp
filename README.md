<div align="center">

# 🎯 EdgeSAM - ONNX Runtime C++
### *40x Faster Edge AI Segmentation with C++17*

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=3000&pause=1000&color=6366F1&center=true&vCenter=true&multiline=true&width=900&lines=Real-Time+SAM2+Segmentation+%F0%9F%9A%80;C%2B%2B17+%2B+ONNX+Runtime+1.12.1+%E2%9A%A1;40x+Faster+Edge+Inference+%F0%9F%94%A5" alt="Typing SVG" />

[![Stars](https://img.shields.io/github/stars/umitkacar/sam2-edge-cpp?style=for-the-badge&logo=github&color=yellow)](https://github.com/umitkacar/sam2-edge-cpp/stargazers)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![C++](https://img.shields.io/badge/C++-17-00599C?style=for-the-badge&logo=cplusplus&logoColor=white)](https://isocpp.org/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![ONNX](https://img.shields.io/badge/ONNX-Runtime_1.12.1-005CED?style=for-the-badge)](https://onnxruntime.ai/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8.0-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)

[![Tests](https://img.shields.io/badge/Tests-11/11_Pass-success?style=for-the-badge&logo=pytest)](tests/)
[![Coverage](https://img.shields.io/badge/Coverage-73.06%25-brightgreen?style=for-the-badge&logo=codecov)](htmlcov/)
[![MyPy](https://img.shields.io/badge/MyPy-0_Errors-blue?style=for-the-badge)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/badge/Ruff-0_Violations-red?style=for-the-badge)](https://github.com/astral-sh/ruff)

</div>

---

## 🌟 Overview

This project implements the **EdgeSAM** (Segmentation-Anything Model) using ONNX Runtime and OpenCV in C++, delivering **40x faster inference** for edge device deployment.

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

This project uses **ultra-modern** Python development tooling for production-ready code:

### Core Tools

- **[Hatch](https://hatch.pypa.io/)** - Modern Python project manager with environment isolation
- **[Ruff](https://github.com/astral-sh/ruff)** ⚡ - Ultra-fast linter **AND** formatter (10-100x faster than traditional tools!)
  - Replaces Black + Flake8 + isort + pyupgrade in a single tool
  - Written in Rust for maximum performance
- **[UV](https://github.com/astral-sh/uv)** 🚀 - Blazing fast Python package installer (10-100x faster than pip)
- **[MyPy](https://mypy-lang.org/)** - Strict static type checker with full coverage
- **[Pytest](https://pytest.org/)** - Testing framework with:
  - **pytest-xdist** for parallel execution (6x faster!)
  - **pytest-cov** for comprehensive coverage tracking (73%+ coverage)
  - **pytest-benchmark** for performance testing
- **[Pre-commit](https://pre-commit.com/)** - Automated quality gates on every commit

### Test Results ✅

```
✅ 11/11 tests passing (100%)
✅ 73.06% code coverage
✅ 0 mypy errors
✅ 0 ruff violations
✅ 0 security issues (bandit)
✅ Production ready!
```

### Coverage Breakdown

```
Name                         Stmts   Miss Branch BrPart   Cover
-----------------------------------------------------------------
edgesam_py/__init__.py           7      2      0      0  71.43%
edgesam_py/cli.py               64     21     22      8  59.30%
edgesam_py/segmentation.py      78      8     22      7  85.00%
-----------------------------------------------------------------
TOTAL                          149     31     44     15  73.06%
```

### Quick Start for Development

```bash
# 1. Clone the repository
git clone https://github.com/umitkacar/edgeSAM-onnxruntime-cpp
cd edgeSAM-onnxruntime-cpp

# 2. Install with development dependencies
pip install -e ".[dev]"

# 3. Install pre-commit hooks
pre-commit install

# 4. Run tests to verify installation
pytest -n auto

# 5. You're ready to develop! 🎉
```

### Development Commands

#### Using Hatch (Recommended)

```bash
# Run tests
hatch run test

# Run tests with coverage
hatch run test-cov

# Run tests in parallel (6x faster!)
pytest -n auto

# Run linters and type checking
hatch run lint:all

# Format code (Ruff)
hatch run lint:fmt

# Type checking (MyPy)
hatch run lint:typing
```

#### Using pytest directly

```bash
# Run all tests (fast, parallel)
pytest -n auto

# Run with verbose output
pytest -xvs

# Run with coverage report
pytest --cov=edgesam_py --cov-report=term-missing

# Run only fast tests (skip slow integration tests)
pytest -m "not slow"

# Run specific test file
pytest tests/test_segmentation.py

# Run specific test
pytest tests/test_cli.py::TestCLI::test_version_flag
```

#### Code Quality Commands

```bash
# Lint and auto-fix with Ruff
ruff check --fix .

# Format code with Ruff
ruff format .

# Type check with MyPy
mypy edgesam_py tests

# Run all quality checks
ruff check . && ruff format --check . && mypy edgesam_py tests
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

### Advanced Testing

```bash
# Run all tests with parallel execution (FAST!)
pytest -n auto

# Run with comprehensive coverage
pytest --cov=edgesam_py --cov-branch --cov-report=html
# Open htmlcov/index.html in browser to see detailed coverage

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only slow tests
pytest -m slow

# Run benchmarks
pytest -m benchmark

# Run with verbose output and stop on first failure
pytest -xvs --tb=short

# Run and generate all report formats
pytest --cov=edgesam_py --cov-report=term --cov-report=html --cov-report=xml
```

### Using UV for Faster Package Management

```bash
# Install dependencies with UV (10-100x faster than pip!)
uv pip install -e ".[dev]"

# Compile requirements with lock file
uv pip compile pyproject.toml -o requirements.txt

# Sync dependencies
uv pip sync requirements.txt

# Install a single package
uv pip install numpy
```

## 📊 Code Quality & Standards

### Automated Quality Enforcement

Every commit is automatically checked for:

- ✅ **Code Style**: Ruff formatting (Black-compatible, 100-char lines)
- ✅ **Linting**: Ruff linter (20+ rule categories including security)
- ✅ **Type Safety**: MyPy strict type checking with zero errors
- ✅ **Testing**: 73.06% code coverage, all tests passing
- ✅ **Security**: Bandit security scanning, no vulnerabilities
- ✅ **Secrets**: No credentials or API keys in code (detect-secrets)
- ✅ **Shell Scripts**: ShellCheck validation for bash scripts
- ✅ **Documentation**: Markdownlint for consistent docs

### Quality Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Test Coverage | ≥70% | **73.06%** | ✅ Pass |
| Tests Passing | 100% | **11/11 (100%)** | ✅ Pass |
| MyPy Errors | 0 | **0** | ✅ Pass |
| Ruff Violations | 0 | **0** | ✅ Pass |
| Security Issues | 0 | **0** | ✅ Pass |
| Type Hints | 100% | **100%** | ✅ Pass |

### Pre-commit Hooks Pipeline

When you commit, these checks run automatically:

1. **General Checks** (5 hooks)
   - Trailing whitespace removal
   - End-of-file fixing
   - YAML/TOML/JSON validation
   - Merge conflict detection
   - Large file prevention (>1MB)

2. **Python Quality** (4 hooks)
   - Ruff linting with auto-fix
   - Ruff formatting
   - MyPy type checking
   - PyUpgrade syntax modernization

3. **Security** (2 hooks)
   - Bandit security scanning
   - Detect-secrets credential scanning

4. **Multi-language** (5 hooks)
   - ShellCheck for bash scripts
   - Clang-format for C++ code
   - CMake-format for CMake files
   - Prettier for web files (JS/CSS/HTML)
   - Markdownlint for documentation

5. **Testing** (on push only - slower)
   - Full pytest suite
   - Coverage threshold check (≥70%)

**Total time**: ~5 seconds on commit, ~30 seconds on push

## 🏗️ Project Structure

```
edgeSAM-onnxruntime-cpp/
├── 📦 edgesam_py/              # Python package (production-ready)
│   ├── __init__.py             # Package exports and version
│   ├── _version.py             # Auto-generated version (VCS)
│   ├── segmentation.py         # Core EdgeSAM segmentation (85% coverage)
│   └── cli.py                  # Command-line interface (59% coverage)
│
├── 🧪 tests/                   # Comprehensive test suite (73% coverage)
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures and configuration
│   ├── test_segmentation.py   # Segmentation tests (7 tests)
│   └── test_cli.py             # CLI tests (4 tests)
│
├── 🔧 src/                     # C++ source code
│   ├── edgeSam.cpp             # C++ implementation
│   ├── edgeSam.h               # C++ headers
│   └── main.cpp                # C++ entry point
│
├── 📚 include/                 # ONNX Runtime headers
│   └── onnxruntime/            # ONNX Runtime C++ API
│
├── 🤖 models/                  # ONNX model files (not in repo)
│   ├── edge_sam_3x_encoder.onnx
│   └── edge_sam_3x_decoder.onnx
│
├── 🖼️ images/                  # Test images (not in repo)
│
├── 🌐 Web Interface
│   ├── index.html              # Modern glassmorphism UI
│   ├── styles.css              # Responsive styling
│   └── script.js               # Interactive features
│
├── 📋 Documentation
│   ├── README.md               # This file
│   ├── CHANGELOG.md            # Detailed version history
│   └── LESSONS_LEARNED.md      # Development insights (400+ lines)
│
├── ⚙️ Configuration
│   ├── pyproject.toml          # Python project config (modern, Hatch-based)
│   ├── .pre-commit-config.yaml # 15+ pre-commit hooks
│   ├── .clang-format           # C++ formatting rules
│   ├── .secrets.baseline       # Secret scanning baseline
│   └── build.sh                # C++ build script
│
└── 🔨 Build artifacts
    ├── htmlcov/                # Coverage HTML reports
    ├── .coverage               # Coverage data
    └── .pytest_cache/          # Pytest cache
```

### Key Files

- **pyproject.toml**: Modern Python packaging with Hatch, Ruff, MyPy configuration
- **LESSONS_LEARNED.md**: In-depth analysis of refactoring decisions (must-read!)
- **CHANGELOG.md**: Complete version history with migration guides

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Setup

1. **Fork and clone**:
```bash
git clone https://github.com/YOUR_USERNAME/edgeSAM-onnxruntime-cpp
cd edgeSAM-onnxruntime-cpp
```

2. **Create a feature branch**:
```bash
git checkout -b feature/amazing-feature
```

3. **Install development dependencies**:
```bash
pip install -e ".[dev]"
# Or use UV for faster installation:
uv pip install -e ".[dev]"
```

4. **Install pre-commit hooks**:
```bash
pre-commit install
```

### Development Workflow

1. **Make your changes** with confidence - tests will catch issues!

2. **Run tests locally**:
```bash
# Fast parallel tests
pytest -n auto

# With coverage
pytest --cov=edgesam_py
```

3. **Format and lint**:
```bash
# Auto-format code
ruff format .

# Lint and auto-fix
ruff check --fix .

# Type check
mypy edgesam_py tests
```

4. **Commit your changes**:
```bash
git add .
git commit -m 'Add amazing feature'
# Pre-commit hooks will run automatically!
```

5. **Push and create PR**:
```bash
git push origin feature/amazing-feature
# Then open a Pull Request on GitHub
```

### Quality Requirements

All contributions must pass:

- ✅ **Ruff linting** (no violations)
- ✅ **Ruff formatting** (Black-compatible style)
- ✅ **MyPy type checking** (strict mode, zero errors)
- ✅ **Pytest tests** (all tests passing)
- ✅ **Coverage** (maintain or improve 73%+ coverage)
- ✅ **Pre-commit hooks** (15+ automated checks)
- ✅ **Security scanning** (Bandit, no vulnerabilities)

### Testing Your Changes

```bash
# Run the full test suite
pytest -xvs

# Run with coverage check
pytest --cov=edgesam_py --cov-report=term-missing --cov-fail-under=70

# Run pre-commit on all files (same as CI)
pre-commit run --all-files

# Verify type safety
mypy edgesam_py tests
```

### Documentation

If you're adding new features:
- Add docstrings (Google style)
- Update README.md if needed
- Add tests for new functionality
- Update CHANGELOG.md

### Code Style Guidelines

We use **Ruff** for both linting and formatting:

```python
# Good - Type hints, clear names, docstrings
def segment_image(
    image_path: Path,
    point_coords: NDArray[np.float32] | None = None,
) -> tuple[NDArray[np.uint8], NDArray[np.float32]]:
    """Segment an image using EdgeSAM.

    Args:
        image_path: Path to input image.
        point_coords: Optional point coordinates for prompting.

    Returns:
        Tuple of (original image, segmentation mask).

    Raises:
        FileNotFoundError: If image doesn't exist.
    """
    # Implementation here
```

### Need Help?

- 📖 Read [LESSONS_LEARNED.md](LESSONS_LEARNED.md) for detailed insights
- 📋 Check [CHANGELOG.md](CHANGELOG.md) for recent changes
- 💬 Open an issue for questions or suggestions
- 🐛 Report bugs with minimal reproduction examples

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
