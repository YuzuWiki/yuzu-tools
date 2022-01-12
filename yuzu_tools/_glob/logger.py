from typing import Union
import logging as __logging

from yuzu_tools import __name__ as Frame_Name

__logging.basicConfig(level=__logging.INFO)
__logger: Union[__logging.Logger,None] = None


def setLogger(logger: "__logging.Logger"):
    global __logger
    if not __logger:
        __logger = logger


def _get_logger() -> "__logging.Logger":
    return __logger


def getLogger(name: str = Frame_Name, level: int = __logging.DEBUG) -> "__logging.Logger":
    global __logger

    if not __logger:

        # # handler 设置
        handler = __logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(
            __logging.Formatter('| %(asctime)s.%(msecs)04d | %(name)-10s | %(levelname)-6s:  %(message)s',
                                datefmt="%Y-%m-%d %H:%M:%S"))

        # 配置默认的logger
        __logger = __logging.Logger(name)
        __logger.addHandler(handler)


    class Proxy:
        def __getattr__(self, level):
            global __logger
            return getattr(_get_logger(), level)

    return Proxy() # noqa

