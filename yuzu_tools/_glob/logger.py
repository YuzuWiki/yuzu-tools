from typing import Union
import logging as __logging

from yuzu_tools import __name__ as Frame_Name

__logging.basicConfig(level=__logging.INFO)
__logger: Union[__logging.Logger,None] = None


def setLogger(logger: "__logging.Logger"):
    global __logger
    if not __logger:
        __logger = logger


def getLogger(name: str = Frame_Name) -> "__logging.Logger":
    global __logger

    if not __logger:
        __logger = __logging.getLogger("yuzu_tools")

    class Proxy:
        def __getattr__(self, item):
            global __logger
            return getattr(__logger, item)

    return Proxy() # noqa

