import asyncio
import os
from pixivcat.AppApi import AppClient

print("=="*100)
REFRESH_TOKEN = "xxx"
PROXY = "socks5h://127.0.0.1:7890"
ILLUST_ID = 99057163
NOVEL_ID = 7970737
NOVEL_USER_ID = 23202642
NOVEL_SERIES = 1513531


async def main():
    app = AppClient(refresh_token=REFRESH_TOKEN, proxy=PROXY, loop=loop)
    async with app:
        test_image = await app.illust_detail(98461062)
        print(",".join([tag.get('translated_name') or "null" for tag in test_image.tags]))
        # await test_image.download_medium(path="images")
        # await test_image


async def download_test():
    app = AppClient(REFRESH_TOKEN, proxy=PROXY)
    async with app:
        images = await app.illust_ranking()
        # while 1:
        images.download_origins("images")
        # images = await images.next()
        # if not images:
        #     break

loop = asyncio.new_event_loop()
loop.run_until_complete(main())
# loop.run_until_complete(main())
if not loop.is_closed():
    loop.close()
