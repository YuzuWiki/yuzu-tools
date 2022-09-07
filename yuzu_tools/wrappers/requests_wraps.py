import sys
from functools import wraps as _wraps
from inspect import getmodule
from typing import Any, Callable, Dict, Tuple

from requests import Response as _Response

from yuzu_tools import logger


def _fmt_ret_data(data) -> str:
    if data is None:
        return ""

    if isinstance(data, str):
        return data[:100]

    if isinstance(data, list):
        return str(data[:10])

    if isinstance(data, tuple):
        return str(data[:10])

    return str(data)[:100]


def requests_wrapper(
    fn: Callable,
    on_exc: Callable = None,  # def on_exc(resp: requests.Response): raise ValueError("xxx")
    wraps: Tuple[Callable] = None,  # 栈顶 -> 栈底
):
    """

        note:
            just run once 'requests.method'
        bad:
            @gateway_wrapper
            def xxx():
                with requests.get(...) as resp:
                   ...

                with requests.get(...) as resp_1:
                    ...

        good:
            @gateway_wrapper
            def xxx():
                with requests.get(...) as resp:
                   ...

            @gateway_wrapper
            def xxx():
                with requests.get(...) as resp:
                   ...

                with requests.get(...) as resp:  # locals will cover 'resp'
                   ...

    :param fn:
    :param on_exc:
    :param wraps:
    :return:
    """
    module_path: str = getmodule(fn).__name__
    func_name: str = fn.__name__

    on_exc = on_exc or (lambda _: None)
    if wraps:
        for wrap in wraps[::-1]:
            fn = wrap(fn)

    @_wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            ret = fn(*args, **kwargs)
        except Exception as e:
            f_locals: Dict[str, Any] = sys.exc_info()[2].tb_next.tb_frame.f_locals
            if f_locals:
                for resp in f_locals.values():
                    if not isinstance(resp, _Response):
                        continue

                    on_exc(resp)
                    break

            #  default log
            logger.exception(
                f"[Requests] {module_path}.{func_name}: error={str(e)}"
                f"\n\targs={args} "
                f"\n\tkwargs={kwargs}\n"
            )
            raise
        else:
            logger.info(
                f"[Requests] {module_path}.{func_name}: "
                f"\n\targs={args} "
                f"\n\tkwargs={kwargs} "
                f"\n\tdata={_fmt_ret_data(ret)}"
            )
            return ret

    return wrapper
