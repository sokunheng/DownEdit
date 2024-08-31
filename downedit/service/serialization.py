def ch_brand_list(brand_list: list):
    """
    Serialize the brand list for the sec-ch-ua header.

    Args:
        brand_list (list): A list of dictionaries containing brand and version information.

    Returns:
        str: The serialized brand list.
    """
    serialized = []
    for _dict in brand_list:
        serialized.append('"' + _dict['brand'] + '";v="' + _dict['version'] + '"')

    return ', '.join(serialized)

def ch_bool(val: bool):
    """
    Serialize a boolean value

    Args:
        val (bool): The boolean value.

    Returns:
        str: The serialized boolean value.
    """
    return '?1' if val else '?0'

def ch_string(val: str):
    """
    Serialize a string value

    Args:
        val (str): The string value.

    Returns:
        str: The serialized string value
    """
    return '"' + val + '"'

def major_version(version_dict):
    """
    Get the major version from a version dictionary.

    Args:
        version_dict (dict): The version dictionary.

    Returns:
        str: The major version.
    """
    return str(version_dict['major']).split('.', 1)[0]

def format_mm_version(version_dict, strip_zero=None):
    """
    Format a major/minor version dictionary.

    Args:
        version_dict (dict): The version dictionary.
        strip_zero (bool): Whether to strip the minor version if it is 0.

    Returns:
        str: The formatted version.
    """
    major = version_dict['major']
    minor = int(version_dict.get('minor', 0))

    if strip_zero is None and minor == 0:
        strip_zero = True

    if minor == 0 and strip_zero:
        return str(major)
    else:
        return f"{major}.{minor}"