#!/bin/bash
nvidia-docker run --init --name=ros-gpu --rm -it -e DISPLAY=:1 -v /tmp/.X11-unix/X0:/tmp/.X11-unix/X0:rw -p 443:40001 robopaas/rosdocked-noetic-workspace-included-gpu:latest
