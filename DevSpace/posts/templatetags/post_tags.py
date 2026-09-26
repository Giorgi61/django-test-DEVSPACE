
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_params(context, **kwargs):

    request_get = context['request'].GET.copy()
    for key, value in kwargs.items():
        request_get[key] = value
    return request_get.urlencode()



