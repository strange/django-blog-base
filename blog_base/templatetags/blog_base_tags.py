from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def entry_url(entry, configuration):
    pub_date = entry.pub_date
    args = [
        configuration.configuration_key,
        pub_date.year,
        pub_date.strftime('%b').lower(),
        pub_date.strftime('%d'),
        entry.pk,
        entry.slug,
    ]
    return reverse('blog-base-entry-detail', args=args)
