#!/usr/bin/env bash
export IMAGE_NAME=robopaas/ros2docked-foxy:latest

# Get this script's path
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd`
popd > /dev/null

# Build the docker image
docker build \
  --build-arg user=$USER\
  --build-arg home=/home/ros \
  --build-arg workspace=/home/ros \
  --build-arg shell=$SHELL\
  --build-arg uid=$UID\
  -t $IMAGE_NAME .

