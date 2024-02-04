

import os
import random

from colorama import *
import requests
from bs4 import BeautifulSoup
import requests_random_user_agent

class TiktokAPI:
    
    def __init__(self) -> None:
        self.tmate_url = "https://tmate.cc/"
        self.douyin_wtf_url = "https://api.douyin.wtf/api?url={link}&minimal=true"
        
    def douyin_wtf(self, link, video_quality="720p"):

        response = requests.get(self.douyin_wtf_url.format(link=link))
        
        if response.status_code == 200:
            data = response.json()
            
            if video_quality == "1080p" or video_quality == "720p":
                download_link = data["nwm_video_url_HQ"]
            else:
                download_link = data["nwm_video_url"]
        else:
            download_link = None

        return download_link 
    
    def tmate_dl(self, link, video_quality=None):
        
        with requests.Session() as s:
            
            user_gen = s.headers['User-Agent']
            
            self.tmate_headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://tmate.cc',
                'Connection': 'keep-alive',
                'Referer': 'https://tmate.cc/',
                'User-Agent': user_gen
            }
            
            response = s.get(self.tmate_url, headers=self.tmate_headers)
            
            download_link = None
            video_title = None

            if response.status_code == 200:
                
                soup = BeautifulSoup(response.content, 'html.parser')

                token = soup.find("input", {"name": "token"})["value"]

                data = {'url': link, 'token': token}

                response = s.post('https://tmate.cc/download', headers=self.tmate_headers, data=data)

                if response.status_code == 200:
                    
                    soup = BeautifulSoup(response.content, 'html.parser')

                    title_element = soup.select_one('#download-box > div.downtmate.mb-10 > div.downtmate-middle.center > div > h1 > a')
                    video_title = title_element.text if title_element else None

                    download_link = soup.find(class_="downtmate-right is-desktop-only right").find_all("a")[0]["href"]

        return download_link, video_title
                