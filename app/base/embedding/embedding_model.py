
import sys

from abc import ABC
import threading
from .utils import get_home_cache_dir,LIGHTEN,truncate,num_tokens_from_string
import os
from huggingface_hub import snapshot_download
import re
import numpy as np
from openai import OpenAI
from config import *
import requests
import time
from threading import Timer
import torch

TIMEOUT=600

# 首先定义一个抽象基类，这样无论使用多少个embedding模型，都可以继承这个类，统一管理
class Base(ABC):
    def __init__(self, key, model_name):
        pass
    """embedding模型一般embedding的维度为1024维，不需要自己控制"""
    def encode(self, texts: list, batch_size=32):
        raise NotImplementedError("Please implement encode method!")

    def encode_queries(self, text: str):
        raise NotImplementedError("Please implement encode method!")

import functools
def singleton_factory(cls):
    """工厂函数，确保类只被初始化一次"""
    instances = {}
    @functools.wraps(cls) 
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@singleton_factory 
class DefaultEmbedding(Base):
    _model = None
    _model_lock = threading.Lock()
    def __init__(self, key, model_name, **kwargs):

        if not LIGHTEN and not DefaultEmbedding._model:
            with DefaultEmbedding._model_lock:
                from FlagEmbedding import FlagModel
                import torch
                if not DefaultEmbedding._model:
                    try:
                        DefaultEmbedding._model = FlagModel(os.path.join(get_home_cache_dir(), re.sub(r"^[a-zA-Z]+/", "", model_name)),
                                                            query_instruction_for_retrieval="为这个句子生成表示以用于检索相关文章：",
                                                            use_fp16=torch.cuda.is_available())
                    except Exception as e:
                        os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
                        model_dir = snapshot_download(repo_id="BAAI/bge-large-zh-v1.5",
                                                      local_dir=os.path.join(get_home_cache_dir(), re.sub(r"^[a-zA-Z]+/", "", model_name)),
                                                      local_dir_use_symlinks=False)
                        DefaultEmbedding._model = FlagModel(model_dir,
                                                            query_instruction_for_retrieval="为这个句子生成表示以用于检索相关文章：",
                                                            use_fp16=torch.cuda.is_available())
        self._model = DefaultEmbedding._model
        # 配置超时下机,避免长时间占用GPU
        # self.last_used = time.time()
        # self.timer = Timer(TIMEOUT, self.release_model)
        # self.timer.start()


    def encode(self, texts: list, batch_size=32):
        # self.last_used = time.time()
        texts = [truncate(t, 2048) for t in texts]
        token_count = 0
        for t in texts:
            token_count += num_tokens_from_string(t)
        res = []
        for i in range(0, len(texts), batch_size):
            res.extend(self._model.encode(texts[i:i + batch_size]).tolist())
        return np.array(res), token_count

    def encode_queries(self, text: str):
        # self.last_used = time.time()
        token_count = num_tokens_from_string(text)
        return self._model.encode_queries([text]).tolist()[0], token_count
    
    def release_model(self):
        """如果模型长时间未使用，就释放GPU资源，不然的话，就可能会不断的占用GPU"""
        print("Releasing GPU model due to inactivity...")
        del self.model
        torch.cuda.empty_cache()


class OpenAIEmbed(Base):
    def __init__(self, key, model_name="text-embedding-ada-002",
                 base_url=OPENAI_BASE):
        if not base_url:
            base_url = "https://api.openai.com/v1"
        self.client = OpenAI(api_key=key, base_url=base_url)
        self.model_name = model_name

    def encode(self, texts: list, batch_size=32):
        texts = [truncate(t, 8191) for t in texts]
        res = self.client.embeddings.create(input=texts,
                                            model=self.model_name)
        return np.array([d.embedding for d in res.data]
                        ), res.usage.total_tokens

    def encode_queries(self, text):
        res = self.client.embeddings.create(input=[truncate(text, 8191)],
                                            model=self.model_name)
        return np.array(res.data[0].embedding), res.usage.total_tokens
    
class OllamaEmbed(Base):
    def __init__(self, key=None, model_name="deepseek-r1:14b",
                 base_url=None):
        if not base_url:
            base_url = "http://localhost:11434/api/generate"

    def encode(self, texts: list, batch_size=32):
        url = "http://localhost:11434/api/embed"  # Ollama API 地址
        payload = {"model": "deepseek-r1:14b", "input": texts} 

        response = requests.post(url,json=payload)
        return response.json()['embeddings'], 0

    def encode_query(self, text):
        url = "http://localhost:11434/api/embed"  # Ollama API 地址
        payload = {"model": "deepseek-r1:14b", "input": text} 

        response = requests.post(url,json=payload)
        return response.json()

def test1():
    # embeddingmodel = OpenAIEmbed(OPENAI_KEY,model_name=OPENAI_EMBED, base_url=OPENAI_BASE) # 已经调好了，可以正常使用
    embeddingmodel = DefaultEmbedding(None,model_name="BAAI/bge-large-zh-v1.5") # 这个也行了
    texts_need_embedding = ["hello world", "你好，世界","哈哈哈哈哈哈哈哈哈","2024美国大选结果出炉，特朗普领先哈里斯当选总统"]
    embed_ret = embeddingmodel.encode(texts_need_embedding)
    print(embed_ret)
    
embeddingmodel = OllamaEmbed()
if __name__ == '__main__':
    
    res = embeddingmodel.encode_query("你好")
    print(res["embedding"])

