#!/usr/bin/env bash

################################################################################
# ZHAW INIT
# Description:  Shell script to create and add the Mahroboter project elements
#               to the CPU image
# Authors:      Leonardo Militano, Mark Straub, Giovanni Toffetti, Stanislaw Januszko
# Date:         2021-11-08
################################################################################

# Check if GITHUB_TOKEN (github.zhaw.ch) is provided
if [ $# -eq 0 ]; then
    echo "Error: Please provide the GitHub token as an argument"
    echo "Usage: $0 <GITHUB_TOKEN>"
    exit 1
fi

# Store the first argument as the GitHub token
export GITHUB_TOKEN=$1
export IMAGE_NAME=robopaas/rosdocked-jazzy-cpu-mahroboter:latest

# Build the docker image
docker build \
  --build-arg BASE_IMAGE=robopaas/rosdocked-jazzy-base-cpu:latest \
  --build-arg USER=ros \
  --build-arg home=/home/ros \
  --build-arg workspace=/home/ros \
  --build-arg shell=$SHELL \
  --build-arg GITHUB_TOKEN=$GITHUB_TOKEN \
  -t $IMAGE_NAME .