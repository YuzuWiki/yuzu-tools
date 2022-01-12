import json
from dataclasses import dataclass
from typing import Union, Any, Iterator, Literal, Optional, Callable

from redis import (
    Redis as _Redis,
    ConnectionPool as _ConnectionPool, RedisError
)

from _glob import logger
from utils.datetime_utils import curr_timestamp

_REDIS_VALUE = Union[bytes, float, int, str]
_JSON_VALUE = Union[dict, set, tuple, list]


class RedisTask(object):
    task_iD:        str
    body:           Any  # task body
    retry_times:    int = 1
    _queue: "_RedisQueue" = None

    def __init__(self, body:  Any, task_id: str = None):
        self.taskID = task_id or self._make_taskid()
        self.body = body

    def _make_taskid(self) -> str:
        return f"{curr_timestamp()}:{hash(self)}"

    def bound(self, queue: "_RedisQueue") -> "RedisTask":
        if not self._queue:
            self._queue = queue
        return self

    def reput(self, is_jump: bool = False) ->  bool:
        if self.retry_times <= 0:
            return False

        if is_jump:
            self._queue.jump(task=self)
        else:
            self._queue.put(task=self)
        return True

    def to_dict(self) -> dict:
        return {
            "task_id":      self.taskID,
            "body":         self.body,
            "retry_times":  self.retry_times
        }

    def to_str(self) -> str:
        return json.dumps({
            "task_id":      self.taskID,
            "body":         self.body,
            "retry_times":  self.retry_times
        })

    @classmethod
    def from_str(cls, t: str) -> "RedisTask":
        task = json.loads(t)
        return RedisTask(body=task["body"], task_id=task["task_id"])


class _RedisQueue(object):

    def __init__(self, key: str, conn: "_Redis"):
        self._conn = conn
        self._key = key

    @property
    def conn(self) -> "_Redis":
        return self._conn

    @property
    def key(self) -> str:
        return self._key

    def length(self) -> int:
        return self.conn.llen(self.key)

    @property
    def ttl(self) -> int:
        return self.conn.ttl(name=self.key)

    @ttl.setter
    def ttl(self, ttl: int = 3 * 60):
        self.conn.expire(name=self.key, time=ttl)

    def pop(self) -> Optional["RedisTask", None]:
        t = self.conn.lpop(name=self.key)
        if not t:
            return
        return RedisTask.from_str(t.decode("utf8")).bound(queue=self)

    def put(self, task: "RedisTask") -> int:
        if task.retry_times > 0:
            return self.conn.rpush(self.key, task.to_str())
        else:
            # 重试次数已经到达上限时候不再重试
            return 0

    def jump(self, task: "RedisTask") -> int:
        return self.conn.lpush(self.key, task.to_str())

    def incr(self, incr: int = 1) -> int:
        return self.conn.incr(self.key, incr)

    def decr(self, decr: int = 1) -> int:
        return self.conn.decr(self.key, decr)

    def clear(self) -> int:
        return self.conn.delete(self.key)

    def set_response_callback(self, command: str,call_able: Callable):
        self.conn.set_response_callback(command=command, callback=call_able)


class RedisQueue(object):
    ...