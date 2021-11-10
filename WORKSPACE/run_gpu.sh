#!/usr/bin/env bash
nvidia-docker run --init --name=ros-gpu --rm -it -e DISPLAY=:1 -v /tmp/.X11-unix/X0:/tmp/.X11-unix/X0:rw --privileged --net host robopaas/rosdocked-noetic-gpu:latest

