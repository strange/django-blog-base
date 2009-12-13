from django.db import models

class LiveEntryManager(models.Manager):
    def get_query_set(self):
        """Return a ``QuerySet`` of Entries that have been marked as being
        live.
        
        """
        return super(LiveEntryManager, self).get_query_set() \
                                            .filter(status=self.model.LIVE)
    def featured(self):
        """Return a ``QuerySet`` of featured Entries."""
        return self.filter(featured=True)
    
    def by_category(self, category):
        """Return a ``QuerySet`` of Entries in ``category``."""
        return self.filter(categories=category)
