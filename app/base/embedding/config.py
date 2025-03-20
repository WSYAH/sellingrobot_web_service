
import os

PROJECT_BASE_DIR = "/root/yah/ragflow"

OPENAI_MODEL = "gpt-4o-mini"
OPENAI_KEY = ''
OPENAI_BASE=''
OPENAI_EMBED='text-embedding-ada-002'


ZHIPUAI_KEY = ""
ZHIPUAI_MODEL = "glm-4-flash"


CACHE_NAME = ".model" # 这里存储embedding模型和reranker模型的缓存
LIGHTEN = int(os.environ.get('LIGHTEN', "0"))

EMBEDING_MODEL = "BAAI/bge-large-zh-v1.5" # embedding模型
RERANKER_MODEL = "BAAI/bge-reranker-v2-m3" # reranker模型,ai_ops严选，他们队伍说是最好用的


IMG_BASE64_PREFIX = 'data:image/png;base64,'

ES_HOST = "localhost:1200"
ES_USERNAME = "elastic"
ES_PASSWORD = " infini_rag_flow"