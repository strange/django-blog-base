from django import http

from blog_base.models import Category
from blog_base import blogs

def get_configuration_or_404(configuration_key):
    """Return configuration instance for `configuration_key`."""
    try:
        return blogs.get_model_and_configuration(configuration_key)
    except blogs.BlogConfigurationNotRegistered:
        raise http.Http404(u"Configuration does not exist.")

def entry_list(request, configuration_key, queryset=None, extra_context=None):
    configuration = get_configuration_or_404(configuration_key)
    return configuration.entry_list(request, queryset, extra_context)

def entry_detail(request, configuration_key, entry_id, year=None, month=None,
                 day=None, entry_slug=None, extra_context=None):
    configuration = get_configuration_or_404(configuration_key)
    return configuration.entry_detail(request, entry_id, year, month, day,
                                      entry_slug, extra_context)

def archive_year(request, configuration_key, year, extra_context=None):
    configuration = get_configuration_or_404(configuration_key)
    return configuration.archive_year(request, year, extra_context)

def archive_month(request, configuration_key, year, month, extra_context=None):
    configuration = get_configuration_or_404(configuration_key)
    return configuration.archive_month(request, year, month, extra_context)

def archive_day(request, configuration_key, year, month, day,
                extra_context=None):
    configuration = get_configuration_or_404(configuration_key)
    return configuration.archive_day(request, year, month, day, extra_context)

def category_detail(request, configuration_key, category_slug,
                    extra_context=None):
    configuration = get_configuration_or_404(configuration_key)
    return configuration.category_detail(request, category_slug, extra_context)

def search(request, configuration_key, extra_context=None):
    configuration = get_configuration_or_404(configuration_key)
    return configuration.search(request, extra_context)
