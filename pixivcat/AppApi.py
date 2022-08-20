from pixivcat.user import Artists
from pixivcat.comments import Comments
from pixivcat.client import Client
from typing import Dict, List, Optional
from asyncio import AbstractEventLoop
from pixivcat.illust import Illustration, Illustrations
from pixivcat.novel import Novel, NovelSeries, Novels
from pixivcat.previews import Previews
from pixivcat.user import Artist, Profile, ProfilePublicity, Workspace
from pixivcat.bookmark import BookmarkDetail, Bookmarks
from pixivcat.tag import Tag


class AppClient(Client):
    url: str = "https://app-api.pixiv.net"

    def __init__(self, refresh_token: str = None, proxy: str = None, url: str = url, loop: Optional[AbstractEventLoop] = None) -> None:
        super().__init__(refresh_token, proxy, url, loop)

    async def user_detail(self, user_id: int, **kws) -> Artist:
        """Get user information by user ID"""
        response = await self.request("GET", f"/v1/user/detail?user_id={user_id}")
        artist = Artist(**response.get("user"))
        artist.profile = Profile(**response.get("profile"))
        artist.profile_publicity = ProfilePublicity(
            **response.get("profile_publicity"))
        artist.workspace = Workspace(**response.get("workspace"))
        return artist

    async def user_illusts(self, user_id: int, type: str = "illust") -> Illustrations:
        """Get user illustrations by user ID"""
        response = await self.request("GET", f"/v1/user/illusts?user_id={user_id}&type={type}")
        return Illustrations(self, response)

    async def user_bookmarks_illust(self, user_id: int, restrict="public", max_bookmark_id=None, tag=None) -> Illustrations:
        """Get user bookmarks by user ID"""
        params = f"?user_id={user_id}&restrict={restrict}"
        params += f"&max_bookmark_id={max_bookmark_id}" if max_bookmark_id else ""
        params += f"&tag={tag}" if tag else ""
        response = await self.request("GET", f"/v1/user/bookmarks/illust{params}")
        return Illustrations(self, response)

    async def user_related(self, seed_user_id: int, offset: int = 0) -> Previews:
        """Get user related previews by ...by user Id"""
        response = await self.request("GET", f"/v1/user/related?seed_user_id={seed_user_id}&offset={offset}")
        return Previews(self, response)

    async def illust_follow(self, restrict: str = "public", offset: int = 0) -> Illustrations:
        """Get to follow the illustrations of the artist"""
        response = await self.request("GET", f"/v2/illust/follow?restrict={restrict}&offset={offset}")
        return Illustrations(self, response)

    async def illust_detail(self, illust_id) -> Illustration:
        """get illust detail"""
        response = await self.request("GET", f"/v1/illust/detail?illust_id={illust_id}")
        return Illustration(**response.get("illust"))

    async def illust_comments(self, illust_id, offset: int = 0, include_total_comments: bool = True) -> Comments:
        """get illust comments"""
        response = await self.request("GET", f"/v1/illust/comments?illust_id={illust_id}&offset={offset}&includ_total_comments={str(include_total_comments).lower()}")
        return Comments(self, **response)

    async def illust_related(self, illust_id, offset: int = 0, seed_illust_ids: list = None) -> Illustrations:
        """Get user related previews by illust Id"""
        response = await self.request("GET", f"/v2/illust/related?illust_id={illust_id}&offset={offset}{'&seed_illust_ids='+str(seed_illust_ids) if seed_illust_ids else ''}")
        return Illustrations(self, response)

    async def illust_recommended(self,
                                 content_type="illust",
                                 offset: int = 0,
                                 include_ranking_label: bool = True,
                                 max_bookmark_id_for_recommend: int = None,
                                 min_bookmark_id_for_recent_illust: int = None,
                                 include_ranking_illusts: bool = None,
                                 bookmark_illust_ids: List[str] = None,
                                 include_privacy_policy: str = None
                                 ) -> Illustrations:
        """get illust recommend"""
        params = f"?content_type={content_type}&include_ranking_label={str(include_ranking_label).lower()}&offset={offset}"
        params += f"&max_bookmark_id_for_recommend={max_bookmark_id_for_recommend}" if max_bookmark_id_for_recommend else ''
        params += f"&min_bookmark_id_for_recent_illust={min_bookmark_id_for_recent_illust}" if min_bookmark_id_for_recent_illust else ''
        params += f"&include_ranking_illusts={str(include_ranking_illusts).lower()}" if include_ranking_illusts else ''
        params += f"&bookmark_illust_ids={','.join(bookmark_illust_ids)}" if bookmark_illust_ids else ''
        params += f"&include_privacy_policy={include_privacy_policy}" if include_privacy_policy else ''
        response = await self.request("GET", "/v1/illust/recommended"+params)
        return Illustrations(self, response)

    async def illust_ranking(self, mode: str = 'day', offset: int = 0, date: str = None) -> Illustrations:
        """get illusts rank

        Args:
            mode(str): day, week, month, day_male, day_female, week_original, week_rookie, day_r18, day_male_r18, day_female_r18, week_r18, week_r18g
            date(str): eg:2022-01-01

        """
        response = await self.request("GET", f"/v1/illust/ranking?mode={mode}&offset={offset}{f'&date={date}' if date else ''}")
        return Illustrations(self, response)

    async def trending_tags_illust(self) -> List[Tag]:
        """get trending tags"""
        response = await self.request("GET", "/v1/trending-tags/illust")
        return [Tag(**tag) for tag in response.get("trend_tags")]

    async def search_illust(self,
                            word: str,
                            search_target: str = 'partial_match_for_tags',
                            sort: str = 'date_desc',
                            offset: int = 0,
                            duration: str = "within_last_day",
                            start_date: str = None,
                            end_date: str = None) -> Illustrations:
        """search illust by word

            Args:

                word(str): search keyword

                search_target(str): 

                    partial_match_for_tags -> partial match tags
                    exact_match_for_tags -> full match tags
                    title_and_caption -> title match

                sort(str): date_desc, date_asc, popular_desc

                duration(str): within_last_day, within_last_week, within_last_month

                start_date/end_date (str):... you know...be like "2022-01-01"
        """
        params = f"?word={word}&search_target={search_target}&sort={sort}&offset={offset}"
        params += f"&duration={duration}" if duration else ""
        params += f"&start_date={start_date}" if start_date else ""
        params += f"&end_date={end_date}" if end_date else ""
        response = await self.request("GET", "/v1/search/illust"+params)
        return Illustrations(self, response)

    async def search_novel(self,
                           word: str,
                           search_target: str = 'partial_match_for_tags',
                           sort: str = 'date_desc',
                           offset: int = 0,
                           merge_plain_keyword_results: bool = True,
                           include_translated_tag_results: bool = True,
                           start_date=None,
                           end_date=None,
                           ) -> Novels:
        """search novel by word

            Args:

                word(str): search keyword

                search_target(str): 

                    partial_match_for_tags -> partial match tags
                    exact_match_for_tags -> full match tags
                    keyword -> keyword match
                    text -> text match

                sort(str): date_desc, date_asc, popular_desc

                start_date/end_date (str):... you know...be like "2022-01-01"

        """
        params = f"?word={word}&search_target={search_target}&sort={sort}&offset={offset}"
        params += f"&merge_plain_keyword_results={str(merge_plain_keyword_results).lower()}"
        params += f"&include_translated_tag_results={str(include_translated_tag_results).lower()}"
        params += f"&start_date={start_date}" if start_date else ""
        params += f"&end_date={end_date}" if end_date else ""
        response = await self.request("GET", "/v1/search/novel"+params)
        return Novels(self, response)

    async def search_user(
        self,
        word: str,
        offset: int = 0,
        sort: str = 'date_desc',
        duration: str = "within_last_day"
    ):
        """search user by word

            Args:

                word(str): search keyword

                sort(str): date_desc, date_asc, popular_desc

                duration(str): within_last_day, within_last_week, within_last_month
        """
        params = f"?word={word}&offset={offset}&sort={sort}&duration={duration}"
        response = await self.request("GET", "/v1/search/user"+params)
        return Previews(self, response)

    async def illust_bookmark_detail(self, illust_id: int) -> BookmarkDetail:
        response = await self.request("GET", f"/v2/illust/bookmark/detail?illust_id={illust_id}")
        return BookmarkDetail(**response.get("bookmark_detail"))

    async def illust_bookmark_add(self, illust_id: int, restrict: str = "public", tags: List[str] = None) -> None:
        """add bookmark by illust id"""
        data = {
            "illust_id": illust_id,
            "restrict": restrict
        }
        if tags:
            data.update({"tags[]": ",".join(tags)})
        await self.request("POST", f"/v2/illust/bookmark/add", data=data)

    async def illust_bookmark_delete(self, illust_id: int) -> None:
        """delete bookmark by illust id"""
        await self.request("POST", "/v1/illust/bookmark/delete", data={"illust_id": illust_id})

    async def user_follow_add(self, user_id: int, restrict: int = "public") -> None:
        """follow user by user_id"""
        await self.request("POST", "/v1/user/follow/add", data={"user_id": user_id, "restrict": restrict})

    async def user_follow_delete(self, user_id: int) -> None:
        """unfollow user by user id"""
        await self.request("POST", "/v1/user/follow/delete", data={"user_id": user_id})

    async def user_bookmark_tags_illust(self,  restrict: str = 'public', offset: int = 0) -> Bookmarks:
        """get user bookmark tags"""
        response = await self.request("GET", f"/v1/user/bookmark-tags/illust?restrict={restrict}&offset={offset}")
        return Bookmarks(self, **response)

    # TODO
    async def user_following(self, user_id: int, restrict='public', offset: int = 0) -> Previews:
        """Get user following"""
        response = await self.request("GET", f"/v1/user/following?user_id={user_id}&restrict={restrict}&offset={offset}")
        return Previews(self, response)

    async def user_follower(self, user_id: int, offset: int = 0) -> Previews:
        """get user flowers by user_id"""
        response = await self.request("GET", f"/v1/user/follower?user_id={user_id}&offset={offset}")
        return Previews(self, response)

    async def user_mypixiv(self, user_id: int, offset: int = 0) -> Previews:
        """Get my pixiv friend by user id"""
        response = await self.request("GET", f"/v1/user/mypixiv?user_id={user_id}&offset={offset}")
        return Previews(self, response)

    async def user_blacklist(self, user_id: int, offset: int = 0) -> Artists:
        """get black list by user id"""
        response = await self.request("GET", f"/v2/user/list?user_id={user_id}&offset={offset}")
        return Artists(self, response)

    async def ugoira_metadata(self, illust_id: int):
        """Get ugoira metadata by illust_id"""
        response = await self.request("GET", f"/v1/ugoira/metadata?illust_id={illust_id}")
        return response

    async def user_novels(self, user_id: int, offset: int = 0) -> Novels:
        """Get user novels by user id"""
        response = await self.request("GET", f"/v1/user/novels?user_id={user_id}&offset={offset}")
        return Novels(self, response)

    async def novel_series(self, series_id: int, last_order: str = None) -> NovelSeries:
        """Get novels series detail"""
        response = await self.request("GET", f"/v2/novel/series?series_id={series_id}{f'&last_order={last_order}' if last_order else ''}")
        return NovelSeries(self, response)

    async def novel_detail(self, novel_id: int) -> Novel:
        """Get novel detail with novel id"""
        response = await self.request("GET", f"/v2/novel/detail?novel_id={novel_id}")
        return Novel(**response.get("novel"))

    async def novel_text(self, novel_id: int) -> Dict:
        response = await self.request("GET", f"/v1/novel/text?novel_id={novel_id}")
        response["series_prev"] = Novel(**response.pop("series_prev"))
        response["series_next"] = Novel(**response.pop("series_next"))
        return response

    async def illust_new(self, content_type: str = "illust", max_illust_id=None) -> Illustrations:
        """Get new illust"""
        response = await self.request("GET", f"/v1/illust/new?content_type={content_type}{f'&max_illust_id={max_illust_id}' if max_illust_id else ''}")
        return Illustrations(self, response)

    async def article(self, article_id: int):
        """Get articie"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Referer": "https://www.pixiv.net"
        }
        response = self.request(
            "GET", f"https://www.pixiv.net/ajax/showcase/article?article_id={article_id}", headers=headers)
        return response
