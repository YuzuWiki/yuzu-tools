import time
from contextlib import contextmanager
from typing import List

from redis import Redis

from yuzu_tools.ext import RedisCounter, RedisQueue

_redis_host = "119.8.30.197"
_redis_post = 6379
_redis_password: str = "FlyingNuts20211125"


@contextmanager
def _with_context(conn: "Redis", key: str, suffix: str) -> "Redis":
    conn.delete(key)
    conn.delete(f"{key}:{suffix}")
    yield conn
    conn.delete(key)
    conn.delete(f"{key}:{suffix}")


class TestRedisCounter(object):
    _conn: "Redis" = None

    queue_key: str = "ygfans_frams:tests:redis_counter"
    _counter_key: str = None

    @property
    def counter_suffix(self) -> str:
        return RedisCounter._suffix

    @property
    def counter_key(self) -> str:
        if not self._counter_key:
            self._counter_key = self.queue_key + ":" + self.counter_suffix
        return self._counter_key

    def setup(self):
        if not self._conn:
            self._conn = Redis(host=_redis_host, port=_redis_post, password=_redis_password)
            assert self._conn.ping(), "invalid Redis server"

    def teardown(self):
        if self._conn:
            self._conn.close()

    def test_counting(self):
        with _with_context(conn=self._conn, key=self.queue_key, suffix=self.counter_suffix) as conn:
            counter = RedisCounter(queue_key=self.queue_key, conn=conn)

            assert counter.key == self.counter_key, "RedisCounter: key error"
            assert counter.total == 0, "RedisCounter: 不存在的 key 应当返回-1"

            assert counter.incr() == 1, "RedisCounter: 自增一次结果错误"
            assert counter.decr() == 0, "RedisCounter: 自减一次结果错误"
            assert counter.total == 0, "RedisCounter: total 应当为 0"

    def test_set(self):
        ttl = 1
        with _with_context(conn=self._conn, key=self.queue_key, suffix=self.counter_suffix) as conn:
            counter = RedisCounter(queue_key=self.queue_key, conn=conn)
            assert counter.total == 0, "RedisCounter: 不存在的 key 应当返回-1"

            counter.set(1, ttl=ttl)
            assert counter.total == 1, "RedisCounter: set 错误, 未 set 进值"

            time.sleep(ttl)
            assert counter.total == 0, "RedisCounter: set 错误, key 应当已经失效"


class TestRedisQueue(object):
    _conn: "Redis" = None

    queue_key: str = "ygfans_frams:tests:redis_queue"

    @property
    def counter_suffix(self) -> str:
        return RedisCounter._suffix

    def setup(self):
        if not self._conn:
            self._conn = Redis(host=_redis_host, port=_redis_post, password=_redis_password)
            assert self._conn.ping(), "invalid Redis server"

    def teardown(self):
        if self._conn:
            self._conn.close()

    def test_consumption(self):
        with _with_context(conn=self._conn, key=self.queue_key, suffix=self.counter_suffix) as conn:
            queue = RedisQueue(queue_key=self.queue_key, conn=conn)
            assert not queue.pop() and queue.is_empty(), f"RedisQueue: 空队列无法 pop 数据, {queue.total()}"

            queue.put("1")
            assert not queue.is_empty(), f"RedisQueue: put 后队列应当不为空 "
            assert queue.pop() == "1" and queue.is_empty(), "RedisQueue: put 》 pop 异常 "

    def test_maxsize(self):
        max_size = 3
        with _with_context(conn=self._conn, key=self.queue_key, suffix=self.counter_suffix) as conn:
            queue = RedisQueue(queue_key=self.queue_key, conn=conn, max_size=max_size)
            assert not queue.pop() and queue.is_empty(), f"RedisQueue: 空队列无法 pop 数据, {queue.total()} / {max_size}"

            queue.put("1")
            queue.put("2")
            assert not queue.is_full(), f"RedisQueue: {queue.total()} / {max_size}"

            queue.put("3")
            assert queue.is_full(), f"RedisQueue: {queue.total()} / {max_size}"

            queue.put("4")
            assert queue.is_full(), f"RedisQueue: {queue.total()} / {max_size}"

    def test_queue(self):
        with _with_context(conn=self._conn, key=self.queue_key, suffix=self.counter_suffix) as conn:
            queue = RedisQueue(queue_key=self.queue_key, conn=conn)
            queue.put("1")
            queue.put("2")
            queue.jump("4")
            queue.put("3")

            assert queue.total() == 4, "RedisQueue: total error"

            arr: List[str] = []
            while not queue.is_empty():
                arr.append(queue.pop())

            assert ";".join(arr) == "4;1;2;3", f"RedisQueue: jump & put error, data = {arr}"
