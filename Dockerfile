FROM python:3.10 AS builder

WORKDIR /app

# 复制当前目录内容到容器中的 /app 目录
COPY requirements.txt .

RUN python -m venv venvs && pip install --upgrade pip

# 使用官方 Python 镜像
FROM python:3.10

# 设置工作目录
WORKDIR /app

# 复制当前目录内容到容器中的 /app 目录
COPY . /app

COPY --from=builder /app/venvs /app/venvs

# 激活虚拟环境并安装依赖
ENV PATH="/app/venvs/bin:$PATH"

RUN pip install requests

#RUN apt-get update && apt-get install -y \
#    libgl1-mesa-glx \
#    libglib2.0-0 \
#    && rm -rf /var/lib/apt/lists/* && python -m venv  /app/venvs
# 运行应用
CMD ["python", "install.py"]