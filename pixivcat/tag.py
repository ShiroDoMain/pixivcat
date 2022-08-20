from pixivcat.base import BaseModel
from .illust import Illustration


class Tag(BaseModel):
    tag: str
    translated_name: str
    illust: Illustration
