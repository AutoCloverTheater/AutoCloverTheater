# 使用官方 Python 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录内容到容器中的 /app 目录
COPY . /app

RUN chmod +x /app/start.sh

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    tesseract-ocr \
    android-tools-adb \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*
# 运行应用
CMD ["/bin/sh", "-x", "/app/start.sh"]