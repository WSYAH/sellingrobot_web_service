"""/
* 模块名:reranker 封装
* 代码描述:
* 作者:uaohan
* 创建时间:2025/2/4 10:40:41
/"""


import numpy as np
from abc import ABC
import threading 
from config import LIGHTEN
from .utils import get_home_cache_dir,truncate, num_tokens_from_string
import os
from huggingface_hub import snapshot_download
import re
import requests

# 实现σ(x)函数
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class Base(ABC):
    def __init__(self, key, model_name):
        pass

    def similarity(self, query: str, texts: list):
        raise NotImplementedError("Please implement encode method!")


class DefaultRerank(Base):
    _model = None
    _model_lock = threading.Lock()

    def __init__(self, key, model_name, **kwargs):
        """
        tips:当然这里的key可以不填,自选的reranker模型不需要填写key
        只是因为复用了embedding的代码，embedding中用到了openai的模型，需要用key，为了代码的统一性，这里也保留了key
        """
        if not LIGHTEN and not DefaultRerank._model:
            import torch
            from FlagEmbedding import FlagReranker
            with DefaultRerank._model_lock:
                if not DefaultRerank._model:
                    try:
                        DefaultRerank._model = FlagReranker(
                            os.path.join(get_home_cache_dir(), re.sub(r"^[a-zA-Z]+/", "", model_name)),
                            use_fp16=torch.cuda.is_available())
                            # use_fp16=False,device=torch.device('cpu'))
                        pass
                    except Exception as e:
                        os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
                        model_dir = snapshot_download(repo_id=model_name,
                                                      local_dir=os.path.join(get_home_cache_dir(),
                                                                             re.sub(r"^[a-zA-Z]+/", "", model_name)),
                                                      local_dir_use_symlinks=False)
                        DefaultRerank._model = FlagReranker(model_dir, use_fp16=torch.cuda.is_available())
        self._model = DefaultRerank._model

    def similarity(self, query: str, texts: list):
        pairs = [(query, truncate(t, 2048)) for t in texts]
        token_count = 0
        for _, t in pairs:
            token_count += num_tokens_from_string(t)
        batch_size = 4096
        res = []
        for i in range(0, len(pairs), batch_size):
            scores = self._model.compute_score(pairs[i:i + batch_size], max_length=2048)
            scores = sigmoid(np.array(scores)).tolist()
            if isinstance(scores, float):
                res.append(scores)
            else:
                res.extend(scores)
        return np.array(res), token_count

def cos_similarity(embedding1,embedding2):
    dot_product = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    cosine_similarity = dot_product / (norm1 * norm2)
    
    return cosine_similarity

class OllamaRerank(Base):
    def __init__(self):
        pass
    def similarity(self, query: str, texts: list):
        url = "http://localhost:11434/api/embed"  # Ollama API 地址

        payload1 = {"model": "deepseek-r1:14b", "input": texts} 

        res1 = requests.post(url,json=payload1)
        embeddings = res1.json()['embeddings']
        
        payload2 = {"model": "deepseek-r1:14b", "input": query} 
        res2 = requests.post(url,json=payload2)
        embedding = res2.json()["embeddings"][0]

        return np.array([cos_similarity(embedding1,embedding) for embedding1 in embeddings]),0


reranker = OllamaRerank()


if __name__ == "__main__":
    import datetime
    start = datetime.datetime.now()
    # if reranker:
    #     del reranker
    texts = [
        "2024大选，特朗普选票领先哈里斯当选美国总统",
        "四年前，乔拜登选票领先特朗普，当选美国总统",
        "提瓦特大陆的鸽子等于两个鸡腿",
        "原神里面的野猪等于两块肉，利用率较低，但是野猪刷新率高弥补了这一点",
        "今天的风真是萧瑟啊"
    ]

    query = "2020年美国大选，谁当选了总统？"
    # reranker = DefaultRerank(None,model_name="BAAI/bge-reranker-v2-m3") 



    print("呦呵呵呵呵")


    ret = reranker.similarity(query, texts)
    print(ret) #(array([7.10363397e-01, 6.38837191e-01, 1.62992067e-05, 1.86962502e-05,3.44702594e-05]), 133)
    
    end = datetime.datetime.now()
    
    print(end - start)
    texts.append("原神，启动！")
    ret = reranker.similarity(query,texts)
    print(ret)
    end2 = datetime.datetime.now()
    print(end2 - end)

    