import json
from typing import Union

from redis import (
    Redis as _Redis,
    ConnectionPool as _ConnectionPool
)

from _glob import logger

_REDIS_VALUE = Union[bytes, float, int, str]
_JSON_VALUE = Union[dict, set, tuple, list]


def _fmt_item(body:  Union[_REDIS_VALUE, _JSON_VALUE]) -> _REDIS_VALUE:
    if isinstance(body, (bytes, float, int, str)):
        return body
    else:
        return json.dumps(body)


class RedisCounter(object):
    _suffix: str = "counter"

    def __init__(self, queue_key: str, conn: "_Redis"):
        assert conn, "RedisCounter: MISS redis conn"

        self._key: str = ":".join((queue_key, self._suffix))
        self._conn: "_Redis" = conn

    @property
    def key(self) -> str:
        return self._key

    @property
    def conn(self) -> "_Redis":
        return self._conn

    def incr(self, incr: int = 1) -> int:
        return self.conn.incr(self.key, incr)

    def decr(self, decr: int = 1) -> int:
        return self.conn.decr(self.key, decr)

    def set(self, cnt: int, ttl: int = 30) -> bool:
        if ttl > 0:
            return self.conn.setex(name=self.key, time=ttl, value=cnt)
        else:
            return self.conn.setnx(self.key, cnt)

    @property
    def total(self) -> int:
        cnt_str: str = self.conn.get(name=self.key)
        if not cnt_str:
            return 0
        else:
            return int(cnt_str)

    def close(self):
        self.conn.close()

    def __del__(self):
        try:
            self.close()
        except:
            ...


class RedisQueue(object):
    _coon = None
    _counter_suffix: str = "counter"

    def __init__(self, queue_key: str, conn: "_Redis" = None, conn_pool: "_ConnectionPool" = None,
                 default_ttl: int = -1, max_size: int = -1):
        assert conn or conn_pool, "RedisQueue: MISS redis conn"
        assert queue_key, "RedisQueue: MISS redis queue_key"


        # 初始化队列基础信息
        self._default_ttl: int = default_ttl
        self._max_size: int = max_size
        self._queue_key: str = queue_key
        self._coon: "_Redis" = self._get_conn(conn=conn, conn_pool=conn_pool)
        # 计数器
        self._counter = RedisCounter(queue_key=queue_key, conn=self.conn)

    @staticmethod
    def _get_conn(conn: "_Redis" = None, conn_pool: "_ConnectionPool" = None) -> "_Redis":
        if conn:
            return conn
        else:
            return _Redis(connection_pool=conn_pool)

    @property
    def conn(self) -> "_Redis":
        return self._coon

    @property
    def key(self) -> str:
        return self._queue_key

    def _queue_len(self) -> int:
        return self.conn.llen(self.key)

    def is_empty(self) -> bool:
        if self._counter.total < 0:
            cnt = self._queue_len()
            self._counter.set(cnt=cnt, ttl=self._default_ttl)

        return self._counter.total == 0

    def is_full(self) -> bool:
        if self._max_size < 0:
            return False
        else:
            return self._counter.total >= self._max_size

    def total(self) -> int:
        if self.is_empty():
            return 0
        else:
            return self._counter.total

    def pop(self) -> Union[str, None]:
        ret = self.conn.lpop(name=self.key)
        if not ret:
            return ret

        self._counter.decr()
        if isinstance(ret, bytes):
            return ret.decode("utf8")
        else:
            return ret

    def put(self, *items: Union[_REDIS_VALUE, _JSON_VALUE]):
        """
            顺序入队
        :param items:
        :return:
        """
        self.conn.rpush(self.key, *[_fmt_item(item) for item in items])
        self._counter.incr(len(items))

    def jump(self, item: Union[_REDIS_VALUE, _JSON_VALUE]):
        """
            插队
        :param item:
        :return:
        """
        self.conn.lpush(self.key, _fmt_item(item))
        self._counter.incr()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            logger.error(f"[Redis Queue] Error: key = {self.key}   error = {exc_val}")

    def __del__(self):
        try:
            # close 计数器 conn
            self._counter.close()

            # close queue conn
            self.conn.close()
        except:
            ...
