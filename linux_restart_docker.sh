#!/bin/bash

# 重启名为 qfnu-login-webserver 的容器
docker restart qfnu-login-webserver

# 检查容器是否成功重启
if [ $? -ne 0 ]; then
    echo "Docker container failed to restart!"
    exit 1
fi

echo "Docker container has been restarted successfully."
