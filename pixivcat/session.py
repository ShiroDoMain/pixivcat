import contextvars
from typing import Dict, Union
from aiohttp import ClientSession
from aiohttp.client import ClientResponse
from multidict import CIMultiDict
session = contextvars.ContextVar("session")
main_loop = contextvars.ContextVar("loop")
PROXY = contextvars.ContextVar("proxy")


class Session(ClientSession):
    def __init__(self, proxy: str, *args, **kws) -> None:
        self.proxy = proxy
        PROXY.set(proxy)
        super().__init__(*args, **kws)

    async def _request(self, *args, **kws) -> ClientResponse:
        kws["proxy"] = self.proxy
        return await super()._request(*args, **kws)

    def update_headers(self, headers: Union[CIMultiDict, Dict, None] = None, **kws) -> None:
        """add some new headers"""
        self._default_headers.update(**headers or kws)
