from django.contrib.syndication.feeds import Feed
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils import feedgenerator

from blog_base import blogs
from blog_base import feed_formats

def get_feeds():
    """Return a dictionary containing `configuration_key` and feed class pairs
    for all configurations that have `use_generic_feeds` set to True.
    
    """
    feeds = {}
    for _configuration_key, _configuration in blogs.all():
        if not _configuration.use_generic_feeds:
            continue

        class EntryFeed(Feed):
            configuration = _configuration
            configuration_key = _configuration_key

            title_template = _configuration.feed_title_template_name
            description_template = \
                _configuration.feed_description_template_name

            feed_type = feedgenerator.Rss201rev2Feed

            def get_site(self):
                if not hasattr(self, '_current_site'):
                    self._current_site = Site.objects.get_current()
                return self._current_site

            def title(self):
                if self.configuration.feed_title is not None:
                    return self.configuration.feed_title
                return self.get_site().name
                
            def link(self):
                if self.configuration.feed_link is not None:
                    return self.configuration.feed_link
                return "http://%s/" % (self.get_site().domain)
                
            def description(self):
                if self.configuration.feed_description is not None:
                    return self.configuration.feed_description
                return "Latest entries on %s" % self.get_site().name
                                                             
            def items(self):
                items = self.configuration.model.live.all()
                return items[:self.configuration.feed_limit]
                
            def item_pubdate(self, obj):
                return obj.pub_date

            def item_link(self, obj):
                return self.configuration.get_entry_absolute_url(obj)

        if _configuration.feed_format == feed_formats.ATOM:
            # Alter the class to support Atom feeds instead of RSS.
            EntryFeed.feed_type = feedgenerator.Atom1Feed
            EntryFeed.subtitle = EntryFeed.description

        feeds[_configuration_key] = EntryFeed
    return feeds
