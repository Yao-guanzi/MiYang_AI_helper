# 使用 Python 3.10
FROM python:3.10

# 设置工作目录
WORKDIR /app

# 安装必要的依赖（增加CUDA支持）
RUN apt-get update && \
    apt-get install -y gcc python3-dev git-lfs libgl1 && \
    rm -rf /var/lib/apt/lists/*

# 安装 git-lfs 并初始化
RUN git lfs install

# 创建模型缓存目录
RUN mkdir -p /app/models

# 复制 requirements.txt 文件并安装依赖
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 安装PyTorch（根据实际CUDA版本选择）
RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu118

# 复制项目代码到镜像中
COPY . .

# 下载模型
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-base-zh-v1.5', cache_folder='/app/models')"
RUN curl -L https://huggingface.co/THUDM/chatglm3-6b/resolve/main/model.safetensors?download=true -o /app/models/chatglm3-6b.safetensors

# 设置环境变量
ENV PYTHONPATH=/app

ENV LANG C.UTF-8
RUN apt-get install -y fonts-wqy-zenhei

# 指定容器启动时运行的命令
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "backend.app:app"]