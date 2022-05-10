#!/usr/bin/env bash

################################################################################
# ZHAW INIT
# Description:  Shell script to create and add the required elements to the
#               CPU image
# Authors:      Leonardo Militano, Mark Straub, Giovanni Toffetti
# Date:         2022-05-06
################################################################################
export ROS_DISTRO=foxy
export IMAGE_NAME=robopaas/rosdocked-${ROS_DISTRO}-k8s:latest

# Build the docker image
docker build \
  --no-cache \
  --build-arg BASE_IMAGE=robopaas/rosdocked-${ROS_DISTRO}-base-k8s:latest \
  --build-arg USER=ros \
  --build-arg shell=$SHELL\
  -t $IMAGE_NAME .
