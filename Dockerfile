LABEL authors="yangfeng"

# 使用官方 Python 基础镜像（推荐 Alpine 版本减小体积）
FROM python:3.10-alpine

# 设置工作目录
WORKDIR /app

# 复制依赖列表和代码到容器
COPY requirements.txt .
COPY src/app ./app

# 安装依赖（使用阿里云镜像加速，按需替换）
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 可选：非 root 用户运行（增强安全性）
RUN adduser -D myuser && chown -R myuser /app
USER myuser

# 暴露端口（如果应用需要）
EXPOSE 8000

# 启动命令（根据实际入口文件修改）
CMD ["python", "./app/main.py"]