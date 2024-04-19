import os
from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

from tkinter import *
import cv2
import pyautogui
import numpy as np
import threading
from tkinter import messagebox as msgbox
from tkinter import filedialog

def start_gui():
    root = Tk()
#함수 정의 1.녹화 함수
run = False #버튼 누르면 종료 명령


def generate_launch_description():
    param_dir = LaunchConfiguration(
        'param_dir',
        default=os.path.join(
        get_package_share_directory('camera'),
        'param',
        'size.yaml')
        )
    return LaunchDescription(
    [
        DeclareLaunchArgument(
            'param_dir',
            default_value=param_dir
        ),
        Node(
            package='camera',
            executable='camera',
            name='camera12',
            parameters=[param_dir],
            output='screen'),
        Node(
            package='camera',  
            executable='mirror_edge',
            name='mirror_edge',
            output='screen'
        ),
        Node(
            package='camera',  
            executable='bolok',
            name='bolok',
            output='screen'
        ),
        Node(
            package='camera', 
            executable='blur',
            name='blur',
            output='screen'
        ),
        Node(
            package='camera',  
            executable='median',
            name='median',
            output='screen'
        ),
        Node(
            package='camera',  
            executable='rens',
            name='rens',
            output='screen'
        ),
        Node(
            package='camera',  
            executable='Sharpening',
            name='Sharpening',
            output='screen'
        ),
        Node(
            package='camera',  
            executable='record',
            name='record',
            output='screen'
        ),
        ExecuteProcess(
            cmd=['rqt'],
            output='screen'
        )
    ])
    