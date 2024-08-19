import time
from colorama import Fore

from .. import get_banner
from ....site.douyin import __main__ as douyin
from ....site.kuaishou import __main__ as kuaishou
from ....site.tiktok import __main__ as tiktok
from ....utils import (
    log,
    selector
)

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
            log.error(str(e[:80]))
            time.sleep(0.5)
            log.pause()


if __name__ == "__main__":
    main()
