__all__ = ["wrapper_api"]

from functools import wraps as _wraps
from inspect import getmodule
from typing import Callable, Dict, List, Tuple

import flask
from flask import request as _flask_request
from flask_restful import HTTPException as _HTTPException

from yuzu_tools import logger


def wrapper_api(api: Callable, wraps: Tuple[Callable] = None) -> Callable:  # 栈顶 -> 栈底
    module_path: str = getmodule(api).__name__
    api_name: str = api.__qualname__

    if wraps:
        for wrap in wraps[::-1]:
            api = wrap(api)

    @_wraps(api)
    def wrapper(*arg, **kwargs):
        try:
            response = api(*arg, **kwargs)
        except _HTTPException as e:  # parse_args error
            try:
                message: List[Dict[str, str]] = [
                    {"key": k, "value": v} for k, v in e.data["message"].items()
                ]
            except:  # noqa
                message: List[Dict[str, str]] = []
                errmsg: str = str(e)  # see flask_restful.abort
            else:
                errmsg: str = "Params Error"

            logger.exception(
                f"[API] {module_path}.{api_name} ERROR: error={errmsg}"
                f"\n\targs = {_flask_request.args.to_dict()}; "
                f"\n\tbody = {_flask_request.json or dict()};"
                f"\n\tmessage = {message}; \n"
            )
            return flask.abort(400, errmsg=errmsg, message=message)

        except Exception as e:
            logger.exception(
                f"[API] {module_path}.{api_name} ERROR:, error={str(e)}"
                f"\n\targs = {_flask_request.args.to_dict()}; "
                f"\n\tbody = {_flask_request.json or dict()}; \n"
            )
            return flask.abort(400, errmsg=str(e))

        else:
            logger.debug(
                f"[API] {module_path}.{api_name}:"
                f"\n\targs = {_flask_request.args.to_dict()}; "
                f"\n\tbody = {_flask_request.json or dict()}; "
            )

        return response

    return wrapper
