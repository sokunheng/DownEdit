
class KauiShou_API:
    """
    Base API URL for Kuaishou services.
    """
    KAUI_SHOU_DOMAIN = "https://www.kuaishou.com"


class Tiktok_API:
    """
    Contains the base API URL for TikTok services.
    """

    # Tiktok Domain
    TIKTOK_DOMAIN = "https://www.tiktok.com"

    # Webcast Domain
    WEBCAST_DOMAIN = "https://webcast.tiktok.com"

    # Login
    LOGIN_ENDPOINT = f"{TIKTOK_DOMAIN}/login/"

    # User Detail Info
    USER_DETAIL = f"{TIKTOK_DOMAIN}/api/user/detail/"

    # User Post
    USER_POST = f"{TIKTOK_DOMAIN}/api/post/item_list/"

    # User Collect
    USER_COLLECT = f"{TIKTOK_DOMAIN}/api/user/collect/item_list/"

    # User Play List
    USER_PLAY_LIST = f"{TIKTOK_DOMAIN}/api/user/playlist/"

    # User Mix
    USER_MIX = f"{TIKTOK_DOMAIN}/api/mix/item_list/"

    # Post Detail
    AWEME_DETAIL = f"{TIKTOK_DOMAIN}/api/item/detail/"

    # Post Comment
    POST_COMMENT = f"{TIKTOK_DOMAIN}/api/comment/list/"

    # Post Search
    POST_SEARCH = f"{TIKTOK_DOMAIN}/api/search/item/full/"


class SITIUS_API:
    """
    Contains the base API URL for SITIUS services.
    """
    API = "https://api.sitius.ir/"

    # Get available samplers
    SAMPLERS = f"{API}v1/samplers/"

    # Get available models
    MODELS = f"{API}v1/models/"

    # Generate image
    GENERATE = f"{API}v1/generate/"


class Domain:
    """
    Provides access to different site domains.
    """
    SITIUS = SITIUS_API()
    TIKTOK = Tiktok_API()
    KUAI_SHOU = KauiShou_API()