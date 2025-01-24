#!/usr/bin/env bash

IMAGE=robopaas/rosdocked-jazzy-cpu:latest
# Get this script's path
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd`
popd > /dev/null

set -e

# enable xhost access for: quick and unsafe
# xhost +SI:localuser:root

# Run the container with shared X11
docker run\
  -h localhost\
  --net=host --ipc=host --pid=host \
  --privileged \
  -e QT_QPA_PLATFORM=xcb \
  -e SHELL\
  -e DISPLAY\
  -e DOCKER=1\
  -v "$HOME:$HOME:rw"\
  -v "/tmp/.X11-unix:/tmp/.X11-unix:rw"\
  -it $IMAGE $SHELL
