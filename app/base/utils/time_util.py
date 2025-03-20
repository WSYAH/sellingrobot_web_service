"""
处理时间的工具类
"""

import time
import pytz
from datetime import datetime

TIME_ZONE = 'Asia/Shanghai'
tz = pytz.timezone(TIME_ZONE)
offset = 28800
formatter = "%Y-%m-%d %H:%M:%S"


def get_now(ms=True):
    return int(time.time() * (1000 if ms else 1))


def get_dt_by_tz(ts):
    return pytz.datetime.datetime.fromtimestamp(ts, tz)


def dt2str(dt, fmt=formatter):
    return dt.strftime(fmt)


def get_dt_by_ts(ts):
    try:
        return pytz.datetime.datetime.fromtimestamp(ts, tz)
    except OSError as err:
        return pytz.datetime.datetime.fromtimestamp(int(ts / 1000), tz)


def rounding_ts_unit_day(ts, floor=True):
    ts += offset * 1000
    rounded = ts - ts % 86400000
    if floor is False:
        rounded += 86400000
    rounded -= offset * 1000
    return rounded


def get_start_end_today(ts):
    start_ts = rounding_ts_unit_day(ts)
    end_ts = start_ts + 86400000
    return start_ts, end_ts


def timestamp2min(t):
    """
    时间戳转整分时间戳
    :param t: 原始时间戳
    :return: 整分时间戳
    """
    return int(t - t % 60000)


def ts_ms_to_rfc3339(timestamp):
    return ts_to_rfc3339(timestamp / 1000)


def ts_to_rfc3339(timestamp):
    utc_tz = pytz.utc
    utc_timestamp = datetime.fromtimestamp(timestamp, tz=utc_tz)
    formatted_time = utc_timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    rfc3339 = f"{formatted_time[:-2]}:{formatted_time[-2:]}"
    return rfc3339
