"""
配置变量定义
"""

import os

import yaml

from config import version

def merge_dict(base_d, extend_d):
    for key in extend_d.keys():
        base_nxt = base_d.get(key)
        extend_nxt = extend_d.get(key)
        if base_nxt is None:
            base_d[key] = extend_nxt
        elif isinstance(extend_nxt, dict):
            merge_dict(base_nxt, extend_nxt)
        else:
            base_d[key] = extend_nxt if key not in base_d else base_nxt


base_d = dict()
package_path = os.path.abspath(f'config/{version}')
for file in os.listdir(package_path):
    if file.endswith(".yaml"):
        with open(os.path.join(package_path, file), 'r', encoding='utf-8') as r:
            extend_d = yaml.load(r, Loader=yaml.FullLoader)
            if file == "config.yaml":
                base_d, extend_d = extend_d, base_d
            merge_dict(base_d, extend_d)

all_data = base_d
return_error_code = all_data['return_error_code']


def err_response_code(code=1, data="", **kwargs):
    """
    请求错误时返回
    :param code: 错误码
    :param data: 数据信息
    """
    if data != "":
        params = {
            "code": code,
            "data": data,
            "msg": return_error_code[code]
        }
    else:
        params = {
            "code": code,
            "msg": return_error_code[code]
        }
    if kwargs:
        params.update(kwargs)
    return params


def exc_response(msg, **kwargs):
    """
    异常时返回错误信息
    :param msg:错误信息
    """
    params = {
        "code": 1,
        "msg": msg
    }
    if kwargs:
        params.update(kwargs)
    return params
