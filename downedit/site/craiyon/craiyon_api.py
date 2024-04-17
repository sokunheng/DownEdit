from colorama import *
import requests
import requests_random_user_agent
import random, string

class CraiyonAPI:
    def __init__(self) -> None:
        self.base_url = "https://api.craiyon.com"
        self.search_endpoint = "/search"
        self.version = "z9j7i0uwg2qhcfyl"
        self.boundary = '----WebKitFormBoundary' + self.generate_boundary()

        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,ko-US;q=0.8,ko;q=0.7,hu-US;q=0.6,hu;q=0.5,km-GB;q=0.4,km;q=0.3',
            'Content-Length': '261',
            'Content-Type': f'multipart/form-data; boundary={self.boundary}',
            'Origin': 'https://www.craiyon.com',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site'
        }

    def generate_boundary(self, length=16):
        valid_chars = string.ascii_letters + string.digits + "-_"
        return ''.join(random.choice(valid_chars) for _ in range(length))
    
    def _generate_user_agent(self):
        with requests.Session() as s:
            return s.headers['User-Agent']

    def search_img(self, prompt):
        user_gen = self._generate_user_agent()
        self.headers['User-Agent'] = user_gen

        multipart_body = (
            f'--{self.boundary}\r\n'
            'Content-Disposition: form-data; name="text"\r\n\r\n'
            f'{prompt}\r\n'
            f'--{self.boundary}\r\n'
            'Content-Disposition: form-data; name="version"\r\n\r\n'
            f'{self.version}\r\n'
            f'--{self.boundary}--\r\n'
        )

        with requests.Session() as s:
            response = s.post(
                self.base_url + self.search_endpoint,
                headers=self.headers,
                data=bytes(multipart_body, 'utf-8')
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
