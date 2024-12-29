#!/bin/bash

# 设置项目名称和镜像名称
PROJECT_NAME="qfnu-login-webserver"
IMAGE_NAME="qfnu-login-webserver"

# 构建Docker镜像
echo "Building Docker image..."
docker build -t $IMAGE_NAME .

# 检查构建是否成功
if [ $? -ne 0 ]; then
    echo "Docker image build failed!"
    exit 1
fi

# 运行Docker容器
echo "Running Docker container..."
docker run -d -p 5000:5000 -v "/${PWD//\\//}":/app --name $PROJECT_NAME $IMAGE_NAME

# 检查容器是否成功启动
if [ $? -ne 0 ]; then
    echo "Docker container failed to start!"
    exit 1
fi

echo "Docker container is running. Access the application at http://localhost:5000"
