# deepseek对外接口+reranker模型对外接口

执行以下命令：

```bash
source activate sellingrobot
```

然后执行以下命令启动后端服务：

```bash
nohup python main.py >> log.log 2>&1 &
```

访问http://localhost:9528即可使用。


服务器若未联网，则可以先联网
curl --data "user={学号}&pass={密码}" http://10.3.8.211/login | grep 'success'


### embedding模型每次启动都要在GPU上挂一个进程,想办法清理掉
nvidia-smi | grep sellingrobot/bin/python | awk '{print $5}' | xargs kill -9

### 停止ollama进程
lsof -i:11434 | grep ollama | awk '{print $2}' | xargs kill -9

!wget https://github.com/ollama/ollama/releases/download/v0.6.2/ollama-linux-amd64.tgz
