import socket
import traceback
from functools import wraps

import pymongo
from bson import ObjectId

from app.base import mongodb_user, mongodb_ip, mongodb_pwd, mongodb_port, auth, db_name
from app.base.utils import logger
from config.config import all_data


def get_ips():
    """
    获取本地ip
    :return: 本地ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception:
        logger.error(traceback.format_exc())
        print('get ip error')
        return ''
    print(f'my ip: {ip}')
    return ip


def get_mongo_client(no):
    """
    获取mongo连接
    :return:
    """
    if no == 0:
        return None
    return pymongo.MongoClient(
        f"mongodb://{mongodb_user}:{mongodb_pwd!s}@{mongodb_ip!s}:{mongodb_port!s}/?authSource"
        f"={auth!s}&readPreference=primary&appname=MongoDB%20Compass&ssl=false", connect=False)[db_name]


first = 0
my_db = get_mongo_client(first)
first += 1


def decorator_db():
    def decorator(function):
        @wraps(function)
        def returned_wrapper(*args, **kw):
            global my_db
            if my_db is None:
                my_db = get_mongo_client(first)
            try:
                r = function(*args, **kw)
            except Exception:
                my_db = get_mongo_client(first)
                r = function(*args, **kw)
            return r

        return returned_wrapper

    return decorator


@decorator_db()
def insert_data(table_name, **kwargs):
    """
    插入单条数据
    :param table_name: 集合名
    :param kwargs: 数据dict
    :return: 插入数据结果
    """
    data_table = my_db[table_name]
    x = data_table.insert_one(kwargs)
    return x


@decorator_db()
def replace_one(table_name, filter, replacement, **kwargs):
    """
    替换单条数据
    :param filter: 查询到单条数据
    :param replacement: 替换后的数据
    :param table_name: 集合名
    :param kwargs: 数据dict
    :return: 插入数据结果
    """
    data_table = my_db[table_name]
    x = data_table.replace_one(filter, replacement, kwargs)
    return x


@decorator_db()
def get_data(table_name=None, my_filter=None, args=None):
    """
    获得单条数据
    :param table_name: 集合名
    :param my_filter: 查询条件
    :param args: 额外查询条件，比如过滤字段
    :return: 数据dict
    """
    data_table = my_db[table_name]
    data = data_table.find_one(my_filter, args)
    return data


@decorator_db()
def get_data_last(table_name=None, my_filter=None, args=None):
    """
    获得单条数据
    :param table_name: 集合名
    :param my_filter: 查询条件
    :param args: 额外查询条件，比如过滤字段
    :return: 数据dict
    """
    data_table = my_db[table_name]
    data = data_table.find_one(my_filter, args, sort=[("_id", -1,)])
    return data


@decorator_db()
def save_data(table_name=None, to_save=None):
    """
    保存单条数据
    :param to_save: 文档
    :param table_name: 集合名
    :return: 数据dict
    """
    data_table = my_db[table_name]
    data = data_table.save(to_save)
    return data


@decorator_db()
def save_many_data(table_name=None, to_save=None):
    """
    保存多条数据
    :param to_save: 文档
    :param table_name: 集合名
    :return: 数据dict
    """
    data_table = my_db[table_name]
    data = data_table.insert_many(to_save)
    return data


@decorator_db()
def filter_data(table_name=None, my_filter=None, args=None):
    """
    选择多条数据
    :param table_name: 集合名
    :param my_filter: 过滤条件
    :param args: 额外查询条件，比如过滤字段
    :return: 数据list
    """
    data_table = my_db[table_name]
    data = data_table.find(my_filter, args)
    return data


@decorator_db()
def update_datas(table_name, query_str, update_str):
    """
    修改单条数据
    :param table_name: 集合名
    :param query_str: 过滤条件
    :param update_str: 修改内容
    :return: 修改结果
    """
    data_table = my_db[table_name]
    data = data_table.update_many(query_str, update_str)
    return data


@decorator_db()
def aggregate_data(table_name=None, my_filter=None):
    """
    聚合数据
    :param table_name: 集合名
    :param my_filter: 过滤条件
    :return: 数据list
    """
    data_table = my_db[table_name]
    data = data_table.aggregate(my_filter)
    return data


@decorator_db()
def bulk_write_data(table_name=None, my_filter=None, write_no=1000):
    """
    批量操作数据
    :param write_no: 批量操作数量上限
    :param table_name: 集合名
    :param my_filter: 过滤条件
    :return: 数据list
    """
    data_table = my_db[table_name]
    data = 0
    for i in range(0, len(my_filter), write_no):
        data = data_table.bulk_write(my_filter[i: i + write_no])

    return data


@decorator_db()
def page_query(table_name=None, my_filter=None, args=None, page_size=1, page_no=1):
    """
    分页查询
    :param table_name: 集合名
    :param my_filter: 过滤条件
    :param args: 额外查询条件，比如过滤字段
    :param page_size: 查询数据条数
    :param page_no: 页码
    :return: 查询结果
    """
    skip = page_size * (page_no - 1)
    data_table = my_db[table_name]
    data = data_table.find(my_filter, args)
    page_count = data.count()
    data = data.sort("_id", pymongo.DESCENDING).limit(page_size).skip(skip)
    return list(data), page_count


@decorator_db()
def page_query_sort(table_name=None, my_filter=None, args=None, page_size=1, page_no=1, sort_k='_id',
                    sort_v=pymongo.DESCENDING):
    """
    分页查询排序
    :param sort_k: 排序key
    :param sort_v: 排序value
    :param table_name: 集合名
    :param my_filter: 过滤条件
    :param args: 额外查询条件，比如过滤字段
    :param page_size: 查询数据条数
    :param page_no: 页码
    :return: 查询结果
    """
    skip = page_size * (page_no - 1)
    data_table = my_db[table_name]
    data = data_table.find(my_filter, args)
    page_count = data.count()
    data = data.sort(sort_k, sort_v).limit(page_size).skip(skip)
    return list(data), page_count


@decorator_db()
def delete_data_one(table_name, my_filter):
    """
    删除单条数据
    :param table_name: 集合名
    :param my_filter: 过滤条件
    :return: 删除结果
    """
    data_table = my_db[table_name]
    data = data_table.delete_one(my_filter)
    return data


@decorator_db()
def delete_data_many(table_name, my_filter):
    """
    删除多条数据
    :param table_name: 集合名
    :param my_filter: 过滤条件
    :return: 删除结果
    """
    data_table = my_db[table_name]
    data = data_table.delete_many(my_filter)
    return data


@decorator_db()
def update_data(table_name, query_str, update_str):
    """
    修改单条数据
    :param table_name: 集合名
    :param query_str: 过滤条件
    :param update_str: 修改内容
    :return: 修改结果
    """
    data_table = my_db[table_name]
    data = data_table.update_one(query_str, update_str)
    return data


@decorator_db()
def delete_all_data(table_name):
    """
    删除所有数据
    :param table_name: 集合名
    :return: 删除结果
    """
    data_table = my_db[table_name]
    data = data_table.delete_many({})
    return data


@decorator_db()
def initialization_user(root_group_config):
    """
    初始化数据库,根据需要改动
    :param root_group_config:
    """
    pass





@decorator_db()
def create_all_index(table_name, keys, **kwargs):
    data_table = my_db[table_name]
    data = data_table.index_information()
    for k, v in data.items():
        if v['key'] == keys:
            return
    try:
        data = data_table.create_index(keys, **kwargs)
    except Exception:
        logger.error(traceback.format_exc())
    return data


@decorator_db()
def get_data_count(table_name=None, my_filter=None, args=None):
    '''
    返回匹配数据条数
    :param table_name:集合名
    :param my_filter: 过滤条件
    :param args: 额外查询条件
    :return: count
    '''
    data_table = my_db[table_name]
    count = data_table.find(my_filter, args).count()
    return count


@decorator_db()
def update_datas(table_name, query_str, update_str):
    """
    修改单条数据
    :param table_name: 集合名
    :param query_str: 过滤条件
    :param update_str: 修改内容
    :return: 修改结果
    """
    data_table = my_db[table_name]
    data = data_table.update_many(query_str, update_str)
    return data



