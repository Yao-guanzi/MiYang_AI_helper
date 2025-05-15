from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Milvus
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import requests


class KnowledgeProcessor:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-zh-v1.5")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", "。", "？", "！", "……"]
        )
        self.vector_db = None

    def process_document(self, file_path):
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith('.docx'):
            loader = Docx2txtLoader(file_path)
        elif file_path.endswith('.txt'):
            loader = TextLoader(file_path)
        else:
            raise ValueError("Unsupported file type")

        documents = loader.load()
        texts = self.text_splitter.split_documents(documents)

        self.vector_db = Milvus.from_documents(
            texts,
            self.embeddings,
            connection_args={"host": os.getenv("MILVUS_HOST"), "port": "19530"},
            collection_name="knowledge_base"
        )

    def retrieve_context(self, question):
        if not self.vector_db:
            return "没有可用的知识库"

        docs = self.vector_db.similarity_search(question, k=3)
        return "\n".join([doc.page_content for doc in docs])

    def generate_answer(self, question, context):
        try:
            prompt = f"<|system|>\n你是一个智能复习助手，请根据上下文用中文回答问题\n上下文：{context}\n<|user|>\n{question}\n<|assistant|>\n"

            response = requests.post(
                "http://ollama:11434/api/generate",
                json={
                    "model": "chatglm3",
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "num_predict": 500,
                        "stop": ["<|user|>", "<|observation|>"]
                    }
                },
                timeout=60
            )

            return response.json().get("response", "未能生成回答").strip()
        except Exception as e:
            return f"生成答案时出现异常：{str(e)}"