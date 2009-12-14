from django.db import models
from django.db.models import Q

class EntryManager(models.Manager):
    def featured(self):
        """Return a ``QuerySet`` of featured Entries."""
        return self.filter(featured=True)
    
    def search(self, query):
        """Simple search."""
        return self.filter(Q(title__icontains=query) | Q(body__icontains=query))


class LiveEntryManager(EntryManager):
    def get_query_set(self):
        """Return a ``QuerySet`` of Entries that have been marked as being
        live.
        
        """
        return super(LiveEntryManager, self).get_query_set() \
                                            .filter(status=self.model.LIVE)
    def by_category(self, category):
        """Return a ``QuerySet`` of Entries in ``category``."""
        return self.filter(categories=category)
