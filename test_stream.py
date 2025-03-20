

from fastapi import FastAPI, HTTPException
import requests
prompt = "你好"
gen_conf = {
        "temperature": 0.7,
        "top_p":0.7,
    }
options = gen_conf

url = "http://localhost:11434/api/generate"  # Ollama API 地址
payload = {"model": "deepseek-r1:14b", "prompt": prompt,"options":options} 
def f(prompt):
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
    try:
        with requests.post(url,json=payload) as response:
            for line in response.iter_lines():
                if line:
                    data = line.decode('utf-8')
                    yield data
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

generator = f("你好")
for chunk in generator:
    print(chunk,type(chunk))