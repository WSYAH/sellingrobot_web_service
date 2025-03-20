import redis

from app.base.utils.base_utils import get_redis_config


def connect_redis(host, port, password, db):
    """
    获取redis连接
    :param host: redis ip
    :param port: 端口
    :param password: 密码
    :param db: 数据库
    :return: redis连接
    """
    redis_pool = redis.ConnectionPool(max_connections=100, host=host, port=port, password=password, db=db)
    return redis.Redis(connection_pool=redis_pool)


redis_config = get_redis_config()
my_redis = connect_redis(redis_config['host'], redis_config['port'], redis_config['password'], redis_config['db'])


def get_redis_data(conn=my_redis, key=None):
    """
    根据key获取value
    :param conn: redis连接
    :param key:
    :return:
    """
    data = conn.get(key)
    return data


def set_redis_data(conn=my_redis, key=None, value=None, ex=None):
    """
    设置key对应的alue
    :param conn: redis连接
    :param key:None
    :param value:
    :param ex: Redis过期时间,不设置则默认不过期
    :return:
    """
    data = conn.set(
        name=key,
        value=value,
        ex=ex
    )
    return data


def delete_redis_data(conn=my_redis, key=None):
    """
    删除key对应数据
    :param conn: redis连接
    :param key:
    :return:
    """
    data = conn.delete(key)
    return data
