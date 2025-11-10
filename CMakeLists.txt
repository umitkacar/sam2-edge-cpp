cmake_minimum_required(VERSION 3.15)

set(PROJECT_NAME edgeSamOrtCpp)
project(
  ${PROJECT_NAME}
  VERSION 1.0.0
  LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)

find_package(Threads)

set(ORT_DIR "${CMAKE_CURRENT_LIST_DIR}/include/onnxruntime/core/session")

find_package(OpenCV REQUIRED)
include_directories(${ORT_DIR} ${OpenCV_INCLUDE_DIRS})

add_executable(${PROJECT_NAME} src/main.cpp src/edgeSam.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE onnxruntime ${OpenCV_LIBS})
