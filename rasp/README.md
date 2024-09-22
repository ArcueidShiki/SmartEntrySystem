On raspberrpi pi 

```bash
sudo apt-get update
sudo apt-get install onnxruntime

# compile 
g++ -o mask_detector mask_detector.cpp `pkg-config --cflags --libs opencv4` -lonnxruntime
./mask_detector
```