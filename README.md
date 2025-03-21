# deepseek部署对外调用接口

执行以下命令创建虚拟环境：

```bash
conda create -n sellingrobot python=3.11
source activate sellingrobot
pip install -r requirements.txt
```

然后执行以下命令启动后端服务：

```bash
nohup python main.py >> log.log 2>&1 &
```

访问http://localhost:9528即可使用。


