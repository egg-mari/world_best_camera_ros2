
# World Best Camera ROS2 App

## Overview

This project is a simple camera application developed using ROS 2 (Robot Operating System version 2). The app is designed to publish and subscribe to image topics in ROS 2, enabling real-time reception and display of camera feeds.

## Installation

Before you begin, ensure that you have ROS 2 installed on your system. For installation instructions, refer to the [ROS 2 Documentation](https://docs.ros.org/en/galactic/Installation.html).

To install the World Best Camera ROS2 App, follow these steps:


# Clone the repository
```bash
git clone https://github.com/yourusername/ros2-camera-app.git
```
# Navigate to the repository directory
```bash
cd ros2-camera-app
```
# Build the ROS 2 packages
```bash
colcon build
```

## Usage

To run the camera app:


# Launch the camera app
```bash
ros2 launch camera camera.launch.py
```

Upon launching the app, the camera feed will be displayed. You can interact with the application through the following interfaces:

## Interface

When you execute the launch file in the terminal, `rqt` will be executed, and the following interfaces will be available:

1. **Default Camera View**: The default camera feed will be displayed.

2. **Filter Selection**: Click this section to change the image filter.

   ![Default Camera View](https://github.com/junroun/world_best_camera_ros2/assets/162243442/d5d2e7e6-d9f4-419e-bd5a-c571db994012)

3. **Available Filters**: Choose from available filters such as 'blur', 'bolol', 'median', 'mirror', 'rens', and 'sharpening'.

4. **Video Recording**:
   - Press the 'R' key to start recording the video.
   - To stop recording, press the 'Q' key.
   - Videos are saved in AVI format in the default directory.

5. **Camera Capture**:
   - Press the 'S' key to capture a screenshot.
   - Captured images are saved in PNG format in the default directory.

   ![Filter Selection](https://github.com/junroun/world_best_camera_ros2/assets/162243442/c5d57908-846d-4435-8e6f-39eeeb84ae9b)

To stop the application, press `Ctrl+C` in the terminal where the app is running.

## Contribution

Contributions to the World Best Camera ROS2 App are welcome. Please feel free to submit pull requests or open issues to discuss proposed changes.
```
