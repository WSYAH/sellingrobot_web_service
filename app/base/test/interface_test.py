import time
# import pydantic
# from bson import ObjectId
# pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str
from . import router,namespace
from fastapi import Depends
from pydantic import BaseModel,Field
from typing import Optional


from app.base.test import logger
from app.base.utils.user_decorator import validate_user_token_permission

import datetime 
import requests



from fastapi.responses import StreamingResponse
async def number_generator():
    for i in range(10):
        yield f"数字 {i}\n"
        time.sleep(1)  # 模拟耗时操作

@router.post("/stream",tags=namespace,name="测试接口",dependencies=[Depends(validate_user_token_permission)],
             response_description="""{}""")
async def stream_numbers():
    return StreamingResponse(number_generator(), media_type="text/plain")

class PromptRequest(BaseModel):
    # model:str = Field("", description="人员姓名")
    prompt: str
    options:dict=Field({})



async def stream(prompt):
    print(datetime.datetime.now())
    url = "http://localhost:11434/api/generate"  # Ollama API 地址
    payload = {"model": "deepseek-r1:14b", "prompt": prompt} 
    print("************", flush=True)
    response = requests.post(url, json=payload,stream=True)
    # print("++++++++++++")
    for line in response.iter_lines(decode_unicode=True):
        # print(datetime.datetime.now(),"::",line,flush=True)
        yield line.decode('utf-8')+"\n"

@router.post("/stream2",tags=namespace,name="测试接口",dependencies=[Depends(validate_user_token_permission)],
             response_description="""{}""")
async def test(request:PromptRequest):
    prompt = request.prompt
    return StreamingResponse(stream(prompt), media_type="text/plain")


import httpx
async def stream2(prompt):
    print(datetime.datetime.now(), "请求开始...")
    url = "http://localhost:11434/api/generate"
    payload = {"model": "deepseek-r1:14b", "prompt": prompt}
    flag = False
    changeline = False
    async with httpx.AsyncClient() as client:
        async with client.stream("POST", url, json=payload) as response:
            print(datetime.datetime.now(), "收到响应流...")
            async for line in response.aiter_lines():
                if line:
                    x = line
                    import json
                    print(datetime.datetime.now(), "::",type(x),changeline,json.loads(x)["response"],x,flush=True)
                    # print(type(line),eval(line[2:2])["response"],flush=True)
                    if  flag:
                        if not changeline and "\n\n" == json.loads(x)['response']:
                            changeline = True
                            print("这是一个双换行", flush=True)
                        else:
                            yield line + "\n"  # 确保每行数据立即返回

                    if "</think>" in json.loads(x)['response']:
                        flag = True
                    

@router.post("/stream3")
async def test(request: dict):
    prompt = request.get("prompt", "")
    return StreamingResponse(stream2(prompt), media_type="text/plain")