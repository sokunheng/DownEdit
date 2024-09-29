import time
from colorama import Fore

from .. import get_banner
from downedit.site.douyin import __main__ as douyin
from downedit.site.kuaishou import __main__ as kuaishou
from downedit.site.tiktok import __main__ as tiktok
from downedit.utils import (
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
                f" Douyin {Fore.RED}(Maintain)": lambda: None,
                f" Kuaishou {Fore.RED}(Maintain)": lambda: None,
                f" Youtube {Fore.RED}(Soon)": lambda: None,
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
