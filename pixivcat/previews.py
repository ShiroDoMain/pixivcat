from typing import Dict, List
from pixivcat.base import BaseModel, MultiMediaBaseModel, BaseClient
from .user import Artist
from .illust import Illustration


class Preview(BaseModel):
    user: Artist
    illusts: List[Illustration]
    novels: list
    is_muted: bool

    def __init__(self, **kwds) -> None:
        self.illusts = [Illustration(**illust)
                        for illust in kwds.pop("illusts")]
        super().__init__(**kwds)


class Previews(MultiMediaBaseModel):
    def __init__(self, client: BaseClient, resp: Dict) -> None:
        self.previews = [Preview(**preview)
                         for preview in resp.pop("user_previews")]
        super().__init__(client=client, **resp)
