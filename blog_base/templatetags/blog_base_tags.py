from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def entry_url(entry, configuration):
    return configuration.get_entry_absolute_url(entry)
