import copy
import json
from collections import OrderedDict

from configfactory.exceptions import JSONEncodeError


def json_dumps(obj, indent=None):
    return json.dumps(obj, indent=indent)


def json_loads(s):
    try:
        return json.loads(s, object_pairs_hook=OrderedDict)
    except Exception as e:
        raise JSONEncodeError(
            'Invalid JSON: {}.'.format(e)
        )


def merge_dicts(dict1, dict2):
    """
    Merge two dictionaries.
    """
    if not isinstance(dict2, dict):
        return dict2
    result = OrderedDict()
    for k, v in dict2.items():
        if k in result and isinstance(dict1[k], dict):
            result[k] = merge_dicts(dict1[k], v)
        else:
            result[k] = copy.deepcopy(v)
    for k, v in dict1.items():
        if k not in result:
            result[k] = copy.deepcopy(v)
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
