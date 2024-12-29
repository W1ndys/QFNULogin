# 使用官方Python基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器中
COPY . /app

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露应用运行的端口
EXPOSE 5000

# 允许python文件运行
CMD ["python", "webserver.py"]

