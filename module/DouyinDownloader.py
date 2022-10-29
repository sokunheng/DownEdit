# download all douyin video from user
# Created by HengSok

import requests,json,os,time,re
from pystyle import *
from moviepy.editor import * 
from colorama import *
from rich.traceback import install
from rich.console import Console

install()
console = Console()
init()


class TikTok():

    #initialization
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.66'
            }

        # capture all videos
        self.Isend = False

        # save username 
        self.nickname = ''
        # Likes
        self.like_counts = 0

        # User unique ID
        self.sec = ''


    def setting(self,uid,music,count,dir,mode):

        if uid != None:
            if uid == None:
                print(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}User cannot be empty")
                pass
            else:
                self.uid = uid;self.save = dir;self.count=count;self.musicarg=music;self.mode=mode
                self.judge_link()
        # no command received
        else:
            time.sleep(1)
        
    # 匹配粘贴的url地址
    def Find(self, string):
        # findall() Find a string that matches a regular expression
        url = re.findall(
            'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
        return url

    def replaceT(self, obj):
        """
        @description  : Replace text illegal characters
        ---------
        @param  : ojb - incoming object
        -------
        @Returns  : n - processed content
        -------
        """
        r = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        if type(obj) == list:
            new = []
            for i in obj:
                # replace with underscore
                retest = re.sub(r, "_", i)
                new.append(retest)
        elif type(obj) == str:
            # replace with underscore
            new = re.sub(r, "_", obj)
        return new

    # Determine the personal homepage api link
    def judge_link(self):

        # Determine the length of the chain
        r = requests.get(url = self.Find(self.uid)[0])
        print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Downloading many {Fore.WHITE}videos.\r")
        # get users sec_uid
        if '?' in r.request.path_url:
            for one in re.finditer(r'user\/([\d\D]*)([?])', str(r.request.path_url)):
                self.sec = one.group(1)
        else:
            for one in re.finditer(r'user\/([\d\D]*)', str(r.request.path_url)):
                self.sec = one.group(1)
        # 2022/08/24: Directly use the path_url in the request, and use user\/([\d\D]*)([?]) to filter out_sec
        print(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}User's sec_id:{Fore.GREEN} "+"%s\r" % self.sec)
        #else:
        #    r = requests.get(url = self.Find(self.uid)[0])
        #    print('[  提示  ]:为您下载多个视频!\r')
        #    # 获取用户sec_uid
        #    # 因为某些情况链接中会有?previous_page=app_code_link参数，为了不影响key结果做二次过滤
        #    # 2022/03/02: 用户主页链接中不应该出现?previous_page,?enter_from参数
        #    # 原user/([\d\D]*?)([?])
        #    # try:
        #    #     for one in re.finditer(r'user\/([\d\D]*)([?])',str(r.url)):
        #    #         key = one.group(1)
        #    # except:
        #    for one in re.finditer(r'user\/([\d\D]*)',str(r.url)):
        #        self.sec = one.group(1)
        #    print('[  提示  ]:用户的sec_id=%s\r' % self.sec)

        # first visit page number
        max_cursor = 0

        # Construct first visit link
        api_post_url = 'https://www.iesdouyin.com/web/api/v2/aweme/%s/?sec_uid=%s&count=%s&max_cursor=%s&aid=1128&_signature=PDHVOQAAXMfFyj02QEpGaDwx1S&dytk=' % ( 
                self.mode, self.sec, str(self.count), max_cursor)

        response = requests.get(url = api_post_url, headers = self.headers)
        html = json.loads(response.content.decode())
        self.nickname = html['aweme_list'][0]['author']['nickname']
        if not os.path.exists(self.nickname):
                os.makedirs(self.nickname)

        self.get_data(api_post_url, max_cursor)
        return api_post_url,max_cursor,self.sec

    # Get the first api data
    def get_data(self, api_post_url, max_cursor):
        # number of attempts
        index = 0
        # store api data
        result = []
        while result == []:
            index += 1
            console.log(f"[cyan][Status][/cyan] {Fore.WHITE}Attempt {Fore.GREEN}{index} {Fore.WHITE}in progress\r".format(index))
            time.sleep(0.3)
            response = requests.get(
                url = api_post_url, headers = self.headers)
            html = json.loads(response.content.decode())
            # with open('r.json', 'wb')as f:
            #     f.write(response.content)
            if self.Isend == False:
                # next page value
                print(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[User] {Fore.GREEN}",str(self.nickname),'\r')
                max_cursor = html['max_cursor']
                result = html['aweme_list']
                print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Capture data successfully! \r")

                # Process the first page of video information
                self.video_info(result, max_cursor)
            else:
                max_cursor = html['max_cursor']
                self.next_data(max_cursor)
                # self.Isend = True
                print(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}There is no data on this page, skipping... \r")

        return result,max_cursor

    # next page
    def next_data(self,max_cursor):
        # Construct the next visit link
        api_naxt_post_url = 'https://www.iesdouyin.com/web/api/v2/aweme/%s/?sec_uid=%s&count=%s&max_cursor=%s&aid=1128&_signature=RuMN1wAAJu7w0.6HdIeO2EbjDc&dytk=' % (
            self.mode, self.sec, str(self.count), max_cursor)

        index = 0
        result = []

        while self.Isend == False:
            # Return to the home page, end
            if max_cursor == 0:
                self.Isend = True
                return
            index += 1
            print(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Pairing ", max_cursor, f"page for {index} attempt!\r".format(index))
            time.sleep(0.3)
            response = requests.get(url = api_naxt_post_url, headers = self.headers)
            html = json.loads(response.content.decode())
            if self.Isend == False:
                # next page value
                max_cursor = html['max_cursor']
                result = html['aweme_list']
                print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Captured data of {max_cursor} page successfully! \r".format(max_cursor))
                # Process next page video information
                self.video_info(result, max_cursor)
            else:
                self.Isend == True
                print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Failed to capture data of {max_cursor} page! \r".format(max_cursor))
                # sys.exit()

    # Process video information
    def video_info(self, result, max_cursor):
        # author_list = [] - author info   
        # video_list = []  - No watermark video link 
        # aweme_id = [] - Work id        
        # nickname = [] - author id      
        # uri_list=[] - Unique Video ID# Cover image

        author_list = [];video_list = [];aweme_id = [];nickname = [];uri_list=[]# dynamic_cover = []

        for v in range(self.count):
            try:
                author_list.append(str(result[v]['desc']))
                # 2022/04/22
                # If directly from /web/api/v2/aweme/post  ~This interface takes data, then only 720p resolution
                # if in /web/api/v2/aweme/iteminfo/  ~This interface takes the video uri
                # splice to aweme.snssdk.com/aweme/v1/play/?video_id=xxxx&radio=1080p  ~then get 1080p clear
                video_list.append(str(result[v]['video']['play_addr']['url_list'][0]))
                uri_list.append(str(result[v]['video']['play_addr']['uri']))
                aweme_id.append(str(result[v]['aweme_id']))
                nickname.append(str(result[v]['author']['nickname']))
                # dynamic_cover.append(str(result[v]['video']['dynamic_cover']['url_list'][0]))
            except Exception as error:
                # print(error)
                pass
        # Filter illegal characters in video copy and author names
        print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Wait for the replacement of illegal characters in the copy!")
        author_list = self.replaceT(author_list)
        console.log(f"[cyan][Status][/cyan] :receipt: {Fore.WHITE}Waiting to replace the author's illegal characters...\r \n")
        nickname = self.replaceT(nickname)
        self.videos_download(author_list, video_list, uri_list, aweme_id, nickname, max_cursor)
        return self,author_list,video_list,uri_list,aweme_id,nickname,max_cursor

    # Check if a video has already been downloaded
    def check_info(self, nickname):
        if nickname == []:
            return
        else:
            v_info = os.listdir((nickname))
        return v_info

    # video download
    def videos_download(self, author_list, video_list, uri_list, aweme_id, nickname, max_cursor):
        # 生成1080p分辨率的视频链接
        new_video_list = [];uri_url = 'https://aweme.snssdk.com/aweme/v1/play/?video_id=%s&radio=1080p&line=0'
        # Create and check if the download directory exists
        try:
            os.makedirs(nickname[0])
        except:
            pass

        v_info = self.check_info(self.nickname)

        # self.count The value may be larger than the length of the actual api，so use len(author_list) (2022/03/22)
        for i in range(len(author_list)):

            # Like video sorting
            self.like_counts += 1

            # Get single video interface information
            try:
                # Official interface
                jx_url  = f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={aweme_id[i]}'    
                js = json.loads(requests.get(
                    url = jx_url,headers=self.headers).text)

                creat_time = time.strftime("%Y-%m-%d %H.%M.%S", time.localtime(js['item_list'][0]['create_time']))
            except Exception as error:
                # print(error)
                pass

            # remove filename  /r/n
            author_list[i] = ''.join(author_list[i].splitlines())
            if len(author_list[i]) > 182:
                print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}", "The file name is too long to be intercepted")
                author_list[i] = author_list[i][0:180]
                console.log(f"[cyan][Status][/cyan] {Fore.WHITE}", f"After interception name：{Fore.GREEN}{0}，{Fore.WHITE}Length：{Fore.GREEN}{1}".format(author_list[i], len(author_list[i])))

            # Check if the video has been downloaded
            try:
                if creat_time + author_list[i] + '.mp4' in v_info:
                    console.log(f"[red][File][/red] {Fore.GREEN}", author_list[i], f'{Fore.WHITE}[File already exists, skipping...]') # 开始下载，显示下载文件大小
                    print('\r')
                    continue
            except:
                # Prevent subscript out of bounds
                pass

            with console.status('[cyan] Fetching data video, please wait...') as status:
                #   try to download the video
                try:
                    # Generate 1080p video link
                    new_video_list.append(uri_url % uri_list[i])     
                    # video info      
                    video = requests.get(video_list[i])                           
                    t_video = requests.get(url=new_video_list[0],
                        # video content
                        headers=self.headers).content
                    # download start time                           
                    start = time.time()
                    # Initialize downloaded size                                     
                    size = 0     
                    # data size of each download                                        
                    chunk_size = 1024
                    # Total download file size                                       
                    content_size = int(video.headers['content-length']) 
                    try:
                        # Check whether the response is successful
                        if video.status_code == 200:                        
                            print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Video] {Fore.WHITE}" + creat_time + " " + author_list[i])
                            console.log(f"[green][Status][/green] {Fore.WHITE}File size: " + "{size:.2f} MB".format(size = content_size / chunk_size /1024))    # 开始下载，显示下载文件大小

                            if self.mode == 'post':
                                v_url = nickname[i] + '\\' + creat_time + re.sub(
                                    r'[\\/:*?"<>|\r\n] + ', "_", author_list[i]) + '.mp4'
                            else:
                                v_url = self.nickname + '\\' + str(self.like_counts)+ '、' + re.sub(
                                    r'[\\/:*?"<>|\r\n] + ', "_", author_list[i]) + '.mp4'

                            with open(v_url,'wb') as file:                
                                for data in video.iter_content(chunk_size = chunk_size):
                                    size += len(data)
                                    # show progress bar
                                    print('\r' + f"{Fore.CYAN}[Programs] {Fore.GREEN}[Download]{Fore.WHITE} " + '%s%.2f%%' % (
                                        '>' * int(size * 50 / content_size), float(size / content_size * 100)), end=' ')
                                file.write(t_video)

                                # Download end time
                                end = time.time() 
                                # print download time                          
                                print('\n' + f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Time:{Fore.YELLOW}"+ " %.2fs\n" % (end - start))
                            
                                new_video_list = []
                        

                    except Exception as error:
                        print(f'{Fore.CYAN}[Programs] {Fore.RED}[Status]{Fore.WHITE} Error downloading video!')
                        print(f"{Fore.CYAN}[Programs] {Fore.RED}[Status]{Fore.WHITE}", error, '\r')

                except Exception as error:
                    # print(error)
                    print(f"{Fore.CYAN}[Programs] {Fore.RED}[Status]{Fore.WHITE}", self.count, ", skipping...\r")
                    break
        # Get next page information
        self.next_data(max_cursor)
    
# main
if __name__ == "__main__":

    os.system('cls')
    txt = f"""{Fore.MAGENTA}
██████╗░░█████╗░██╗░░░██╗██╗░░░██╗██╗███╗░░██╗░░░░░░██████╗░██╗░░░░░
██╔══██╗██╔══██╗██║░░░██║╚██╗░██╔╝██║████╗░██║░░░░░░██╔══██╗██║░░░░░
██║░░██║██║░░██║██║░░░██║░╚████╔╝░██║██╔██╗██║█████╗██║░░██║██║░░░░░
██║░░██║██║░░██║██║░░░██║░░╚██╔╝░░██║██║╚████║╚════╝██║░░██║██║░░░░░
██████╔╝╚█████╔╝╚██████╔╝░░░██║░░░██║██║░╚███║░░░░░░██████╔╝███████╗
╚═════╝░░╚════╝░░╚═════╝░░░░╚═╝░░░╚═╝╚═╝░░╚══╝░░░░░░╚═════╝░╚══════╝
    Created by HengSok - DouyinDownload V1.2.5{Fore.GREEN}
            """
    print(Center.XCenter(txt))
    # draw layout
    print(Box.DoubleCube(f"""Ex1: https://v.douyin.com/jqwLHjF/ \nEx2: https://www.douyin.com/user/MS4wLjABAAAARz7MJzxuIgUFeEBer0sy7mMIvZzac"""))

    # Create a new instance
    TK = TikTok()
    user = input(f"{Fore.YELLOW}Enter User Link:{Fore.WHITE} ")
    music = 'no'
    count = int(35)
    dir = ''
    mode = 'post'
    TK.setting(user,music,count,dir,mode)
    time.sleep(1.5) 
    console.log(f"[cyan][Status][/cyan] {Fore.WHITE}Successfully downloaded all{Fore.WHITE} videos :white_check_mark:")
    time.sleep(1)                   
    print(input(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))