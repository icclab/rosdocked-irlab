#!/usr/bin/env bash
docker run --init --name=ros-k8s --rm -it -p 8080 robopaas/rosdocked-humble-k8s:latest

