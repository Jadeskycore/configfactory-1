from django.utils.html import format_html


def html_params(**kwargs):
    params = []
    for k, v in sorted(kwargs.items()):
        if k in ('class_', 'class__', 'for_'):
            k = k[:-1]
        elif k.startswith('data_'):
            k = k.replace('_', '-', 1)
        if v is True:
            params.append(k)
        elif v is False:
            pass
        else:
            params.append('%s=%s' % (str(k), format_html(v)))
    return ' '.join(params)
