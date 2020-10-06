#!/usr/bin/env bash
export IMAGE_NAME=robopaas/rosdocked-irlab-ws-novnc:latest

set -e

docker run\
  -h `hostname` \
  -p 8443:443 \
  --device=/dev/video0\
  --device=/dev/dri\
  -e SHELL\
  -e DISPLAY\
  -e DOCKER=1\
  -it $IMAGE_NAME $SHELL
