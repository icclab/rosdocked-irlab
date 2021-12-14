#!/usr/bin/env bash
nvidia-docker run --init --name=ros-k8s --rm -it -p 80:8080 robopaas/rosdocked-noetic-k8s:latest

