from collections import OrderedDict
from copy import deepcopy


def merge_dicts(dict1, dict2):
    """
    Merge two dictionaries.
    """
    if not isinstance(dict2, dict):
        return dict2
    result = deepcopy(dict1)
    for k, v in dict2.items():
        if k in result and isinstance(result[k], dict):
            result[k] = merge_dicts(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result


def flatten_dict(d, parent_key='', sep='.'):
    """
    Flatten dictionary keys.
    """
    if not isinstance(d, dict):
        return d
    items = []
    for k, v in d.items():
        new_key = sep.join([parent_key, k]) if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return OrderedDict(items)


def sort_dict(d):
    if not isinstance(d, dict):
        return d
    return OrderedDict(sorted(d.items()))
