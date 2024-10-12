
class SITIUS_API:
    """
    Contains the base API URL for SITIUS services.
    """
    API = "https://api.sitius.ir/"

    # Get available samplers
    SAMPLERS = f"{API}v1/samplers/"

    # Get available models
    MODELS = f"{API}v1/models/"

class Domain:
    """
    Provides access to different site domains.
    """
    SITIUS = SITIUS_API()