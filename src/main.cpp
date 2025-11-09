#include <opencv2/opencv.hpp>
#include <thread>
#include "edgeSam.h"

int main(int argc, char** argv) {
    if (argc < 2) {
        printf("Please, add an image!");
        exit(0);
    }

    // Read Image Input
    std::string imageFilePath = argv[1];
    cv::Mat image = cv::imread(imageFilePath);
    if (image.empty()) {
        std::cout << "Image loading failed" << std::endl;
        return -1;
    }

    Sam::Parameter param("../models/edge_sam_3x_encoder.onnx", "../models/edge_sam_3x_decoder.onnx",
                         std::thread::hardware_concurrency());
    param.providers[0].deviceType = 0;
    param.providers[1].deviceType = 0;
    Sam sam(param);

    auto inputSize = sam.getInputSize();
    if (inputSize.empty()) {
        std::cout << "Sam initialization failed" << std::endl;
        return -1;
    }

    std::cout << "Resize image to " << inputSize << std::endl;
    cv::resize(image, image, inputSize);
    if (!sam.loadImage(image)) {
        std::cout << "Image loading failed" << std::endl;
        return -1;
    }

    cv::Rect box{0, 0, 1024, 1024};
    // std::list<cv::Point> points{cv::Point(512, 512)};
    // std::list<cv::Point> negativePoints{cv::Point(5, 5),cv::Point(1019, 5)};

    cv::Mat mask = sam.getMask({}, {}, box);
    cv::imwrite("../output/mask.png", mask);
    // apply mask to image
    cv::Mat outImage = image.clone();
    outImage = cv::Mat::zeros(image.size(), CV_8UC3);
    for (int i = 0; i < image.rows; i++) {
        for (int j = 0; j < image.cols; j++) {
            auto bFront = mask.at<uchar>(i, j) > 0;
            float factor = bFront ? 1.0 : 0.2;
            outImage.at<cv::Vec3b>(i, j) = image.at<cv::Vec3b>(i, j) * factor;
        }
    }
    cv::imwrite("../output/overlayImgMask.png", outImage);
}
