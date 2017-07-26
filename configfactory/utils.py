import copy
import json
import re
from collections import OrderedDict

from configfactory.exceptions import (
    CircularInjectError,
    InjectKeyError,
    JSONEncodeError,
)

key_re = r'[a-zA-Z][(\-|\.)a-zA-Z0-9_]*'
inject_regex = re.compile(r'(?<!\$)(\$(?:{param:(%(n)s)}))'
                          % ({'n': key_re}))


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


def replace_pytype(match):
    content = match.group()
    val = content.replace('\"', '').split(':')[-1]
    if val == 'True':
        return 'true'
    elif val == 'False':
        return 'false'
    return val


def inject_params(
        content: str,
        params: dict,
        calls: int=0,
        raise_exception: bool=True
):
    """
    Inject params to content.
    """

    circular_threshold = 100

    if calls > circular_threshold:
        if raise_exception:
            raise CircularInjectError(
                'Circular injections detected.'
            )
        return content

    calls += 1

    def replace_param(match):
        whole, key = match.groups()
        try:
            return str(params[key])
        except KeyError:
            if raise_exception:
                raise InjectKeyError(
                    message='Injection key `%(key)s` does not exist.' % {
                        'key': key
                    },
                    key=key
                )
            return whole

    if not inject_regex.search(content):
        return content

    content = inject_regex.sub(replace_param, content)

    if inject_regex.search(content):
        return inject_params(
            content=content,
            params=params,
            calls=calls,
            raise_exception=raise_exception
        )

    return content


def inject_dict_params(
        data: dict,
        params: dict,
        flatten: bool = False,
        raise_exception: bool = True):
    """
    Inject params to dictionary.
    """

    if flatten:
        data = flatten_dict(data)

    def inject(key, value):

        if isinstance(value, str):

            search = inject_regex.search(value)
            if not search:
                return value

            whole, param_key = search.groups()
            params_value = params.get(param_key)

            value = inject_params(
                content=value,
                params=params,
                raise_exception=raise_exception
            )

            if (
                params_value is not None
                and str(params_value) == value
            ):
                return params_value

        return value

    return traverse_dict(data, callback=inject)


def traverse_dict(obj, path=None, callback=None):
    """
    Traverse through nested dictionary.
    """

    if path is None:
        path = []

    if isinstance(obj, dict):
        value = OrderedDict([
            (key, traverse_dict(value, path + [key], callback))
            for key, value in obj.items()
        ])
    elif isinstance(obj, list):
        value = [
            traverse_dict(elem, path + [[]], callback)
            for elem in obj
        ]
    else:
        value = obj

    if callback is None:
        return value
    else:
        return callback(path, value)
