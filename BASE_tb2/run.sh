#!/bin/sh
nvidia-docker run -it --privileged --net host -v "$HOME:$HOME:rw" robopaas/rosdocked-humble-tb2:latest
