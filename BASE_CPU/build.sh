#!/usr/bin/env bash

################################################################################
# ZHAW INIT
# Description:  Dockerfile to create the Base CPU Docker image
# Authors:      Leonardo Militano, Mark Straub, Giovanni Toffetti
# Date:         2021-11-08
################################################################################

# Get this script's path
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd`
popd > /dev/null

. "${SCRIPTPATH}/../images.env"
export IMAGE_NAME=${BASE_CPU_IMAGE}

# Update latest base image
docker pull ghcr.io/sloretz/ros:${ROS_DISTRO}-desktop-full

# NOTE: --no-cache was removed. `docker pull` above already refreshes the base
# image, so a full uncached rebuild every run only cost build time. Set
# NO_CACHE=1 to force one.
# NOTE: `--allow network.host` was removed too: it is a buildx entitlement flag
# and does nothing without a matching `RUN --network=host` in the Dockerfile.
docker build \
  ${NO_CACHE:+--no-cache} \
  --build-arg USER=ros \
  --build-arg uid=$UID\
  --build-arg home=/home/ros \
  --build-arg workspace=/home/ros \
  --build-arg shell=$SHELL\
  -t $IMAGE_NAME .
