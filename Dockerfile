#FROM ros:kinetic
FROM osrf/ros:melodic-desktop-full-bionic

# Arguments
ARG user
ARG uid
ARG home
ARG workspace
ARG shell

# Basic Utilities
RUN apt-get -y update && apt-get install -y zsh screen tree sudo ssh

