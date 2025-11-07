
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
