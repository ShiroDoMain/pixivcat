import asyncio
import os
from typing import Dict, List

from pyparsing import Optional
from pixivcat.base import BaseModel, MultiMediaBaseModel, BaseClient
from .user import Artist
from .session import main_loop, Session, PROXY
from aiohttp.client_exceptions import ClientConnectorError, ServerDisconnectedError, ClientPayloadError, ClientOSError


class Illustration(BaseModel):
    id: int
    title: str
    caption: str
    create_date: str
    height: int
    image_urls: Dict
    is_bookmarked: bool
    is_muted: bool
    meta_pages: List
    meta_single_page: Dict
    page_count: int
    restrict: int
    sanity_level: int
    series: Dict
    tags: List
    tools: List
    total_bookmarks: int
    total_comments: int
    total_view: int
    type: str
    user: Artist
    visible: bool
    width: int
    x_restrict: int

    async def _download(self, url: str, _fn: str, _path: str = None, _session=None) -> None:
        image_type = url.split(".")[-1]
        _fn = _fn if _fn else url.split("/")[-1]
        if not _fn.endswith(image_type):
            _fn = _fn[:-4]+image_type
        _fn = _fn if not _path else _path+_fn
        print(f"{_fn} downloading...")
        while 1:
            try:
                async with _session.get(url, headers={"Referer": "https://app-api.pixiv.net/"}) as resp:
                    if resp.status not in (200, 301):
                        print(f"{_fn} download fail, status code: {resp.status}")
                    data = await resp.read()
                    with open(_fn, "wb") as f:
                        f.write(data)
                    await asyncio.sleep(.1)
            except (
                ClientConnectorError,
                ServerDisconnectedError,
                ClientPayloadError
            ) as e:
                continue
            except Exception as e:
                print(f"download {_fn} error:{str(e)}")
                raise
            else:
                break
        print(f"{_fn} download completed")

    async def download_origin(self, path: str = None, filename: str = None) -> None:
        if not self.meta_pages and not self.meta_single_page:
            return
        if path and not os.path.exists(path):
            os.mkdir(path)
        if path and not path.endswith("/"):
            path += "/"
        origin_urls: List[str] = [self.meta_single_page.get("original_image_url"), ] if self.meta_single_page else [
            url.get("image_urls").get("original") for url in self.meta_pages]
        while 1:
            try:
                async with Session(proxy=PROXY.get()) as session:
                    for url in origin_urls:
                        await self._download(url, filename, path, session)
                        if filename:
                            break
            except ClientOSError as e:
                continue
            return

    async def download_medium(self, medium: str = "medium", filename: str = None, path: str = None):
        """download illust medium
            Args:
                medium(str): square_medium, medium(Default), large
        """
        if not self.image_urls:
            return
        if path and not os.path.exists(path):
            os.mkdir(path)
        if path and not path.endswith("/"):
            path += "/"
        medium_urls: List[str] = [urls.get("image_urls").get(
            medium) for urls in self.meta_pages] if self.meta_pages else [self.image_urls.get(medium), ]
        async with Session(proxy=PROXY.get()) as session:
            for url in medium_urls:
                await self._download(url, filename, path, session)
                if filename:
                    break


class Illustrations(MultiMediaBaseModel):
    def __init__(self, client: "BaseClient", resp: Dict) -> None:
        self.illusts = [Illustration(**illust)
                        for illust in resp.pop("illusts")]
        super().__init__(client=client, **resp)

    def download_origins(self, path: str):
        try:
            main_loop = asyncio.get_running_loop()
        except RuntimeError:
            print("warnning: cannot get running loop")
            main_loop = main_loop.get()
        if not self.illusts:
            return
        for illust in self.illusts:
            main_loop.create_task(illust.download_origin(path=path))

    def download_mediums(self, path: str, medium: str = "medium"):
        """download illust medium
            Args:
                medium(str): square_medium, medium(Default), large
        """
        try:
            main_loop = asyncio.get_running_loop()
        except RuntimeError:
            print("warnning: cannot get running loop")
            main_loop = main_loop.get()
        if not self.illusts:
            return
        for illust in self.illusts:
            main_loop.create_task(
                illust.download_medium(path=path, medium=medium))
