#!/usr/bin/env bash

################################################################################
# ZHAW INIT
# Description:  Shell script to create the Base GPU Docker image
# Authors:      Leonardo Militano, Mark Straub, Giovanni Toffetti
# Date:         2021-11-08
################################################################################
export ROS_DISTRO=humble
export CUDA_RELEASE=12.2.0
export IMAGE_NAME=robopaas/rosdocked-${ROS_DISTRO}-base-k8s:cuda${CUDA_RELEASE}

# Get this script's path
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd`
popd > /dev/null

# Build the docker image
docker build --no-cache \
  --build-arg user=user\
  --build-arg uid=$UID\
  --build-arg home=/home/user \
  --build-arg workspace=/home/user \
  --build-arg shell=$SHELL\
  --build-arg CUDA_RELEASE=${CUDA_RELEASE}\
  -t $IMAGE_NAME .
