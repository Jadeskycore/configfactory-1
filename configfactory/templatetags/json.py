from json import dumps as json_dumps

from django.core.serializers.json import DjangoJSONEncoder
from django.template import Library

register = Library()


@register.filter
def jsonify(data):

    unsafe_chars = {
        '&': '\\u0026',
        '<': '\\u003c',
        '>': '\\u003e',
        '\u2028': '\\u2028',
        '\u2029': '\\u2029'}
    json_str = json_dumps(data, cls=DjangoJSONEncoder, indent=4)

    for (c, d) in unsafe_chars.items():
        json_str = json_str.replace(c, d)

    return json_str
