from django import template
from django.templatetags.static import static
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def bootstrap_css():
    css_url = static('bootstrap/css/bootstrap.min.css')
    return mark_safe(f'<link rel="stylesheet" href="{css_url}">')
