#include "edgeSam.h"
#include <onnxruntime_cxx_api.h>
#include <fstream>
#include <iostream>
#include <opencv2/opencv.hpp>
#include <string>
#include <vector>

struct SamModel {
    Ort::Env env{ORT_LOGGING_LEVEL_WARNING};
    std::unique_ptr<Ort::Session> sessionPre, sessionSam;

    std::vector<int64_t> inputShapePre, outputShapePre;
    Ort::MemoryInfo memoryInfo{Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeCPU)};
    std::vector<float> outputTensorValuesPre;
    const char *inputNamesEdgeSam[3]{"image_embeddings", "point_coords", "point_labels"},
        *outputNamesEdgeSam[2]{"scores", "masks"};

    bool bModelLoaded = false;
    SamModel(const Sam::Parameter& param) {
        for (auto& p : param.models) {
            std::ifstream f(p);
            if (!f.good()) {
                std::cerr << "Model file " << p << " not found" << std::endl;
                return;
            }
        }

        auto wpreModelPath = param.models[0];
        auto wsamModelPath = param.models[1];

        sessionPre = std::make_unique<Ort::Session>(env, wpreModelPath.c_str(),
                                                    Ort::SessionOptions{nullptr});
        int targetNumber[]{1, 3};
        if (sessionPre->GetInputCount() != 1 || sessionPre->GetOutputCount() != targetNumber[0]) {
            std::cerr << "Preprocessing model not loaded (invalid input/output count)" << std::endl;
            return;
        }

        sessionSam = std::make_unique<Ort::Session>(env, wsamModelPath.c_str(),
                                                    Ort::SessionOptions{nullptr});
        const auto samOutputCount = sessionSam->GetOutputCount();
        if (sessionSam->GetInputCount() != targetNumber[1]) {
            std::cerr << "Model not loaded (invalid input/output count)" << std::endl;
            return;
        }

        inputShapePre = sessionPre->GetInputTypeInfo(0).GetTensorTypeAndShapeInfo().GetShape();
        outputShapePre = sessionPre->GetOutputTypeInfo(0).GetTensorTypeAndShapeInfo().GetShape();
        if (inputShapePre.size() != 4 || outputShapePre.size() != 4) {
            std::cerr << "Preprocessing model not loaded (invalid shape)" << std::endl;
            return;
        }

        bModelLoaded = true;
    }

    cv::Size getInputSize() const {
        if (!bModelLoaded) return cv::Size(0, 0);
        return cv::Size(inputShapePre[3], inputShapePre[2]);
    }
    bool loadImage(const cv::Mat& image) {
        if (image.size() != cv::Size(inputShapePre[3], inputShapePre[2])) {
            std::cerr << "Image size not match" << std::endl;
            return false;
        }
        if (image.channels() != 3) {
            std::cerr << "Input is not a 3-channel image" << std::endl;
            return false;
        }

        std::vector<float> inputTensorValuesFloat;
        inputTensorValuesFloat.resize(inputShapePre[0] * inputShapePre[1] * inputShapePre[2] *
                                      inputShapePre[3]);
        for (int i = 0; i < inputShapePre[2]; i++) {
            for (int j = 0; j < inputShapePre[3]; j++) {
                inputTensorValuesFloat[i * inputShapePre[3] + j] = image.at<cv::Vec3b>(i, j)[2];
                inputTensorValuesFloat[inputShapePre[2] * inputShapePre[3] + i * inputShapePre[3] +
                                       j] = image.at<cv::Vec3b>(i, j)[1];
                inputTensorValuesFloat[2 * inputShapePre[2] * inputShapePre[3] +
                                       i * inputShapePre[3] + j] = image.at<cv::Vec3b>(i, j)[0];
            }
        }

        for (auto& v : inputTensorValuesFloat) {
            v /= 255.;
        }

        auto inputTensor = Ort::Value::CreateTensor<float>(
            memoryInfo, inputTensorValuesFloat.data(), inputTensorValuesFloat.size(),
            inputShapePre.data(), inputShapePre.size());
        std::vector<Ort::Value> outputTensors;
        outputTensorValuesPre = std::vector<float>(outputShapePre[0] * outputShapePre[1] *
                                                   outputShapePre[2] * outputShapePre[3]);
        outputTensors.push_back(Ort::Value::CreateTensor<float>(
            memoryInfo, outputTensorValuesPre.data(), outputTensorValuesPre.size(),
            outputShapePre.data(), outputShapePre.size()));

        Ort::RunOptions run_options;
        const char *inputNamesPreEdge[] = {"image"}, *outputNamesPreEdge[] = {"image_embeddings"};
        sessionPre->Run(run_options, inputNamesPreEdge, &inputTensor, 1, outputNamesPreEdge,
                        outputTensors.data(), outputTensors.size());

        return true;
    }

    void getMask(const std::list<cv::Point>& points, const std::list<cv::Point>& negativePoints,
                 const cv::Rect& roi, cv::Mat& outputMaskSam, double& iouValue) const {
        const size_t maskInputSize = 256 * 256;
        float maskInputValues[maskInputSize],
            hasMaskValues[] = {0},
            orig_im_size_values[] = {(float)inputShapePre[2], (float)inputShapePre[3]};
        memset(maskInputValues, 0, sizeof(maskInputValues));

        std::vector<float> inputPointValues, inputLabelValues;
        for (auto& point : points) {
            inputPointValues.push_back((float)point.x);
            inputPointValues.push_back((float)point.y);
            inputLabelValues.push_back(1);
        }
        for (auto& point : negativePoints) {
            inputPointValues.push_back((float)point.x);
            inputPointValues.push_back((float)point.y);
            inputLabelValues.push_back(0);
        }

        if (!roi.empty()) {
            inputPointValues.push_back((float)roi.x);
            inputPointValues.push_back((float)roi.y);
            inputLabelValues.push_back(2);
            inputPointValues.push_back((float)roi.br().x);
            inputPointValues.push_back((float)roi.br().y);
            inputLabelValues.push_back(3);
        }

        const int numPoints = inputLabelValues.size();
        std::vector<int64_t> inputPointShape = {1, numPoints, 2}, pointLabelsShape = {1, numPoints},
                             maskInputShape = {1, 1, 256, 256}, hasMaskInputShape = {1},
                             origImSizeShape = {2};

        std::vector<Ort::Value> inputTensorsSam;
        inputTensorsSam.push_back(Ort::Value::CreateTensor<float>(
            memoryInfo, (float*)outputTensorValuesPre.data(), outputTensorValuesPre.size(),
            outputShapePre.data(), outputShapePre.size()));

        auto inputNames = inputNamesEdgeSam;
        auto outputNames = outputNamesEdgeSam;
        int outputNumber = 2;
        int outputMaskIndex = 1;
        int outputIOUIndex = 0;

        inputTensorsSam.push_back(
            Ort::Value::CreateTensor<float>(memoryInfo, inputPointValues.data(), 2 * numPoints,
                                            inputPointShape.data(), inputPointShape.size()));
        inputTensorsSam.push_back(
            Ort::Value::CreateTensor<float>(memoryInfo, inputLabelValues.data(), numPoints,
                                            pointLabelsShape.data(), pointLabelsShape.size()));

        if (outputMaskSam.type() != CV_8UC1 ||
            outputMaskSam.size() != cv::Size(inputShapePre[3], inputShapePre[2])) {
            outputMaskSam = cv::Mat(inputShapePre[2], inputShapePre[3], CV_8UC1);
        }

        Ort::RunOptions runOptionsSam;
        auto outputTensorsSam = sessionSam->Run(runOptionsSam, inputNames, inputTensorsSam.data(),
                                                inputTensorsSam.size(), outputNames, outputNumber);

        auto& outputMask = outputTensorsSam[outputMaskIndex];
        auto maskShape = outputMask.GetTensorTypeAndShapeInfo().GetShape();

        cv::Mat outputMaskImage(maskShape[2], maskShape[3], CV_32FC1,
                                outputMask.GetTensorMutableData<float>());

        if (outputMaskImage.size() != outputMaskSam.size()) {
            cv::resize(outputMaskImage, outputMaskImage, outputMaskSam.size());
        }

        for (int i = 0; i < outputMaskSam.rows; i++) {
            for (int j = 0; j < outputMaskSam.cols; j++) {
                outputMaskSam.at<uint8_t>(i, j) = outputMaskImage.at<float>(i, j) > 0 ? 255 : 0;
            }
        }

        iouValue = outputTensorsSam[outputIOUIndex].GetTensorMutableData<float>()[0];
    }
};

Sam::Sam(const Parameter& param) : m_model(new SamModel(param)) {}
Sam::~Sam() { delete m_model; }

cv::Size Sam::getInputSize() const { return m_model->getInputSize(); }
bool Sam::loadImage(const cv::Mat& image) { return m_model->loadImage(image); }

cv::Mat Sam::getMask(const cv::Point& point, double* iou) const {
    return getMask({point}, {}, {}, iou);
}

cv::Mat Sam::getMask(const std::list<cv::Point>& points, const std::list<cv::Point>& negativePoints,
                     double* iou) const {
    return getMask(points, negativePoints, {}, iou);
}

cv::Mat Sam::getMask(const std::list<cv::Point>& points, const std::list<cv::Point>& negativePoints,
                     const cv::Rect& roi, double* iou) const {
    double iouValue = 0;
    cv::Mat m;
    m_model->getMask(points, negativePoints, roi, m, iouValue);
    if (iou != nullptr) {
        *iou = iouValue;
    }
    return m;
}
