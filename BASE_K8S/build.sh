#!/usr/bin/env bash

################################################################################
# ZHAW INIT
# Description:  Shell script to create the Base GPU Docker image
# Authors:      Leonardo Militano, Mark Straub, Giovanni Toffetti
# Date:         2021-11-08
################################################################################
export ROS_DISTRO=noetic
export IMAGE_NAME=robopaas/rosdocked-${ROS_DISTRO}-base-k8s:11.8.0-devel-ubuntu20.04

# Get this script's path
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd`
popd > /dev/null

# Build the docker image
docker build \
  --build-arg user=user\
  --build-arg uid=$UID\
  --build-arg home=/home/user \
  --build-arg workspace=/home/user \
  --build-arg shell=$SHELL\
  -t $IMAGE_NAME .
