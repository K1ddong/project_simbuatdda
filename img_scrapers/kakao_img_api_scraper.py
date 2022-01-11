import aiohttp
import asyncio
import aiofiles
import os
import urllib.request
import re
from config import get_secret


async def img_downloader(session, img):
    img_name_process = re.sub('[\/:*?"<>|]', "", (img.split("/")[-1]).split(".")[0])
    img_name = f"{img_name_process}.jpg"
    try:
        os.mkdir(f"./images_{keyword}")
    except FileExistsError:
        pass

    async with session.get(img) as response:
        if response.status == 200:
            async with aiofiles.open(
                f"./images_{keyword}/{img_name}", mode="wb"
            ) as file:
                img_data = await response.read()
                await file.write(img_data)


async def fetch(session, url, i):
    print(i + 1)
    headers = {
        "Authorization": get_secret("KAKAO_API_ID"),
    }
    try:
        async with session.get(url, headers=headers) as response:
            result = await response.json()
            documents = result["documents"]
            images = [document["image_url"] for document in documents]
            await asyncio.gather(*[img_downloader(session, img) for img in images])
    except Exception as ex:
        print(ex)
        pass


async def main():
    BASE_URL = "https://dapi.kakao.com/v2/search/image"
    urls = [f"{BASE_URL}?query={keyword}&size=20&page={i}" for i in range(1, 11)]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[fetch(session, url, i) for i, url in enumerate(urls)])


if __name__ == "__main__":
    input_keyword = input("얻고자 하는 이미지 키워드 : ")
    keyword = urllib.parse.quote(input_keyword)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
