from selenium import webdriver
import undetected_chromedriver as uc

from downedit.utils.common import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .tiktok_api import TiktokAPI


class TikTokExtractor:

    def __init__(self) -> None:
        pass

    def extract_url_from_user(username, folder_path):

        with console.status('[cyan]Starting... please wait!', spinner='line') as status:
            
            options = webdriver.ChromeOptions()
            
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--headless')
            
            driver = uc.Chrome(use_subprocess=True)
            driver.get('https://www.tiktok.com/@' + username)

        try:
            
            with console.status('[cyan]Getting User... please wait!', spinner='line') as status:
                new_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="main-content-others_homepage"]/div/div[2]/div[2]/div/div[1]'))
                )
                new_element.click()
            
            video_count = 0
            
            while True:
                video_count += 1

                with console.status('[cyan]Getting Video... please wait!', spinner='line') as status:
                    
                    button = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div[4]/div/div[1]/button[3]'))
                    )

                    video_url = driver.current_url
                    
                    api = TiktokAPI()
                    
                    download_link, video_title = api.tmate_dl(link=video_url)
                
                video_dl = VideoDL(download_link, folder_path)
                video_dl.download(video_title, folder_path)

                if button.is_enabled():
                    button.click()
                else:
                    driver.quit()
                    return video_count
                
        except Exception as e:
            print(
                f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Error] {Fore.RED}{str(e[:80])}")
        finally:
            driver.quit()
            return video_count