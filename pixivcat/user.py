from pixivcat.base import BaseModel, MultiMediaBaseModel, BaseClient
from typing import Dict, List


class User(BaseModel):
    account: str = None
    id: str = None
    is_mail_authorized: bool = None
    is_premium: bool = None
    mail_address: str = None
    name: str = None
    profile_image_urls: Dict = None
    x_restrict: int = None
    sex: str = None


class ProfilePublicity(BaseModel):
    birth_day: str
    birth_year: str
    gender: str
    job: str
    pawoo: bool
    region: str


class Profile(BaseModel):
    address_id: int = None
    background_image_url: str = None
    birth: str = None
    birth_day: str = None
    birth_year: int = None
    country_code: str = None
    gender: str = None
    is_premium: bool = None
    is_using_custom_profile_image: bool = None
    job: str = None
    job_id: int = None
    pawoo_url: str = None
    region: str = None
    total_follow_users: int = None
    total_illust_bookmarks_public: int = None
    total_illust_series: int = None
    total_illusts: int = None
    total_manga: int = None
    total_mypixiv_users: int = None
    total_novel_series: int = None
    total_novels: int = None
    twitter_account: str = None
    twitter_url: str = None
    webpage: str = None


class Workspace(BaseModel):
    chair: str
    comment: str
    desk: str
    desktop: str
    monitor: str
    mouse: str
    music: str
    pc: str
    printer: str
    scanner: str
    tablet: str
    tool: str
    workspace_image_url: str


class Artist(BaseModel):
    id: int
    name: str
    account: str
    profile_image_urls: Dict
    profile: Profile = None
    workspace: Workspace = None
    profile_publicity: ProfilePublicity = None
    comment: str = None
    is_followed: bool = None


class Artists(MultiMediaBaseModel):
    def __init__(self, client: BaseClient, resp: Dict) -> None:
        self.users = [Artist(**artist) for artist in resp.pop("users")]
        super().__init__(client, **resp)
