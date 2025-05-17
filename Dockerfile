# 基础镜像（明确指定Python 3.10）
FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

# 系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git-lfs \
    libgl1 \
    fonts-wqy-zenhei \
    python3.10-dev \
    && rm -rf /var/lib/apt/lists/*

# 在Dockerfile中添加模型路径映射
ENV MODEL_PATH=/app/models/chatglm3-6b

# 配置Python环境
RUN ln -sf /usr/bin/python3.10 /usr/bin/python && \
    ln -sf /usr/bin/python3.10 /usr/bin/python3

# 环境变量
ENV LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Shanghai \
    PYTHONPATH=/app

# 安装依赖
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 复制项目文件
COPY . .

# 下载嵌入模型
RUN python -c "from sentence_transformers import SentenceTransformer; \
    SentenceTransformer('BAAI/bge-base-zh-v1.5', cache_folder='/app/models')"

# 端口暴露
EXPOSE 5000

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "300", "backend.app:app"]