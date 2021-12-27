import time
from datetime import datetime
from typing import Union

from yuzu_tools import const


def curr_timestamp() -> int:
    # 十三位时间戳
    return int(time.time() * 1000)


def curr_datetime() -> "datetime":
    return datetime.now()


def curr_strftime(fmt: str = const.FMT_DATETIME) -> str:
    return datetime.now().strftime(fmt)


def _fmt_timestamp(timestamp: int) -> Union[int, float]:
    if timestamp > 1000000000000:
        timestamp /= 1000
    return timestamp


def timestamp_to_strftime(timestamp: int, fmt: str = const.FMT_DATETIME) -> str:
    return datetime.fromtimestamp(_fmt_timestamp(timestamp)).strftime(fmt)


def timestamp_to_datetime(timestamp: int) -> "datetime":
    return datetime.fromtimestamp(_fmt_timestamp(timestamp))


def datetime_to_strftime(date: "datetime", fmt: str = const.FMT_DATETIME) -> str:
    return date.strftime(fmt)


def strftime_to_timestamp(strftime: str, fmt: str = const.FMT_DATETIME) -> int:
    t = time.strptime(strftime, fmt)
    return int(time.mktime(t) * 1000)
