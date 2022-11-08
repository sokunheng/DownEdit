# download all kuaishou video from user
# date 09/11/2022
# Created by HengSok

import requests
import json
import time
import os
import re
from bs4 import BeautifulSoup
from colorama import *
from pystyle import *
from colorama import *
from rich.traceback import install
from rich.console import Console


install()
console = Console()

PROFILE_URL = "https://live.kuaishou.com/profile/"
DATA_URL = "https://live.kuaishou.com/m_graphql"
WORK_URL = "https://m.gifshow.com/fw/photo/"

class Crawler:

    param_did = ""

    s = requests.Session()
    gen = s.headers['User-Agent']
    headers_web = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Host': 'live.kuaishou.com',
        'Origin': 'https://live.kuaishou.com',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        # User-Agent/Cookie - Modify according to your computer
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        'Cookie': ''
    }
    headers_mobile = {
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36'
    }

    crawl_list = []

    date_cache = ""
    date_pic_count = 0

    def set_did(self, did):
        self.param_did = did
        self.headers_web['Cookie'] = 'did=' + did + "; userId="
        self.headers_mobile['Cookie'] = 'did=' + did
    
    def crawl(self):
        print("Ready to start crawling total of %d users." % len(self.crawl_list))
        time.sleep(1.5)
        for uid in self.crawl_list:
            #self.date_count = 0
            self.__crawl_user(uid)

    def add_to_list(self, uid):
        self.crawl_list.append(uid)

    def __crawl_user(self, uid):

        global res, dir
        if uid.isdigit():
            uid = self.__switch_id(uid)

        payload = {"operationName": "privateFeedsQuery",
                    "variables": {"principalId": uid, "pcursor": "", "count": 999},
                    "query": "query privateFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n  privateFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n    pcursor\n    list {\n      id\n      thumbnailUrl\n      poster\n      workType\n      type\n      useVideoPlayer\n      imgUrls\n      imgSizes\n      magicFace\n      musicName\n      caption\n      location\n      liked\n      onlyFollowerCanComment\n      relativeHeight\n      timestamp\n      width\n      height\n      counts {\n        displayView\n        displayLike\n        displayComment\n        __typename\n      }\n      user {\n        id\n        eid\n        name\n        avatar\n        __typename\n      }\n      expTag\n      __typename\n    }\n    __typename\n  }\n}\n"}
        res = requests.post(DATA_URL, headers=self.headers_web, json=payload)

        works = json.loads(res.content.decode(encoding='utf-8', errors='strict'))['data']['privateFeeds']['list']

        if not os.path.exists("./kuaishou"):
            os.makedirs("./kuaishou")

        # These two lines of code write the response to json for analysis
        # with open(uid + ".json", "w") as fp:
        #     fp.write(json.dumps(works, indent=2))

        # Prevent the user from live broadcast, the first work is live broadcast by default, 
        # resulting in the acquisition of information as NoneType
        # if works[0]['id'] is None:
        #     works.pop(0)
        name = re.sub(r'[\\/:*?"<>|\r\n]+', "", works[0]['user']['name'])

        dir = "kuaishou/" + name + "(" + uid + ")"
        # print(len(works))
        if not os.path.exists(dir):
            os.makedirs(dir)

        # if not os.path.exists(dir + ".list"):
        #     print("")


        print(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] Start crawling users " + name + ", saved in " + dir)
        print(f"""\n{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.RED}@{name} {Fore.YELLOW}Have Published {Fore.BLUE}{str(len(works))} {Fore.YELLOW}works. Downloading them...""")
        console.log("[cyan][Status][/cyan] Already Downloaded Videos Will Be Skipped.\n")
        # for j in range(len(works)):
        #     self.__crawl_work(dir, works[j], j + 1)
        #     time.sleep(1)
        self.__crawl_work()

        console.log("[cyan][Status][/cyan] Completed crawling " + name + " user.")
        time.sleep(1)

    def __switch_id(self, uid):
        payload = {"operationName": "SearchOverviewQuery",
                   "variables": {"keyword": uid, "ussid": None},
                   "query": "query SearchOverviewQuery($keyword: String, $ussid: String) {\n  pcSearchOverview(keyword: $keyword, ussid: $ussid) {\n    list {\n      ... on SearchCategoryList {\n        type\n        list {\n          categoryId\n          categoryAbbr\n          title\n          src\n          __typename\n        }\n        __typename\n      }\n      ... on SearchUserList {\n        type\n        ussid\n        list {\n          id\n          name\n          living\n          avatar\n          sex\n          description\n          counts {\n            fan\n            follow\n            photo\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      ... on SearchLivestreamList {\n        type\n        lssid\n        list {\n          user {\n            id\n            avatar\n            name\n            __typename\n          }\n          poster\n          coverUrl\n          caption\n          id\n          playUrls {\n            quality\n            url\n            __typename\n          }\n          quality\n          gameInfo {\n            category\n            name\n            pubgSurvival\n            type\n            kingHero\n            __typename\n          }\n          hasRedPack\n          liveGuess\n          expTag\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}

        res = requests.post(DATA_URL, headers=self.headers_web, json=payload)
        dt = json.loads(res.content.decode(encoding='utf-8', errors='strict'))['data']
        # with open("data/jj_" + uid + ".json", "w") as fp:
        #     fp.write(json.dumps(dt, indent=2))

        return dt['pcSearchOverview']['list'][1]['list'][0]['id']

    def __crawl_work(self):

        list = json.loads(res.content.decode(encoding='utf-8', errors='strict'))['data']['privateFeeds']['list']
        count = 0

        for video in list:

            count += 1
            item = video["id"]
            url = f"https://www.videofk.com/https://www.kuaishou.com/short-video/{item}"
            header = {
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8 rv:4.0) Gecko/20140131 Firefox/35.0"
            }
            link = requests.get(url=url, headers=header)
            soup = BeautifulSoup(link.content, 'html.parser')
            download_url = soup.select('.video_files > div:nth-child(2) > a:nth-child(1)')[0]['href']

            start = time.time()
            # data size of each download                                        
            chunk_size = 1024

            if not os.path.exists(f"{dir} + "/"+ {item}.mp4"):

                video_bytes = requests.get(download_url, stream=True)
                total_length = int(video_bytes.headers.get("Content-Length"))
                console.log(f"[green][Status][/green] File size: " + "{size:.2f} MB".format(size = total_length / chunk_size /1024)) 
                with open(f'{dir} + "/"+ {item}.mp4', 'wb') as out_file:
                    out_file.write(video_bytes.content)
                    end = time.time()

                    print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Timelapse:{Fore.YELLOW}"+ " %.2fs" % (end - start))
                    print(f"""{Fore.CYAN}[Programs] {Fore.YELLOW}[File] {Fore.GREEN}{item}.mp4{Fore.YELLOW} Downloaded\n""")
                    time.sleep(0.7)
            else:
                print(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[File] {Fore.GREEN}{item}.mp4{Fore.WHITE} already exists! Skipping...\n")
                time.sleep(0.7) 
                continue
        time.sleep(1) 
        console.log(f"[cyan][Status][/cyan] Successfully downloaded [green]{count}[/green] videos ✓")

def crawl():
    crawler = Crawler()

    param_did = input(f"{Fore.YELLOW}Input Your Cookie 'did':{Fore.WHITE} ")
    crawler.set_did(param_did)

    uid = input(f"{Fore.YELLOW}Enter User ID:{Fore.WHITE} ")
    crawler.add_to_list(uid)

    crawler.crawl()

    print(input(f"\n{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))

if __name__ == "__main__":

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
    print(Box.DoubleCube(f"""Example Below\nCookie 'did': web_ff20177777baea2a2808135f0595b77f \nUser ID: 3xnpgvvuei3umwk"""))
    crawl()
