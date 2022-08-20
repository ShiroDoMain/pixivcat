from typing import List
from pixivcat.base import BaseModel
from .client import BaseClient


class Comments(BaseModel):
    total_comments: int
    commenets: List
    next_url: str
    comment_access_control: int

    def __init__(self, client: BaseClient, **kws) -> None:
        self.client = client
        super().__init__(**kws)

    async def next(self) -> "Comments":
        response = await self.client.request("GET", self.next_url)
        return Comments(client=self.client, **response)
