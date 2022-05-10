#!/usr/bin/env bash
export ROS_DISTRO=foxy
nvidia-docker run --init --name=ros-k8s-ros2 --rm -it -p 80:8080 robopaas/rosdocked-${ROS_DISTRO}-k8s:latest

