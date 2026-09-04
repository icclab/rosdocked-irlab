#!/usr/bin/env bash

################################################################################
# ZHAW INIT
# Description:  Shell script to create the Base GPU Docker image
# Authors:      Leonardo Militano, Mark Straub, Giovanni Toffetti
# Date:         2021-11-08
################################################################################
# Get this script's path
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd`
popd > /dev/null

. "${SCRIPTPATH}/../images.env"
export IMAGE_NAME=${BASE_K8S_IMAGE}

# NOTE: the user/uid/home/workspace build args this used to pass are not declared
# by BASE_K8S/Dockerfile (it hardcodes ENV USER=ros), so they were silently
# ignored. Only NVIDIA_DRIVER_VERSION is actually consumed -- see images.env.
docker build  \
  --build-arg NVIDIA_DRIVER_VERSION=${NVIDIA_DRIVER_VERSION} \
  -t $IMAGE_NAME .
