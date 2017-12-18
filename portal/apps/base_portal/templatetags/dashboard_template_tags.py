from django import template
from django.utils.safestring import mark_safe

import json

register = template.Library()


@register.filter(name='mark_js_safe', is_safe=True)
def mark_js_safe(obj):
    return mark_safe(json.dumps(obj))
