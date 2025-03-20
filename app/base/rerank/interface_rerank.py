import time
# import pydantic
# from bson import ObjectId
# pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str
from . import router,namespace
from fastapi import Depends
from pydantic import BaseModel,Field
from typing import Optional,List
import requests
from fastapi import FastAPI, HTTPException
from app.base.test import logger
from app.base.utils.user_decorator import validate_user_token_permission
from .reranker_model import reranker


class QueryRequest(BaseModel):
    # model:str = Field("", description="人员姓名")
    query: str
    texts: List[str] = Field([], description="需要进行筛选的texts")


@router.post('/api/rerank',tags=namespace,name="大模型测试接口",dependencies=[Depends(validate_user_token_permission)],
             response_description="""{}"""
            )
async def call_rerank(request: QueryRequest):
    """
    接收 query 并调用rerank模型
    """
    query = request.query
    texts = request.texts
    ret = reranker.similarity(query= query,texts=texts)
    print(type(ret))
    print(ret)
    print(ret[0].tolist())
    return {
        "code":0,
        "data":ret[0].tolist()
    }

    


