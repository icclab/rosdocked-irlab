#!/usr/bin/env bash

################################################################################
# ZHAW INIT
# Description:  Shell script to create and add the required elements to the
#               CPU image
# Authors:      Leonardo Militano, Mark Straub, Giovanni Toffetti
# Date:         2021-11-08
################################################################################
export CUDA_RELEASE=12.2.0
export IMAGE_NAME=robopaas/rosdocked-humble-k8s:cuda${CUDA_RELEASE}

# Build the docker image
docker build \
  --build-arg BASE_IMAGE=robopaas/rosdocked-humble-base-k8s:cuda${CUDA_RELEASE} \
  --build-arg USER=ros \
  --build-arg shell=$SHELL\
  -t $IMAGE_NAME .
