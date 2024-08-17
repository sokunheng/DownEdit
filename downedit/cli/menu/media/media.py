import time
from colorama import Fore

from .._banners import get_banner
from ....utils.tool_selector import selector
from ....utils.logger import logger
from ....site.douyin import __main__ as douyin
from ....site.kuaishou import __main__ as kuaishou
from ....site.tiktok import __main__ as tiktok

def main():
    while selector.running:
        try:
            banner_display, banner_msg = get_banner("VIDEO_DL")
            selector.display_banner(
                banner_display,
                banner_msg
            )
            # TODO: Media Video Downloader Algorithm
            menu_list = {
                " Tiktok": tiktok.main,
                " Kuaishou": lambda: None,
                " Youtube": lambda: None,
                " Back": lambda: None,
            }

            selector.start(
                menu_options=menu_list,
                input_message=f"{Fore.YELLOW}Select Media Platform{Fore.WHITE}"
            )

        except Exception as e:
            logger.error(str(e[:80]))
            time.sleep(0.5)
            logger.pause()


if __name__ == "__main__":
    main()
