#!/usr/bin/env bash

export IMAGE_NAME=robopaas/rosdocked-noetic-cpu:latest

# Run the container with shared X11
#   --device=/dev/duo1:/dev/duo1\
# remove device mapping if docker complains

# Get this script's path
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd`
popd > /dev/null

set -e

  docker run\
  -h `hostname` \
  --privileged \
  --net=host \
  --device=/dev/dri \
  --device=/dev/video2 \
  --device=/dev/video3 \
  --device=/dev/video4 \
  --device=/dev/video5 \
  --device=/dev/video6 \
  --device=/dev/video7 \
  -e SHELL \
  -e DISPLAY \
  -e DOCKER=1 \
  -v "/tmp/.X11-unix:/tmp/.X11-unix:rw" \
  -v $PWD:/home/ros/catkin_ws/src/rap_challenge \
  -it $IMAGE_NAME $SHELL
