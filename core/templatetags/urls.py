from urllib.parse import urlparse, urlunparse
from django.http import QueryDict
from django import template

register = template.Library()

@register.simple_tag
def replace_query_param(url, param, value):
    (scheme, netloc, path, params, query, fragment) = urlparse(url)
    query_dict = QueryDict(query).copy()
    query_dict[param] = value
    query = query_dict.urlencode()
    return urlunparse((scheme, netloc, path, params, query, fragment))
