class BaseError(Exception):
    ...


class WrapperError(BaseError):
    ...


class RpcError(BaseError):
    ...


class RedisError(BaseError):
    ...
