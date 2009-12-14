from django.conf.urls.defaults import *

from blog_base import views
from blog_base.feeds import get_feeds

p = (
    # Feeds
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
     { 'feed_dict': get_feeds() }),

    (r'^(?P<configuration_key>\w+)/$', views.entry_list, {},
     'blog-base-entry-list'),
    (r'^(?P<configuration_key>\w+)/(?P<year>\d{4})/$', views.archive_year, {},
     'blog-base-archive-year'),
    (r'^(?P<configuration_key>\w+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
     views.archive_month, {}, 'blog-base-archive-month'),
    (r'^(?P<configuration_key>\w+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/$',
     views.archive_day, {}, 'blog-base-archive-day'),
    (r'^(?P<configuration_key>\w+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/(?P<entry_id>\d+)-(?P<entry_slug>[\w\-]+)/$',
     views.entry_detail, {}, 'blog-base-entry-detail'),
    (r'^(?P<configuration_key>\w+)/categories/(?P<category_slug>[\w-]+)/$',
     views.category_detail, {}, 'blog-base-category-detail'),
    (r'^(?P<configuration_key>\w+)/search/$',
     views.search, {}, 'blog-base-search'),
)

urlpatterns = patterns('', *p)
