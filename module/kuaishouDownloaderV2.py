# download all video from user kuaishou no watermark
# created by HengSok

import requests
import json
import os
import time
import re
from rich.console import Console
from colorama import *
from requests_html import HTMLSession
import requests_random_user_agent
from pystyle import *


console  = Console()

def downKuai():

    cookie = input(f"{Fore.YELLOW}Input Your Cookie:{Fore.WHITE} ")
    uid = input(f"{Fore.YELLOW}Enter User ID:{Fore.WHITE} ")
    header = {
        'content-type': 'application/json',
        # Paste your cookies here
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }
    payload = {"operationName": "privateFeedsQuery",
                "variables": {"principalId": uid, "pcursor": "", "count": 999},
                "query": "query privateFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n  privateFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n    pcursor\n    list {\n      id\n      thumbnailUrl\n      poster\n      workType\n      type\n      useVideoPlayer\n      imgUrls\n      imgSizes\n      magicFace\n      musicName\n      caption\n      location\n      liked\n      onlyFollowerCanComment\n      relativeHeight\n      timestamp\n      width\n      height\n      counts {\n        displayView\n        displayLike\n        displayComment\n        __typename\n      }\n      user {\n        id\n        eid\n        name\n        avatar\n        __typename\n      }\n      expTag\n      __typename\n    }\n    __typename\n  }\n}\n"}

    res = requests.post("https://live.kuaishou.com/m_graphql", headers=header, json=payload, timeout=15)

    print(res.status_code)
    works = json.loads(res.content.decode(encoding='utf-8', errors='strict'))['data']['privateFeeds']['list']

    if len(works) == 0:
        print(f"{Fore.CYAN}[Programs] {Fore.RED}[Status] {Fore.RED}Error connection, {Fore.WHITE}please try again!")
    else:
        if not os.path.exists("./kuaishou"):
            os.makedirs("./kuaishou")

        # These two lines of code write the response to json for analysis
        # with open(uid + ".json", "w") as fp:
        #     fp.write(json.dumps(works, indent=2))

        # Prevent the user from live broadcast, the first work is live broadcast by default, 
        # resulting in the acquisition of information as NoneType
        # if works[0]['id'] is None:
        #     works.pop(0)
        try: 
            name = re.sub(r'[\\/:*?"<>|\r\n]+', "", works[0]['user']['name'])

            dir = "kuaishou/" + name

            if not os.path.exists(dir):
                os.makedirs(dir)
        except IndexError as e:
            print(f"{Fore.CYAN}[Programs] {Fore.RED}[Status] {Fore.WHITE}Error:{Fore.RED}", e)
            time.sleep(1)

        print(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Start crawling users {Fore.GREEN}{name}{Fore.WHITE}, saved in {Fore.GREEN}" + dir)
        print(f"""\n{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.RED}@{name} {Fore.YELLOW}Have Published {Fore.BLUE}{str(len(works))} {Fore.YELLOW}videos. Downloading them...""")
        console.log("[cyan][Status][/cyan] Already Downloaded Videos Will Be Skipped.\n")

        # Official API
        # clientCacheKey2 = video["id"]
        # videourl = 'https://www.kuaishou.com/short-video/' + clientCacheKey2

        # data = {
        #     "operationName": "visionVideoDetail",
        #     "variables": {
        #         "photoId": clientCacheKey2,
        #         "page": "detail",
        #     },
        #     "query": "query visionVideoDetail($photoId: String, $type: String, $page: String, $webPageArea: String) {\n  visionVideoDetail(photoId: $photoId, type: $type, page: $page, webPageArea: $webPageArea) {\n    status\n    type\n    author {\n      id\n      name\n      following\n      headerUrl\n      __typename\n    }\n    photo {\n      id\n      duration\n      caption\n      likeCount\n      realLikeCount\n      coverUrl\n      photoUrl\n      liked\n      timestamp\n      expTag\n      llsid\n      viewCount\n      videoRatio\n      stereoType\n      croppedPhotoUrl\n      manifest {\n        mediaType\n        businessType\n        version\n        adaptationSet {\n          id\n          duration\n          representation {\n            id\n            defaultSelect\n            backupUrl\n            codecs\n            url\n            height\n            width\n            avgBitrate\n            maxBitrate\n            m3u8Slice\n            qualityType\n            qualityLabel\n            frameRate\n            featureP2sp\n            hidden\n            disableAdaptive\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    tags {\n      type\n      name\n      __typename\n    }\n    commentLimit {\n      canAddComment\n      __typename\n    }\n    llsid\n    danmakuSwitch\n    __typename\n  }\n}\n"
        # }

        # data = json.dumps(data)

        # response = requests.post('https://www.kuaishou.com/graphql', headers=header, data=data)
        # response.encoding = 'zh-CN'

        # json_data = response.json()

        # data_title = str(json_data['data']['visionVideoDetail']['photo']['caption']).replace("r'[\/\\\:\*\?\"\<\>\|]'",'')
        # data_url = json_data['data']['visionVideoDetail']['photo']['photoUrl']
        # name = json_data['data']['visionVideoDetail']['author']['name']

        count = 0
        for video in works:

            if video['id'] is None:
                break
            else:
                pass
            item = video["id"]
            w_caption = re.sub(r"\s+", " ", video['caption'])
            w_name = re.sub(r'[\\/:*?"<>|\r\n]+', "", w_caption)[0:39]
            print(f"""{Fore.CYAN}[Programs] {Fore.YELLOW}[Title] {Fore.GREEN}{w_name}\r""")

            AttributeError = False
            while not AttributeError:
                try:
                    url = f"https://www.videofk.com/https://www.kuaishou.com/short-video/{item}"
                    s = requests.Session()
                    gen = s.headers['User-Agent']
                    header = {
                        'User-Agent': gen
                    }
                    session = HTMLSession()
                    link = session.get(url=url, headers=header)
                    time.sleep(1)
                    sel = '#wrap > div.body-result > div > div.video_item_body > div > div.video_info > div.video_files > div > a'
                    get = link.html.find(sel, first=True).absolute_links
                    break         
                except:
                    time.sleep(0.2)
                    pass

            start = time.time()
            # Initialize downloaded size                                     
            size = 0     
            # data size of each download                                        
            chunk_size = 1024

            for download_url in get:

                if not os.path.exists(dir + '/' + f"{str(w_caption)}.mp4"):

                    video_bytes = requests.get(download_url, stream=True)
                    total_length = int(video_bytes.headers.get("Content-Length"))
                    console.log(f"[green][Status][/green] File size: " + "{size:.2f} MB".format(size = total_length / chunk_size /1024)) 
                    with open(dir + '/' + f"{w_caption}.mp4", 'wb') as out_file:
                        out_file.write(video_bytes.content)
                        end = time.time()

                    print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Timelapse:{Fore.YELLOW}"+ " %.2fs" % (end - start))
                    print(f"""{Fore.CYAN}[Programs] {Fore.YELLOW}[File] {Fore.GREEN}{item}.mp4{Fore.YELLOW} {Fore.WHITE}Downloaded ✓\n""")
                    time.sleep(1)
                else:
                    print(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[File] {Fore.GREEN}{item}.mp4{Fore.WHITE} already exists! Skipping...\n")
                    time.sleep(1) 
                    continue
            count += 1
        time.sleep(1) 
        console.log(f"[cyan][Status][/cyan] Successfully downloaded [green]{count}[/green] videos ✓")
        time.sleep(0.8)
        print(input(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))

if __name__ == "__main__":
    os.system('cls')
    banner = f"""{Fore.MAGENTA} 
██╗░░██╗██╗░░░██╗░█████╗░██╗░██████╗██╗░░██╗░█████╗░██╗░░░██╗░░░░░░██████╗░██╗░░░░░
██║░██╔╝██║░░░██║██╔══██╗██║██╔════╝██║░░██║██╔══██╗██║░░░██║░░░░░░██╔══██╗██║░░░░░
█████═╝░██║░░░██║███████║██║╚█████╗░███████║██║░░██║██║░░░██║█████╗██║░░██║██║░░░░░
██╔═██╗░██║░░░██║██╔══██║██║░╚═══██╗██╔══██║██║░░██║██║░░░██║╚════╝██║░░██║██║░░░░░
██║░╚██╗╚██████╔╝██║░░██║██║██████╔╝██║░░██║╚█████╔╝╚██████╔╝░░░░░░██████╔╝███████╗
╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝╚═╝╚═════╝░╚═╝░░╚═╝░╚════╝░░╚═════╝░░░░░░░╚═════╝░╚══════╝
                                  by HengSok
    """
    print(Center.XCenter(banner))
    print(f'{Fore.GREEN}')
    print(Box.DoubleCube(f"""Example Below\nCookie: kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; did=web_dfe556cf2a8....\nUser ID: 3xnpgvvuei3umwk"""))
    downKuai()
