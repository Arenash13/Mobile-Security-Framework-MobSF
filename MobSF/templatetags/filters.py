from django import template

import base64


register = template.Library()
@register.filter
def key(data, key_name):
    """Return the data for a key_name."""
    return data.get(key_name)


@register.filter
def b64decode(data):
    """Return a base 64 decoded string."""
    return base64.b64decode(data.encode('utf-8')).decode('utf-8')


@register.filter
def path_to_package(path):
    return path.replace('/', '.')
