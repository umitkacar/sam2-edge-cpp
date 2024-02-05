#ifndef SAMCPP__SAM_H_
#define SAMCPP__SAM_H_

#include <opencv2/core.hpp>
#include <string>
#include <list>

struct SamModel;

class Sam {
  SamModel* m_model{nullptr};

 public:
  struct Parameter {
    struct Provider {
      // deviceType: 0 - CPU, 1 - CUDA
      int gpuDeviceId{0}, deviceType{0};
      size_t gpuMemoryLimit{0};
    };
    Provider providers[2];  // 0 - embedding, 1 - segmentation
    std::string models[2];  // 0 - embedding, 1 - segmentation
    int threadsNumber{1};
    Parameter(const std::string& preModelPath, const std::string& samModelPath, int threadsNumber) {
      models[0] = preModelPath;
      models[1] = samModelPath;
      this->threadsNumber = threadsNumber;
    }
  };
  // constructor
  Sam(const Parameter& param);
  ~Sam();

  cv::Size getInputSize() const;
  bool loadImage(const cv::Mat& image);

  cv::Mat getMask(const std::list<cv::Point>& points, const std::list<cv::Point>& negativePoints,
                  const cv::Rect& roi, double* iou = nullptr) const;
  cv::Mat getMask(const std::list<cv::Point>& points, const std::list<cv::Point>& negativePoints,
                  double* iou = nullptr) const;
  cv::Mat getMask(const cv::Point& point, double* iou = nullptr) const;

};

#endif  // SAMCPP__SAM_H_
