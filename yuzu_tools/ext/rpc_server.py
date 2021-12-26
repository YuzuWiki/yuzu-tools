__all__ = ["RpcServer"]

from concurrent.futures import (
    ThreadPoolExecutor as _ThreadPoolExecutor
)
from socketserver import (
    ThreadingMixIn as _ThreadingMixIn
)
from xmlrpc.server import (
    SimpleXMLRPCServer as _SimpleXMLRPCServer,
    SimpleXMLRPCRequestHandler as _SimpleXMLRPCRequestHandler
)
from threading import (
    Lock as _threading_Lock,
    Thread as _Thread
)

from yuzu_tools._glob import logger
from yuzu_tools.errors import RpcError


class _RpcServer(_ThreadingMixIn, _SimpleXMLRPCServer):
    _pool = None
    _worker: int = 1

    def init_pool(self, worker: int):
        if worker <= 0:
            raise RpcError("invalid worker")

        self._worker = worker or self._worker

    @property
    def pool(self) -> "_ThreadPoolExecutor":
        if not self._pool:
            self._pool = _ThreadPoolExecutor(max_workers=self._worker)
        return self._pool

    def process_request(self, request, client_address):
        if self.pool:
            self.pool.submit(self.process_request_thread, request, client_address)
        else:
            super(_RpcServer, self).process_request(request=request, client_address=client_address)


class _RequestHandler(_SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class RpcServer(object):
    """
        class Server(RpcServer):
            def alive(self):
                 ...

        is_run = RpcServer.run_forever(port=10023, worker=3)

    """
    __is_run: bool = False

    @classmethod
    def run_forever(cls, port: int, worker: int = 1) -> bool:
        if cls.__is_run:
            return cls.__is_run

        def new_rpc_service(obj):
            # 根据指定的 cls  new 一个rpc, 若启动则需要 rpc.serve_forever()
            rpc = _RpcServer(
                addr=('0.0.0.0', port),
                requestHandler=_RequestHandler,
                allow_none=True
            )
            cls.__single = rpc

            rpc.init_pool(worker=worker)
            rpc.register_introspection_functions()
            rpc.register_instance(obj)

            logger.info("RPC server Run....")
            rpc.serve_forever()
            logger.info("RPC server stop....")

        with _threading_Lock():
            if not cls.__is_run:
                #  run rpc server
                _Thread(target=new_rpc_service, kwargs={"obj": cls()}).start()

                cls.__is_run = True
        return cls.__is_run
