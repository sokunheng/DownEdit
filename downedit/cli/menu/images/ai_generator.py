import time

from pystyle import *
from colorama import *

from .. import get_banner
from downedit.utils import (
    log,
    selector
)

def main():
    try:
        banner_display, banner_msg = get_banner("AI_IMAGE_GENERATOR")
        selector.display_banner(banner_display, banner_msg, "- ai generative")
        log.pause()
        return

    except Exception as e:
        log.error(e)
        time.sleep(0.5)
        log.pause()
        return

if __name__ == "__main__":
    main()
