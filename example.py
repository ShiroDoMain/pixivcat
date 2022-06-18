import asyncio
import os
from pixivCat.AppApi import AppClient

print("=="*100)
AUTH_TOKEN = "**************************"
PROXY = "socks5h://127.0.0.1:7890"
USER_ID = 69493659
ILLUST_ID = 99057163
NOVEL_ID = 7970737
NOVEL_USER = 23202642
NOVEL_SERIES = 1513531

async def main():
    app = AppClient(refresh_token=AUTH_TOKEN,proxy=PROXY,loop=loop)
    await app.auth()
    test_image = await app.illust_detail(99057205)
    await test_image.download_medium(path="images")
    await test_image


async def download_test():
    app = AppClient(AUTH_TOKEN, proxy=PROXY)
    await app.auth()
    images = await app.illust_ranking()
    while 1:
        images.download_origins("images")
        images = await images.next()
        if not images:
            break

try:
    loop = asyncio.new_event_loop()
    # loop.run_until_complete(download_test())
    loop.run_until_complete(main())
    loop.run_forever()
except:
    os._exit(1)
finally:
    loop.close()
                