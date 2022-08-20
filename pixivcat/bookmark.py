from typing import List
from pixivcat.base import BaseModel, BaseClient, MultiMediaBaseModel


class BookmarkDetail(BaseModel):
    is_bookmarked: bool
    tags: List
    restrict: str


class Bookmarks(MultiMediaBaseModel):
    bookmark_tags: List

    def __init__(self, client: BaseClient, **kwds) -> None:
        super().__init__(client, **kwds)
