import collections

from copy import deepcopy


def merge_dicts(dict1, dict2):
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
    if not isinstance(d, dict):
        return d
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def sort_dict(d):
    if not isinstance(d, dict):
        return d
    return collections.OrderedDict(sorted(d.items()))
