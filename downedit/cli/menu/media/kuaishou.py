from colorama import Fore

from downedit.site import KuaiShou
from .. import get_banner

from downedit.utils import (
    log,
    selector
)


def main():
    banner_display, banner_msg = get_banner("KUAISHOU_DL")
    selector.display_banner(
        banner_display,
        banner_msg
    )
    user = input(f"{Fore.YELLOW}Enter User Link:{Fore.WHITE} ")
    kuaishou = KuaiShou(user=user)
    kuaishou.download_all_videos()

if __name__ == "__main__":
    main()