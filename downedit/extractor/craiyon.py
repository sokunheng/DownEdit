import tempfile
import time
from selenium import webdriver
import undetected_chromedriver as uc

from rich.console import Console
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

console = Console()

class CraiyonExtractor:
    
    def __init__(self) -> None:
        pass
    
    def extract_img_from_ai(self, url, prompt):
                    
        try:
             
            with console.status('[cyan]Starting... please wait!', spinner='line') as status:
                
                options = webdriver.ChromeOptions()
                # options.add_argument('--no-sandbox')
                # options.add_argument('--disable-dev-shm-usage')
                # options.add_argument('--ignore-certificate-errors')
                # options.add_argument('--allow-running-insecure-content')
                # options.add_argument('--headless')
                
                driver = uc.Chrome()
                driver.get(url)

            
            # with console.status('[cyan]Generating Images... please wait!', spinner='line') as status:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="app"]'))
                )    
                
                javascript_code = '''
                    const base_url = "https://api.craiyon.com";
                    const search_endpoint = "/search";
                    const version = "z9j7i0uwg2qhcfyl";
                    const boundary = '----WebKitFormBoundary' + generateBoundary();

                    const headers = {
                        'Accept': '*/*',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'en-US,en;q=0.9,ko-US;q=0.8,ko;q=0.7,hu-US;q=0.6,hu;q=0.5,km-GB;q=0.4,km;q=0.3',
                        'Content-Type': `multipart/form-data; boundary=${boundary}`,
                        'Origin': 'https://www.craiyon.com',
                        'Sec-Ch-Ua-Mobile': '?0',
                        'Sec-Ch-Ua-Platform': '"Windows"',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-site'
                    };

                    function generateBoundary(length = 16) {
                        const validChars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_';
                        let result = '';
                        for (let i = 0; i < length; i++) {
                            result += validChars.charAt(Math.floor(Math.random() * validChars.length));
                        }
                        return result;
                    }

                    function genImg(prompt) {

                        const multipartBody = `--${boundary}\r\n`
                            + 'Content-Disposition: form-data; name="text"\r\n\r\n'
                            + `${prompt}\r\n`
                            + `--${boundary}\r\n`
                            + 'Content-Disposition: form-data; name="version"\r\n\r\n'
                            + `${version}\r\n`
                            + `--${boundary}--\r\n`;

                        fetch(base_url + search_endpoint, {
                            method: 'POST',
                            headers: headers,
                            body: multipartBody
                        })
                        .then(response => {
                            if (response.ok) {
                                return response.json();
                            } else {
                                throw new Error('Request failed');
                            }
                        })
                        .then(data => {
                            console.log(data);
                            // Process the response data here
                        })
                        .catch(error => {
                            console.error('Error:', error);
                        });
                    }

                    ''' + f'genImg("{prompt}");'
                    
                driver.execute_script(javascript_code)
                time.sleep(5) 
                
        except Exception as e:
            print(
                f"[Programs] [Error] {str(e[:80])}")
        finally:
            driver.quit()
            return []