#!/usr/bin/env bash
export TAG=latest
export BASE_IMAGE=robopaas/rosdocked-kinetic-gpu-workspace-included
#export BASE_IMAGE=robopaas/rosdocked-kinetic-workspace-included-gpu-manual
export IMAGE_NAME=$BASE_IMAGE:$TAG

set -e

nvidia-docker run --privileged --net=host -h localhost -e PATH=/usr/local/cuda/bin/:$PATH -e LD_LIBRARY_PATH=/usr/local/cuda/lib64 -e NVIDIA_VISIBLE_DEVICES=all -e NVIDIA_DRIVER_CAPABILITIES=compute,utility -v /usr/local/cuda-10.2:/usr/local/cuda -it $IMAGE_NAME $SHELL
