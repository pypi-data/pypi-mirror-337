FROM ros:noetic-ros-core

RUN apt-get update \
    && apt-get upgrade -y \
    && apt install -y \
        python3-pip git

RUN pip install pytest
