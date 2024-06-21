import time
from colorama import Fore

from .._banners import get_banner
from ....utils.common import tool_selector
from ....utils.logger import logger
from ....site.douyin import __main__ as douyin
from ....site.kuaishou import __main__ as kuaishou
from ....site.tiktok import __main__ as tiktok

def main():
    while tool_selector.running:
        try:
            banner_display, banner_msg = get_banner("VIDEO_DL")
            tool_selector.display_banner(
                banner_display,
                banner_msg
            )
            # TODO: Media Video Downloader Algorithm
            menu_list = {
                " Douyin": douyin.main,
                " Tiktok": tiktok.main,
                " Kuaishou": kuaishou.main,
                " Youtube": lambda: None,
                " Back": lambda: None,
            }

            tool_selector.start(
                menu_options=menu_list,
                input_message=f"{Fore.YELLOW}Select Media Platform{Fore.WHITE}"
            )

        except Exception as e:
            logger.error(str(e[:80]))
            time.sleep(0.5)
            logger.pause()


if __name__ == "__main__":
    main()
