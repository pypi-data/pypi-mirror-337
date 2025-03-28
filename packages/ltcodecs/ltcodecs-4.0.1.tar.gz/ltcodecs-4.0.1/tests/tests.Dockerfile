FROM ros:noetic-ros-core

# install ros package
RUN apt-get update && apt-get upgrade -y
RUN apt install python3-pip git ros-noetic-dynamic-reconfigure -y
RUN pip install -U pytest pytest-cov