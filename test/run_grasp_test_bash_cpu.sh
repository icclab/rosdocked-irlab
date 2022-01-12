#!/usr/bin/env bash
export IMAGE=robopaas/rosdocked-noetic-cpu:latest

docker run -d -i $IMAGE /bin/bash

export CONTAINER_NAME=$(docker ps --latest --format "{{.Names}}")
echo $CONTAINER_NAME

# TEST #1: testing navigation stack
# test with bash
echo "Testing navigation stack..."
docker exec -i $CONTAINER_NAME ./catkin_ws/src/icclab_summit_xl/.ci/grasp_test_bash.sh
if [[ "$?" == "0" ]] ; then
  echo "Grasping test failed. Check output."
  echo "Killing docker container $CONTAINER_NAME..."
  docker kill $CONTAINER_NAME
  docker rm $CONTAINER_NAME
  exit 1
elif [[ "$?" == "1" ]] ; then
  echo "Grasping test succeeded! No issues found."
  echo "Killing docker container $CONTAINER_NAME..."
  docker kill $CONTAINER_NAME
  docker rm $CONTAINER_NAME
  exit 0
else
  echo "State of test unknown. Check output."
  echo "Killing docker container $CONTAINER_NAME..."
  docker kill $CONTAINER_NAME
  docker rm $CONTAINER_NAME
  exit 1
fi
