#!/usr/bin/env bash
nvidia-docker run --init --name=ros-k8s --rm -it -p 8080:8080 robopaas/rosdocked-humble-k8s:cuda12.2.0

