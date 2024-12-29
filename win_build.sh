#!/bin/bash

# 设置镜像名称
IMAGE_NAME="qfnu-login-webserver"

# 构建Docker镜像
echo "Building Docker image..."
docker build -t $IMAGE_NAME .

# 检查构建是否成功
if [ $? -ne 0 ]; then
    echo "Docker image build failed!"
    exit 1
fi

echo "Docker image built successfully." 