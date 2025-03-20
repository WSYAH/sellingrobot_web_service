import importlib
import os

from fastapi import FastAPI
from fastapi.routing import APIWebSocketRoute

app = FastAPI(docs_url=None, redoc_url=None)

interface_list = ['develop_version', 'pams', 'OfficeAdmin', 'justplay', 'user_manage', 'camera', 'hg_websocket',
                  'gitkens']
service_dir = []
service_name = [name for name in os.listdir('./app') if not name.startswith("__")]
for service in service_name:
    # if service in interface_list:
    service_dir.append(service)
visited_routes = set()
root_group_config = set()
for ser in service_dir:
    if ser == '.DS_Store':
        continue
    func_dir = os.listdir('./app/' + ser)
    for interface_dir in func_dir:
        if interface_dir[0] != '_':
            if interface_dir == '.DS_Store':
                continue
            p = './app/' + ser + '/' + interface_dir
            interface_name = os.listdir(p)
            for i in interface_name:
                if i[0:9] == 'interface':
                    import_package = '.' + ser + '.' + interface_dir + '.' + i.split('.')[0]
                    params_ = importlib.import_module(import_package, package='app')
                    router = getattr(params_, 'router')
                    new_routes = []
                    # 去重
                    for route in router.routes:
                        if isinstance(route, APIWebSocketRoute):
                            app.include_router(router)
                            continue
                        key = f"{p}:{route.path}{route.name}{str(route.methods)}"
                        if key not in visited_routes:
                            new_routes.append(route)
                            visited_routes.add(key)
                    router.routes = new_routes
                    app.include_router(router=router)
