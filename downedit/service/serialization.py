"""
Serialization module for DownEdit.
Copyright: 2024 - (github.com/sokunheng)
License: Apache License 2.0
"""

def ch_brand_list(brand_list: list):
    serialized = []
    for _dict in brand_list:
        serialized.append('"' + _dict['brand'] + '";v="' + _dict['version'] + '"')

    return ', '.join(serialized)

def ch_bool(val: bool):
    return '?1' if val else '?0'

def ch_string(val: str):
    return '"' + val + '"'

def major_version(version_dict):
    return str(version_dict['major']).split('.', 1)[0]

def format_mm_version(version_dict, strip_zero=None):
    major = version_dict['major']
    minor = int(version_dict.get('minor', 0))

    if strip_zero is None and minor == 0:
        strip_zero = True

    if minor == 0 and strip_zero:
        return str(major)
    else:
        return f"{major}.{minor}"