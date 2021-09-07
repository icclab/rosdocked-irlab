#!/usr/bin/env bash
export IMAGE_NAME=seanrmurphy/simple-ros-container

# Get this script's path
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd`
popd > /dev/null


# Build the docker image
docker build \
  --build-arg user=ros\
  --build-arg uid=1001\
  --build-arg home=/home/ros \
  --build-arg workspace=/home/ros \
  --build-arg shell=$SHELL\
  -t $IMAGE_NAME .
