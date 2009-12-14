import datetime

from django.db.models import loading
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _

from blog_base.managers import LiveEntryManager
from blog_base.managers import EntryManager
from blog_base import markup

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('name'))
    description = models.TextField(blank=True)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('name', )
        app_label = 'blog_base'
    

class BaseEntry(models.Model):
    """Abstract base class used to add a few fields and some basic
    functionality when extended.
    
    Worth noting is that if you choose not to extend this class, you need add
    some necessary fields as these are used in the application views.
    
    """
    (LIVE, DRAFT, HIDDEN) = (0, 1, 3)
    STATUS_CHOICES = (
        (LIVE, _(u"Live")),
        (DRAFT, _(u"Draft")),
        (HIDDEN, _(u"Hidden")),
    )
    
    INPUT_FORMAT_CHOICES = (
        (markup.TEXTILE, _(u"Textile")),
        (markup.MARKDOWN, _(u"Markdown")),
        (markup.RESTRUCTUREDTEXT, _(u"ReStructuredText")),
        (markup.HTML, _(u"HTML")),
        (markup.PLAIN_TEXT, _(u"Plain Text")),
    )
    
    author = models.ForeignKey(User, help_text=_(u"Author of the entry."),
                               verbose_name=_(u"author"))

    title = models.CharField(max_length=200, verbose_name=_(u"title"))
    slug = models.SlugField(unique=True,
                            help_text=_(u"Do not edit when the entry has "
                                        "been published."))
    
    status = models.PositiveIntegerField(default=DRAFT, choices=STATUS_CHOICES,
                                         help_text=_(u"Drafts will be "
                                                     "visible on the site, "
                                                     "but only to staff and "
                                                     "super users."))

    summary = models.TextField(blank=True)
    summary_html = models.TextField(blank=True, editable=False)
    
    body = models.TextField()
    body_html = models.TextField(blank=True, editable=False)
    
    categories = models.ManyToManyField(Category, blank=True)
    related_entries = models.ManyToManyField('self', blank=True)
    
    featured = models.BooleanField(default=False)
    pub_date = models.DateTimeField(default=datetime.datetime.now)

    input_format = models.PositiveIntegerField(choices=INPUT_FORMAT_CHOICES,
                                               default=markup.PLAIN_TEXT)

    objects = EntryManager()
    live = LiveEntryManager()
    
    def is_draft(self):
        """Return ``True`` if the entry is but a draft."""
        return self.status == self.DRAFT
    
    def summary_or_body(self):
        """Return the summary of the Entry if available, otherwise fall back
        to the body.
        
        """
        return self.summary_html != '' and self.summary_html or self.body_html
    
    def save(self, *args, **kwargs):
        """Override to persist generated html from ``body`` and ``summary``
        and to set the publication date if status was changed from draft to
        live.
        
        """
        if self.pk:
            # Set the publication date if the status of the entry has changed
            # from DRAFT to LIVE and the date of the entry has not been
            # already changed.
            entry = self._default_manager.get(pk=self.pk)
            if entry.status == self.DRAFT and self.status == self.LIVE and \
               entry.pub_date == self.pub_date:
                self.pub_date = datetime.datetime.now()
        
        # Generate and store markup.
        self.body_html = markup.to_html(self.body, self.input_format)
        if self.summary:
            self.summary_html = markup.to_html(self.summary, self.input_format)
        else:
            self.summary_html = ''
        super(BaseEntry, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title
    
    class Meta:
        abstract = True
        ordering = ('-pub_date', )
        verbose_name = _('entry')
        verbose_name_plural = _('entries')
        get_latest_by = 'pub_date'
