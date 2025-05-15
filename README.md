# 🍃 迷羊智能复习助手

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.2-green)
![Docker](https://img.shields.io/badge/Docker-24.0.6-important)

一个基于RAG技术、Docker容器化部署的智能复习助手，整合知识库检索与大模型问答功能。

## 📌 项目声明
- 本项目为**个人学习用途**开发，仅供技术研究参考
- **禁止任何形式的商业使用**，包括但不限于：
  - 直接售卖本系统或修改版本
  - 作为商业产品/服务的组成部分
  - 用于盈利性培训、咨询等场景
- 使用者需承诺：
  - 不将本项目用于任何盈利目的
  - 不将项目成果用于学术不端行为
  - 不得逆向工程破解系统核心逻辑
- 模型使用遵循[Apache 2.0许可证](LICENSE)的非商业条款

## 🚀 核心功能
- 支持PDF/DOCX/TXT格式文档上传
- 基于Milvus的语义检索增强（RAG）
- ChatGLM3-6B大模型智能问答
- 容器化一键部署（Docker Compose）
- 响应式前端界面

## 🛠️ 技术栈
| 组件         | 技术选型                     |
|--------------|------------------------------|
| 前端         | HTML5 + CSS3 + Vanilla JS    |
| 后端         | Flask + Gunicorn             |
| 向量数据库   | Milvus 2.3                   |
| 大模型服务   | Ollama + ChatGLM3-6B         |
| 部署方案     | Docker + Nginx               |

## 🖥️ 本地部署指南

### 环境要求
- NVIDIA GPU（≥16GB显存）
- Docker 24.0+
- Docker Compose 2.20+

### 三步快速启动
```bash
# 1. 克隆仓库
git clone https://github.com/Yao-guanzi/MiYang_AI_helper

# 2. 进入项目目录
cd MiYang_AI_helper

# 3. 启动服务（自动构建镜像）
docker-compose up -d --build

# 4. 加载模型（关键步骤！）
docker exec -it ollama ollama pull chatglm3