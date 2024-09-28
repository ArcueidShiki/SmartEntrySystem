#include <onnxruntime/core/session/onnxruntime_cxx_api.h>
#include <opencv2/opencv.hpp>
#include <iostream>
#include <vector>

int main()
{
    // Init ONNX Runtime environment
    Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "mask_detector");

    // Set session
    Ort::SessionOptions session_options;
    session_options.SetIntraOpNumThreads(1);

    // load ONNX model
    const char *model_path = "mask_detector.onnx";
    Ort::Session session(env, model_path, session_options);

    // get model input and output
    Ort::AllocatorWithDefaultOptions allocator;

    const char *input_name = session.GetInputName(0, allocator);
    const char *output_name = session.GetOutputName(0, allocator);
    std::cout << "Input Name: " << input_name << "\n";
    std::cout << "Output Name: " << output_name << "\n";

    // load images and preprocess
    cv::Mat img = cv::imread("test_image.jpg"); // read images
    cv::resize(img, img, cv::Size(224, 224));   // resize  image 224x224
    img.convertTo(img, CV_32F, 1.0 / 255);      // normalize 0 ~ 1
    cv::cvtColor(img, img, cv::COLOR_BGR2RGB);  // convert to rgb mode

    // convert image to float points
    std::vector<float> input_tensor_values(img.begin<float>(), img.end<float>());

    // input vector
    std::vector<int64_t> input_shape = {1, 224, 224, 3}; // 输入形状
    Ort::Value input_tensor = Ort::Value::CreateTensor<float>(allocator, input_tensor_values.data(), input_tensor_values.size(), input_shape.data(), input_shape.size());

    // run model
    auto output_tensors = session.Run(Ort::RunOptions{nullptr}, &input_name, &input_tensor, 1, &output_name, 1);

    // ouput
    float *raw_output = output_tensors.front().GetTensorMutableData<float>();

    std::cout << "Mask: " << raw_output[0] << " Without Mask: " << raw_output[1] << "\n";

    return 0;
}
