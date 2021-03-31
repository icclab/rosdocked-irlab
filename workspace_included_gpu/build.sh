#!/usr/bin/env bash
export IMAGE_NAME=robopaas/rosdocked-kinetic-workspace-included-gpu:labs

# Get this script's path
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd`
popd > /dev/null

# Build the docker image
docker build --no-cache \
  --build-arg USER=$USER\
  --build-arg uid=$UID\
  --build-arg HOME=/home/ros \
  --build-arg WORKSPACE=/home/ros \
  --build-arg shell=$SHELL\
  -t $IMAGE_NAME .
