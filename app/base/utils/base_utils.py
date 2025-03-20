import hashlib
import time
import traceback
from datetime import datetime

from dateutil.tz import tz

from app.base import data
from app.base.utils import logger

base_config = data

def get_neo4j_config():
    """
    获取neo4j配置
    @return:
    """
    try:
        return base_config['neo4j']
    except KeyError:
        logger.error(traceback.format_exc())
        return None
def get_redis_config():
    """
    获取配置
    @return:
    """
    try:
        return base_config['redis']
    except KeyError:
        logger.error(traceback.format_exc())
        return None

def get_openai_config():
    """
    获取openAI的基础配置
    :return:
    """
    try:
        return base_config["big_model"]
    except KeyError:
        logger.error(traceback.format_exc())
        return None


def corr_response(data=None):
    """
    请求正常时返回
    :param data: 返回参数dict
    """
    params = {"code": 0, "data": 0} if data is None else {"code": 0, "data": data}
    return params


def err_response(description=''):
    """
    请求错误时返回
    :param description: 错误详情
    """
    params = {
        "code": 1,
        "data": "",
        "msg": description
    }
    return params


def hash_md5(content):
    """
    字符串md5加密
    :param content: 字符串明文
    :return: 密文
    """
    hash_data = hashlib.md5()
    hash_data.update(content.encode())
    return hash_data.hexdigest()[:32]


def update_token(random_content):
    """
    更新token
    :return: （用户名+当前时间）密文
    """
    token = hash_md5(random_content)
    return token


def get_page_no(all_no, no):
    """
    获取总页码数
    :param all_no: 所有数据数量
    :param no: 单页数据条数
    :return: 总页码数
    """
    return all_no // no if all_no % no == 0 else (all_no // no + 1)


def clear_d(args):
    """
    去掉dict中value为None的键值对
    :param args: 原始dict
    :return: 过滤后的dict
    """
    for k in list(args.keys()):
        if isinstance(args[k], dict):
            args[k] = clear_d(args[k])
        if args[k] is None:
            del args[k]
    return args


def get_min_timestamp():
    """
    获取分钟级别时间戳
    :return:
    """
    timestamp = int(time.time() * 1000)
    return timestamp - timestamp % 60000


def get_timestamp():
    """
    获取毫秒级时间戳
    :return:
    """
    return time.time() * 1000


def get_shanghai_now_time():
    """
    获取上海时区datetime
    :return:
    """
    return datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S.%f")


def get_value_unit(value, unit):
    if unit == '%':
        value = round(value * 100, 2)
    elif unit == 'MB':
        value = int(value)
    elif unit == 'GB':
        value = round(value, 1)
    else:
        value = round(value, 2)
    return value
