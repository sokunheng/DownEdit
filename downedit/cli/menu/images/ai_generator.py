import time

from pystyle import *
from colorama import *

from .. import get_banner
from downedit.utils import (
    log,
    selector
)

def main():
    banner_display, banner_msg = get_banner("AI_IMAGE_GENERATOR")
    selector.display_banner(
        banner_display,
        banner_msg, "- ai generative"
    )
    available_tools = {
        f" Cloud"                  : lambda: None,
        f" Local {Fore.RED}(Soon)" : lambda: None,
        f" Back"                   : lambda: None,
    }
    return selector.start(
        menu_options=available_tools,
        input_message=f"{Fore.YELLOW}Select Tools{Fore.WHITE}"
    )

if __name__ == "__main__":
    main()
