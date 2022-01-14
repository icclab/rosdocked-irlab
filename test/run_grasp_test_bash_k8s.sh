#!/usr/bin/env bash
export IMAGE=robopaas/rosdocked-noetic-k8s:latest

export CONTAINER_NAME=grasp_test_k8s
echo $CONTAINER_NAME

docker rm -f $CONTAINER_NAME || true

docker run -d -i --rm --name $CONTAINER_NAME $IMAGE  /bin/bash

# TEST #1: testing navigation stack
# test with bash
echo "Testing grasping stack..."
docker exec -i $CONTAINER_NAME ./catkin_ws/src/icclab_summit_xl/.ci/grasp_test_bash.sh
if [[ "$?" == "0" ]] ; then
  echo "Grasping test failed. Check output."
  echo "Removing docker container $CONTAINER_NAME..."
  docker rm -f $CONTAINER_NAME || true
  exit 1
elif [[ "$?" == "1" ]] ; then
  echo "Grasping test succeeded! No issues found."
  echo "Removing docker container $CONTAINER_NAME..."
  docker rm -f $CONTAINER_NAME || true
  exit 0
else
  echo "State of test unknown. Check output."
  echo "Removing docker container $CONTAINER_NAME..."
  docker rm -f $CONTAINER_NAME || true
  exit 1
fi
