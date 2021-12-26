from typing import Union
import logging as __logging

__logging.basicConfig(level=__logging.INFO)
__logger: Union[__logging.Logger,None] = None


def setLogger(logger: "__logging.Logger"):
    global __logger
    if not __logger:
        __logger = logger


def _getLogger() -> "__logging.Logger":
    global __logger
    return __logger


def getLogger() -> "__logging.Logger":
    global __logger

    if not __logger:
        __logger = __logging.getLogger("yuzu_tools")

    class Proxy:
        def __getattr__(self, item):
            global __logger
            return getattr(_getLogger(), item)

    return Proxy()

