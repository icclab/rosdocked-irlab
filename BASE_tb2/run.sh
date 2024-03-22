#!/bin/sh
nvidia-docker run -it  --privileged --rm --net host -v "$HOME:$HOME:rw" -v /dev/kobuki:/dev/kobuki -v /dev/lidar:/dev/lidar robopaas/rosdocked-hum-tb2_nephele:latest 
