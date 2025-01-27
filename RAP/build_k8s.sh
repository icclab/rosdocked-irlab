#!/usr/bin/env bash
export IMAGE_NAME=robopaas/rap-jazzy:cuda12.5.0
#robopaas/rap-lab-intro-k8s

# Build the docker image
docker build \
  --build-arg BASE_IMAGE=robopaas/rosdocked-jazzy-k8s:cuda12.5.0 \
  --build-arg home=/home/ros \
  --build-arg workspace=/home/ros \
  --build-arg shell=$SHELL\
  -t $IMAGE_NAME .
