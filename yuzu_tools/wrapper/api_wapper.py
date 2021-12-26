from typing import Callable, Dict, Any, Union, Tuple, List
from functools import wraps
from collections import OrderedDict
from dataclasses import dataclass

from flask import (
    request as _flask_request,
    Flask as _Flask
)

from yuzu_tools._glob import logger
from yuzu_tools.errors import WrapperError
from yuzu_tools.utils.datetime_utils import curr_timestamp


BEFORE_FN_VALUE = Union[Tuple[int, str], None]


@dataclass
class OnExc:
    err_msg: str
    err_types: Tuple[type]


def fail(err_code: int, err_msg: str) -> dict:
    return {
        "result":       "failure",
        "error_code":   err_code,
        "reason":       err_msg
    }


def _get_name(obj: Any) -> str:
    """
        获取函数名称
    :param fn:
    :return:
    """
    from inspect import isclass, ismethod

    if isclass(obj):
        return obj.__name__
    elif ismethod(obj):
        return obj.__name__
    else:
        return obj.__class__.__name__


class ApiWrapper(object):
    """
        def before() -> is_ok, [err_code, err_msg]:
            ...

        def after(api: Flask, method: str, ret: Union[dict, Any]):
            ...


        使用示例：
            # ========= 装饰器申明 ==========
            api_wrapper = ApiWrapper()
            api_wrapper.register_before(
                before,
            )
            api_wrapper.register_after(
                after,
            )
            api_wrapper.register_on_exc(
                (RedisError, 4000, "redis error" )
            )


            # ========= 实际使用 ===========
            class TestAPI(YgResource):

                @api_wrapper
                def get(self):
                    ...
    """
    default_errcode = 5000
    default_errmsg = "SYSTEM ERROR"

    __before: Dict[str, Callable] = None
    __after: Dict[str, Callable] = None
    __on_exc: Dict[int, OnExc] = None

    def __init__(self):
        self.__before = OrderedDict()
        self.__after = OrderedDict()

    def _run_before(self) -> Tuple[bool, BEFORE_FN_VALUE]:
        for name, fn in self.__before:
            try:
                is_ok, err_value = fn()
                if not is_ok:
                    return False, err_value
            except Exception as e:
                return False, (self.default_errcode, self.default_errmsg)

        return True, None

    def _run_after(self, api: "_Flask", method: str, ret: Union[dict, Any]):
        for name, fn in self.__before:
            try:
                is_ok, err_value = fn(api=api, method=method, ret=ret)
                if not is_ok:
                    return False, err_value
            except Exception as e:
                logger.error(e)

    def _on_exc(self, e: Exception) -> dict:
        for err_code, on_exc in self.__on_exc:
            if issubclass(e.__class__, on_exc.err_types):
                return fail(err_code=err_code, err_msg=on_exc.err_msg)

        return fail(err_code=self.default_errcode, err_msg=self.default_errmsg)

    def __call__(self, api_method: Callable):

        @wraps(api_method)
        def _wrapper(api: "_Flask", *args, **kwargs):
            api_name: str = _get_name(api)
            method: str = api_method.__name__.upper

            is_ok, err_body = self._run_before()
            if not is_ok:
                logger.debug(f"{api_name}.{method} API: run before fail, err_body = {err_body}"
                             f"\n\targs = {_flask_request.args.to_dict()}; "
                             f"\n\tbody = {_flask_request.json or dict()}; ")
                return fail(err_code=err_body[0], err_msg=err_body[1])

            begin_time: int = curr_timestamp()
            try:
                ret = api_method(api, *args, **kwargs)
            except Exception as e:
                logger.error(f"{api_name}.{method} API:  fail, error = {str(e)}"
                             f"\n\targs = {_flask_request.args.to_dict()}; "
                             f"\n\tbody = {_flask_request.json or dict()}; ")
                logger.exception(e)
                return self._on_exc(e=e)
            else:
                spend_time: int = curr_timestamp() - begin_time
                logger.info(f"{api_name}.{method} API:  SUCCESS, spend_time = {spend_time} ms"                   
                            f"\n\targs = {_flask_request.args.to_dict()}; "
                            f"\n\tbody = {_flask_request.json or dict()};"
                            f"\n\tresponse = {str(ret)[:1000]}")

            self._run_after(api=api, method=method, ret=ret)
            return ret

        return _wrapper

    def register_before(self, *  fns: Callable):
        """
            注册请求开始前动作(一般是检测性质动作), 函数不会重名
        :param fns:
            eg.  def before() -> tuple[is_ok, Union[Tuple[err_code, err_msg], None]]:
                is_ok == True: ret = [True, None]
                is_ok == False: ret = [False, [err_code， err_msg]]
        :return:
        """
        for fn in fns:
            fn_name = _get_name(fn)
            if fn_name in self.__before:
                raise WrapperError(f"Register Before ERROR: {fn_name} already exists")

            self.__before[fn_name] = fn

    def register_after(self, *fns: Callable):
        """
            注册请求结束后动作
        :param fns:
                eg.  def after(api: Flask, method: str, ret: Union[dict, Any]):
        :return:
        """
        for fn in fns:
            fn_name = _get_name(fn)
            if fn_name in self.__after:
                raise WrapperError(f"Register Before ERROR: {fn_name} already exists")

            self.__after[fn_name] = fn

    def register_on_exc(self, *args: Tuple[Exception, int, str]):
        """
            注册异常时， 对某些异常类型的特殊处理（err_code， err_msg）
        :param args:
            eg Exception, 5000, "系统异常"
        :return:
        """
        ...
