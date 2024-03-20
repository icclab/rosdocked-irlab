#!/bin/sh
nvidia-docker run -it --entrypoint start_tb2_nomap.sh --privileged --rm --net host -v "$HOME:$HOME:rw" -v /dev/kobuki:/dev/kobuki -v /dev/lidar:/dev/lidar robopaas/rosdocked-hum-tb2_zenoh:latest 
#nvidia-docker run -it --privileged --net host -v "$HOME:$HOME:rw" robopaas/rosdocked-humble-tb2:latest
