# Stage 1: Build stage
FROM python:3.10-slim AS builder

WORKDIR /app

# Create and activate virtual environment
RUN python -m venv /opt/venvs
ENV PATH="/opt/venvs/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 使用官方 Python 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# Copy only the virtual environment from the builder image
COPY --from=builder /opt/venvs /app/venvs

# Activate the virtual environment
ENV PATH="/app/venvs/bin:$PATH"

# 复制当前目录内容到容器中的 /app 目录
COPY . /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 运行应用
CMD ["python", "main.py"]