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
from fastapi.responses import StreamingResponse
from app.base.test import logger
from app.base.utils.user_decorator import validate_user_token_permission
import datetime
import json
import aiohttp

class PromptRequest(BaseModel):

    prompt: str
    options:dict=Field({})


@router.post('/api/generate',tags=namespace,name="大模型测试接口",dependencies=[Depends(validate_user_token_permission)],
             response_description="""{}"""
            )
async def call_ollama(request: PromptRequest):
    """
    接收 prompt 并调用 Ollama 本地模型
    """
    print(datetime.datetime.now())
    url = "http://localhost:11434/api/generate"  # Ollama API 地址
    payload = {"model": "deepseek-r1:14b", "prompt": request.prompt,"options":request.options, "stream":False} 

    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

class Message(BaseModel):
    role: str
    content: str
# 定义请求体格式
class ChatRequest(BaseModel):
    # model: str
    messages: List[Message]
    options:dict=Field({})

@router.post('/api/chat',tags=namespace,name="大模型测试接口",dependencies=[Depends(validate_user_token_permission)],
             response_description="""{}"""
            )
async def chat_with_ollama(request: ChatRequest):
    """
    代理请求到 Ollama 的 /api/chat 接口
    """
    url = "http://localhost:11434/api/chat"  # Ollama API 地址
    payload = {"model": "deepseek-r1:14b", "messages": [msg.dict() for msg in request.messages],"stream":False}

    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/api/generate_streamly",tags=namespace,name="大模型测试接口",dependencies=[Depends(validate_user_token_permission)],
             response_description="""{}""")
async def generate_streamly(request: PromptRequest):
    """
    接收 prompt 并调用 Ollama 本地模型
    """
    print(datetime.datetime.now())
    url = "http://localhost:11434/api/generate"  # Ollama API 地址
    payload = {"model": "deepseek-r1:14b", "prompt": request.prompt,"options":request.options,"stream":True} 

    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
    try:
        
        # 使用 aiohttp 进行异步 HTTP 请求
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    raise HTTPException(status_code=response.status, detail=await response.text())

                async def event_stream():
                    async for line in response.content:
                        decoded_line = line.decode('utf-8').strip()
                        if decoded_line:
                            print(datetime.datetime.now(), "::", decoded_line)
                            yield json.dumps(json.loads(decoded_line)) + "\n"

                # 返回异步生成器，适用于 async
                return StreamingResponse(event_stream(), media_type="application/json")

    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))