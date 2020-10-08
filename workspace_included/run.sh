#!/usr/bin/env bash
export IMAGE_NAME=robopaas/rosdocked-irlab-ws-novnc:latest

set -e

docker run\
  -p 8443:443 \
  -e SHELL\
  -e DOCKER=1\
  -it $IMAGE_NAME $SHELL
