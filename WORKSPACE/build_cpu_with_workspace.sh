#!/usr/bin/env bash

################################################################################
# ZHAW INIT
# Description:  Shell script to create and add the required elements to the
#               CPU image
# Authors:      Leonardo Militano, Mark Straub, Giovanni Toffetti
# Date:         2021-11-08
################################################################################

# Get this script's path
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd`
popd > /dev/null

. "${SCRIPTPATH}/../images.env"
export IMAGE_NAME=${CPU_IMAGE}

# Build the docker image
docker build \
  --build-arg BASE_IMAGE=${BASE_CPU_IMAGE} \
  --build-arg USER=ros \
  --build-arg uid=$UID \
  --build-arg home=/home/ros \
  --build-arg workspace=/home/ros \
  --build-arg shell=$SHELL\
  -t $IMAGE_NAME .
