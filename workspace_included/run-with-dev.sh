#!/usr/bin/env bash
export TAG=latest
export BASE_IMAGE=robopaas/rosdocked-kinetic-workspace-included
export IMAGE_NAME=$BASE_IMAGE:$TAG

local_image=$(docker images | grep $BASE_IMAGE | grep $TAG)
if ! [[ -z "$local_image" ]] ; then
  read -p "Do you wish to delete local $IMAGE_NAME image and pull an updated version? (y/n) " yn
  case $yn in
    [Yy]* ) echo "Deleting $IMAGE_NAME locally"; docker rmi -f $IMAGE_NAME;;
   [Nn]* ) echo "Using local image $IMAGE_NAME";;
  esac
fi

set -e

# Run the container with shared X11
#   --device=/dev/duo1:/dev/duo1\
docker run\
  -h `hostname`\
  --name irlab\
  --rm\
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
