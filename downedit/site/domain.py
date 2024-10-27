class Perchance_API:
    """
    Contains the base API URL for Perchance services.
    """

    # Perchance Domain
    PERCHANCE_DOMAIN = "https://perchance.org"

    PERCHANCE_CC =  "https://perchanceai.cc"

    # Perchance API
    PERCHANCE_API = "https://image-generation.perchance.org"

    # Get Access Code
    ACCESS_CODE = f"{PERCHANCE_DOMAIN}/api/getAccessCodeForAdPoweredStuff"

    # Check Verification Status
    CHECK_VERYIFY = f"{PERCHANCE_API}/api/checkVerificationStatus"

    # User Verify
    USER_VERIFY = f"{PERCHANCE_API}/api/verifyUser"

    # Turnstile
    EMBED_TURNSTILE = f"{PERCHANCE_API}//embed"

    # Download Image
    DOWNLOAD_IMAGE = f"{PERCHANCE_API}/api/downloadTemporaryImage"

    # Generate Image
    GENERATE_IMAGE = f"{PERCHANCE_API}/api/generate"

    PREDICT = f"{PERCHANCE_CC}/api/model/predict/v1"

    # Text to Image
    TEXT_TO_IMAGE = f"{PERCHANCE_API}/textToImage"


class AIGG_API:
    """
    Contains the base API URL for Downedit services.
    """
    DOMAIN = "https://aiimagegenerator.io"

    GENERATE_IMAGE = f"{DOMAIN}/api/model/predict-peach"


class AI_Image_API:
    """
    Contains the base API URL for AI Image services.
    """
    PERCHANCE = Perchance_API()
    AIGG = AIGG_API()


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


class Domain:
    """
    Provides access to different site domains.
    """
    AI_IMAGE = AI_Image_API()
    TIKTOK = Tiktok_API()
    KUAI_SHOU = KauiShou_API()