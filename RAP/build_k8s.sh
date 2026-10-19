#!/usr/bin/env bash
# Get this script's path
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd`
popd > /dev/null

. "${SCRIPTPATH}/../images.env"
export IMAGE_NAME=${RAP_IMAGE}

# Build the docker image
docker build \
  --build-arg BASE_IMAGE=${K8S_IMAGE} \
  -t "$IMAGE_NAME" "$SCRIPTPATH"
