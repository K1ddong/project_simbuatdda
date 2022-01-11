import re
import requests
from bs4 import BeautifulSoup
import os
import urllib
import json
import asyncio
import aiofiles
import aiohttp
import time

# async def img_downloader(session, img):
#     print(img)
#     img_name_process = re.sub('[\/:*?"<>|]', "", (img.split("/")[-1]).split(".")[0])
#     img_name = f"{img_name_process}.jpg"
#     try:
#         os.mkdir(f"./images_{keyword}")
#     except FileExistsError:
#         pass

#     async with session.get(img) as response:
#         if response.status == 200:
#             async with aiofiles.open(
#                 f"./images_{keyword}/{img_name}", mode="wb"
#             ) as file:
#                 img_data = await response.read()
#                 await file.write(requests.get(img_data).content)


# async def fetch(session, urls):
#     async with session.get(urls) as response:
#         result = await response.text()
#         soup = BeautifulSoup(result, "html.parser")
#         images = soup.find_all("a", "iusc")
#         await asyncio.gather(
#             *[
#                 img_downloader(session, str(json.loads(img.get("m"))["murl"]))
#                 for img in images
#             ]
#         )


# async def main():
#     BASE_URL = "https://www.bing.com/images/search"
#     urls = f"{BASE_URL}?q={keyword}"
#     async with aiohttp.ClientSession() as session:
#         await asyncio.gather(
#             *[fetch(session, urls)]
#         )  # , i) for i, url in enumerate(urls)])


def main():
    BASE_URL = "https://www.bing.com/images/search"
    urls = f"{BASE_URL}?q={keyword}"

    # response = requests.get(urls)

    try:
        os.mkdir(f"./images_{input_keyword}")
    except FileExistsError:
        pass

    with requests.Session() as session:
        response = session.get(urls)
        soup = BeautifulSoup(response.text, "html.parser")
        img_tags = soup.find_all("a", "iusc")

        for img_link in img_tags:
            time.sleep(0.1)
            link = img_link.get("m")
            metadata = json.loads(link)["murl"]
            img_data = requests.get(metadata).content
            img_name_process = re.sub(
                '[\/:*?"<>|]', "", (metadata.split("/")[-1]).split(".")[0]
            )
            img_name = f"{img_name_process}.jpg"
            with open(f"./images_{input_keyword}/{img_name}", "wb") as handler:
                handler.write(img_data)

    # img_urls = [img["src"] for img in img_tags]

    # for url in img_urls:
    #     filename = re.search(r"/([\w_-]+[.](jpg|gif|png))$", url)
    #     if not filename:
    #         print("Regex didn't match with the url: {}".format(url))
    #         continue

    #     try:
    #         os.mkdir(f"./images_{keyword}")
    #     except FileExistsError:
    #         pass

    #     with open(f"./images_{keyword}/{filename}", mode="wb") as file:
    #         file.write(requests.get(filename).content)


if __name__ == "__main__":
    input_keyword = input("얻고자 하는 이미지 키워드 : ")
    keyword = urllib.parse.quote(input_keyword)
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # asyncio.run(main())
    main()
