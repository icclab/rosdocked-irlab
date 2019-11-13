#!/usr/bin/env bash
export IMAGE_NAME=robopaas/rosdocked-melodic-gazebo:latest

# Get this script's path
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd`
popd > /dev/null

set -e

# Run the container with shared X11
#   --device=/dev/duo1:/dev/duo1\
docker run\
  -h `hostname` \
  -v "$SCRIPTPATH/notebooks:/home/ros/notebooks:rw" \
  --privileged\
  --net=host\
  --device=/dev/video0\
  --device=/dev/video1\
  --device=/dev/video2\
  --device=/dev/video3\
  --device=/dev/dri\
  -e SHELL\
  -e DISPLAY\
  -e DOCKER=1\
  -v "/tmp/.X11-unix:/tmp/.X11-unix:rw"\
  -it $IMAGE_NAME $SHELL
