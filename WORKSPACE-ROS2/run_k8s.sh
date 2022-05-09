#!/usr/bin/env bash
# nvidia-docker run --init --name=ros-k8s-ros2 --rm -it -p 80:8080 robopaas/rosdocked-ros2-base-k8s:latest
export ROS_DISTRO=foxy
# docker run --init --name=ros-k8s-ros2 --rm -it -p 80:8080 robopaas/rosdocked-${ROS_DISTRO}-base-k8s:latest
# docker run --init --name=ros-k8s-ros2 --rm -it -p 80:8080 robopaas/rosdocked-${ROS_DISTRO}-k8s:latest
docker run --init --name=ros-k8s-ros2 --rm -it -p 80:8080 test

