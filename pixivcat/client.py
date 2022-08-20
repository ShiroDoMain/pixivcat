from asyncio import AbstractEventLoop
import asyncio
import hashlib

from pixivcat.base import BaseClient
from .user import User
from .session import Session, session, main_loop, PROXY
from typing import Any, Dict, NoReturn, Optional, Union


class URL:
    url: str

    def __init__(self, url=None) -> None:
        self.url = url

    def __call__(self, path: str, *args: Any, **kwds: Any) -> Any:
        if not path.startswith("/"):
            path += "/"
        return self.url + path


class Client(BaseClient):
    def __init__(self,
                 refresh_token: str = None,
                 proxy: str = None,
                 url: str = None,
                 loop: Optional[AbstractEventLoop] = None
                 ) -> None:
        self._url = URL(url=url)
        self._loop = loop or asyncio.new_event_loop()
        self._session = Session(proxy=proxy, loop=loop)
        session.set(self._session)
        main_loop.set(self._loop)
        self.refresh_token = refresh_token

        self.CLIENT_ID = "MOBrBDS8blbauoSck0ZfDbtuzpyT"
        self.CLIENT_SECRET = "lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj"
        self.encryption = "28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c"

        self.access_token = None
        self.user = None

    @classmethod
    def encrypt(self, data: str, encryption: str = "") -> None:
        mix = data+encryption
        return hashlib.md5(mix.encode("UTF-8")).hexdigest()

    def set_url(self, url: str) -> None:
        self._url = url

    async def request(self, method: str, url: str, **kwds) -> Dict:
        url = self._url(url) if url.startswith("/") else url
        async with self._session.request(method=method, url=url, **kwds) as resp:
            return await self.raise_status_code(resp)

    async def raise_status_code(self, response) -> Union[NoReturn, Dict]:
        if response.status not in (200, 301):
            raise Exception(f"request error, status code {(await response.json())}")
        return await response.json()

    async def auth(self, refresh_token: Optional[str] = None, headers: Dict = None, lang = "zh-cn"):
        """login, use refresh_token"""
        data = {}
        headers = headers or {}
        if not headers.get("user-agent"):
            headers["user-agent"] = "PixivAndroidApp/5.0.234 (Android 11; Pixel 5)"
            headers["Accept-Language"] = lang
        self._session.update_headers(headers)
        data["grant_type"] = "refresh_token"
        data["client_id"] = self.CLIENT_ID
        data["client_secret"] = self.CLIENT_SECRET
        if not refresh_token and not self.refresh_token:
            raise ValueError("no refresh_token")
        data["refresh_token"] = refresh_token or self.refresh_token
        response = await self.request("POST", "https://oauth.secure.pixiv.net/auth/token", data=data, headers=headers)
        if not response:
            # raise no response exception
            raise Exception(f"get auth response error")
        self.access_token = response.get("access_token")
        self._session.update_headers(
            Authorization=f"Bearer {self.access_token}")
        self.user = User(**response.get("user"))

    async def __aenter__(self):
        if self.refresh_token:
            await self.auth()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """wait download complite"""
        while 1:
            tasks = asyncio.all_tasks()
            if len(tasks) <= 1:
                break
            await asyncio.sleep(1)
        if not self._session.closed:
            await self._session.close()
        if not self._loop.is_running():
            self._loop.close()
