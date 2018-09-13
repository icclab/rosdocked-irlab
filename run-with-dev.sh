#!/usr/bin/env bash

# Check args
if [ "$#" -ne 1 ]; then
  echo "usage: ./run.sh IMAGE_NAME"
  return 1
fi

# Get this script's path
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd`
popd > /dev/null

set -e

# Run the container with shared X11
#   --device=/dev/duo1:/dev/duo1\
docker run\
  -h localhost\
  --net=host\
  --device=/dev/video0:/dev/video0\
  --device=/dev/dri\
  -e SHELL\
  -e DISPLAY\
  -e DOCKER=1\
  -v "$HOME:$HOME:rw"\
  -v "/tmp/.X11-unix:/tmp/.X11-unix:rw"\
  -v "/lib/modules/4.14.0-041400-generic:/lib/modules/4.14.0-041400-generic:rw"\
  -it $1 $SHELL
