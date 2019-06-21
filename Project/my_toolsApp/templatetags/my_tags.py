from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def error_code(name):
    return getattr(settings, name,"")
