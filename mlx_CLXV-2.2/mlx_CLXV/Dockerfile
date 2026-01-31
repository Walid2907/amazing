FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libvulkan-dev \
    libxcb1-dev \
    libxcb-keysyms1-dev \
    zlib1g-dev \
    libbsd-dev \
    clang \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
