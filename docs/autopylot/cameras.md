---
title: Cameras
parent: autopylot
---

## Cameras
Folder containing the cameras class.

### Camera
To simplify the way to instantiate camera classes, we use the method Camera() declared in autopylot.cameras.py. \
It takes in argument the camera type you want to instantiate and returns the instance of that class.
If no arguments are provided, the instance will be created according to the CAMERA_TYPE from the JSON settings file.


Example:
```json
{
    "CAMERA_TYPE": "webcam",
    "SOME_OTHER_SETTINGS": "test"
}
```
```python
from autopylot.cameras import Camera

camera = Camera()
camera.update()
```
Would instantiate the camera referring to the CAMERA_TYPE: "webcam" (Webcam)

*Note: this is the only public method available to instantiate cameras (all the following classes are private).*


### Webcam
This is the default camera, it is used to fetch images from a physical camera (in our case a USB webcam). It can be selected using the CAMERA_TYPE: "webcam" option. \
If you want to force the use of the webcam camera without specifying the CAMERA_TYPE, you can use the following:
```python
from autopylot.cameras import Camera

camera = Camera(camera_type="webcam")
camera.update()
```
At every `camera.update()` call, an image is fetched from the camera and is stored into the memory under the "image" key.


### SimWebcam
This class is used to fetched images from the simulator. It can be selected using the CAMERA_TYPE: "sim" option. \
If you want to force the use of the webcam camera without specifying the CAMERA_TYPE, you can use the following:
```python
from autopylot.cameras import Camera

camera = Camera(camera_type="sim")
camera.update()
```
At every `camera.update()` call, an image is fetched from the simulator client and is stored into the memory under the "image" key.


### Replay
This class is used to simulate a camera from a dataset folder, in other words "replay the data". It can be selected using the CAMERA_TYPE: "replay" option. \
It has an optional argument dataset_path to specify the path to the dataset folder. If none are provided, it uses the DATASET_PATH from the JSON settings file. \
If you want to force the use of the replay camera without specifying the CAMERA_TYPE, you can use the following:
```python
from autopylot.cameras import Camera

camera = Camera(camera_type="replay")
camera.update()
```
At every `camera.update()` call, an image is fetched from dataset folder and is stored into the memory under the "image" key, it also loads the image data associated to the image and stores it into the memory.


### Dummy 
This class is used for testing purposes, when you don't have any data or camera, you can use this class instead. It can be selected using the CAMERA_TYPE: "dummy" option. \
If you want to force the use of the dummy camera without specifying the CAMERA_TYPE, you can use the following:
```python
from autopylot.cameras import Camera

camera = Camera(camera_type="dummy")
camera.update()
```
At every `camera.update()` call, a new random image is created and stored in the memory under the "image" key.