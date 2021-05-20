#!/usr/bin/env bash
export IMAGE_NAME=robopaas/rap-lab-foxy-gpu:rap20210520

# Build the docker image
docker build \
  --build-arg BASE_IMAGE=robopaas/rosdocked-foxy-gpu:labs \
  --build-arg home=/home/ros \
  --build-arg workspace=/home/ros \
  --build-arg shell=$SHELL\
  -t $IMAGE_NAME .

