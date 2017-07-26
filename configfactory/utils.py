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
pytype_regex = re.compile(r'\"pytype:.+\"')


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
    """Inject params to content."""

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
            val = params[key]
            if not isinstance(val, str):
                return 'pytype:{}'.format(params[key])
            return val
        except KeyError:
            if raise_exception:
                raise InjectKeyError(
                    message='Injection key `%(key)s` does not exist.' % {
                        'key': key
                    },
                    key=key
                )
            return whole

    content = inject_regex.sub(replace_param, content)

    if inject_regex.search(content):
        return inject_params(
            content=content,
            params=params,
            calls=calls,
            raise_exception=raise_exception
        )

    content = pytype_regex.sub(replace_pytype, content)

    return content
