#!/usr/bin/env bash
export IMAGE_NAME=robopaas/rosdocked-kinetic-gpu:latest

# Get this script's path
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd`
popd > /dev/null

# Build the docker image
nvidia-docker build --no-cache \
  --build-arg user=$USER\
  --build-arg uid=$UID\
  --build-arg home=$HOME\
  --build-arg workspace=$SCRIPTPATH\
  --build-arg shell=$SHELL\
  -t $IMAGE_NAME .
