#!/usr/bin/env bash

################################################################################
# ZHAW INIT
# Description:  Shell script to create and add the required elements to the
#               CPU image
# Authors:      Leonardo Militano, Mark Straub, Giovanni Toffetti
# Date:         2021-11-08
################################################################################

export IMAGE_NAME=robopaas/rosdocked-noetic-k8s:latest

# Build the docker image
docker build \
  --build-arg BASE_IMAGE=robopaas/rosdocked-noetic-base-k8s:latest \
  --build-arg USER=ros \
  --build-arg shell=$SHELL\
  -t $IMAGE_NAME .
