from typing import Dict, List, Optional
from pixivcat.base import BaseModel, MultiMediaBaseModel
from pixivcat.user import Artist
from pixivcat.client import BaseClient


class Novel(BaseModel):
    id: int
    title: str
    caption: str
    restrict: int
    x_restrict: int
    is_original: bool
    image_urls: Dict
    create_date: str
    tags: List
    page_count: int
    text_length: int
    user: Artist
    series: Dict
    is_bookmarked: bool
    total_bookmarks: int
    total_view: int
    visible: bool
    total_comments: int
    is_muted: bool
    is_mypixiv_only: bool
    is_x_restricted: bool


class Novels(MultiMediaBaseModel):
    def __init__(self, client: BaseClient, resp: Dict) -> None:
        self.novels = [Novel(**novel) for novel in resp.pop("novels")]
        super().__init__(client=client, **resp)


class NovelSeriesDetail(BaseModel):
    id: int
    title: str
    caption: str
    is_original: bool
    is_concluded: bool
    content_count: int
    total_character_count: int
    user: Artist
    display_text: str


class NovelSeries(MultiMediaBaseModel):
    def __init__(self, client: BaseClient, resp: Dict) -> None:
        self.novel_series_detail = NovelSeriesDetail(
            **resp.pop("novel_series_detail"))
        self.novel_series_first_novel = Novel(
            **resp.pop("novel_series_first_novel"))
        self.novel_series_latest_novel = Novel(
            **resp.pop("novel_series_latest_novel"))
        self.novels = [Novel(**novel) for novel in resp.pop("novels")]
        super().__init__(client, **resp)
