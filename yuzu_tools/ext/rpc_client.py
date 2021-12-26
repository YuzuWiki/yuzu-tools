__all__ = ["RpcClient"]

from typing import Any

from xmlrpc.client import (
    ServerProxy as _ClientProxy,
)

from yuzu_tools._glob import logger
from yuzu_tools.utils.datetime_utils import curr_timestamp


class _RpcLogContext(object):

    def __init__(self, url: str, api: str, params: Any):
        self._url: str = url + "/" + api.replace(".", "/")
        self._begin_time: int = 0
        self._params = params

    @staticmethod
    def spend_time(begin_time: int, done_time: int) -> str:
        spend_t = done_time - begin_time

        ret = f"{spend_t % 1000} MS"
        spend_t = spend_t // 1000
        for index, unit in enumerate(["S ", "M:", "H:"], start=1):
            if spend_t <= 0:
                return ret

            ret = f"{spend_t % 60}{unit}" + ret
            spend_t = spend_t // 60

    def __enter__(self):
        self._begin_time = curr_timestamp()

    def __exit__(self, exc_type, exc_val, exc_tb):
        log_fmt = "[RPC client] {status}:  begin_time = {begin_time} spend_time = {spend_time}  " \
                  "URL = {url}  params = {params} {error}"

        spend_time = self.spend_time(self._begin_time, curr_timestamp())
        if exc_type:
            logger.error(
                log_fmt.format(
                    cls_name=self.__class__.__name__,
                    status="FAIL",
                    begin_time=self._begin_time,
                    spend_time=spend_time,
                    url=self._url,
                    params=self._params,
                    error=f"error = {exc_val}")
            )

        else:
            logger.info(
                log_fmt.format(
                    cls_name=self.__class__.__name__,status="SUCCESS",
                    begin_time=self._begin_time,
                    spend_time=spend_time,
                    url=self._url,
                    params=self._params,
                    error="")
            )


class _Method:
    # some magic to bind an XML-RPC method to an RPC server.
    # supports "nested" methods (e.g. examples.getStateName)
    def __init__(self, send, name):
        self.__send = send
        self.__name = name

    def __getattr__(self, name):
        return _Method(self.__send, "%s.%s" % (self.__name, name))

    def __call__(self, *args):
        return self.__send(self.__name, args)


class RpcClient(_ClientProxy):
    """
        eg。
            class RpcClient(RpcClient):
                ...

            client = RpcClient("127.0.0.1:20075")   # default: http://127.0.0.1:20075
            client.alive()                          # 等价访问 rpc:  127.0.0.1:20075/alive

    """

    def __init__(self, uri: str, *args, **kwargs):
        uri = uri.strip()
        if len(uri.split("://")) == 1:
            uri = f"http://{uri}"
        self._url = uri

        super(RpcClient, self).__init__(uri=self._url,  *args, **kwargs)

    def __getattr__(self, name):
        return _Method(self.__request, name)

    def __request(self, methodname: str, params: Any):
        with _RpcLogContext(url=self._url, api=methodname, params=params):
            request = getattr(super(RpcClient, self), f"_{_ClientProxy.__name__}__request")
            return request(methodname, params)

