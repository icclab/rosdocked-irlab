#!/usr/bin/env bash
export IMAGE_NAME=robopaas/rosdocked-irlab-ws-novnc:latest

set -e


docker run\
  -h `hostname` \
  --device=/dev/video0\
  --device=/dev/video1\
  --device=/dev/video2\
  --device=/dev/video3\
  --device=/dev/dri\
  -e SHELL\
  -e DISPLAY\
  -e DOCKER=1\
  -it $IMAGE_NAME $SHELL
