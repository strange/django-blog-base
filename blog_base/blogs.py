from django.shortcuts import get_object_or_404
from django.views.generic.date_based import archive_day
from django.views.generic.date_based import archive_month
from django.views.generic.date_based import archive_year
from django.views.generic.list_detail import object_detail
from django.views.generic.list_detail import object_list

from blog_base import feed_formats
from blog_base import markup
from blog_base.models import BaseEntry
from blog_base.models import Category

class BlogConfiguration(object):
    markup_format = markup.PLAIN_TEXT

    paginate_by = None
    template_object_name = 'entry'

    entry_list_template_name = 'blog_base/entry_list.html'
    entry_detail_template_name = 'blog_base/entry_detail.html'
    archive_year_template_name = 'blog_base/entry_archive_year.html'
    archive_month_template_name = 'blog_base/entry_archive_month.html'
    archive_day_template_name = 'blog_base/entry_archive_month.html'
    category_detail_template_name = 'blog_base/category_detail.html'

    # Admin settings

    use_generic_admin = True
    admin_regular_fields = ['title', 'slug', 'status', 'summary', 'body',
                            'categories', 'related_entries']
    admin_advanced_fields = ['pub_date', 'author', 'input_format']
    admin_list_display = ('title', 'author', 'pub_date', 'status')
    admin_list_filter = ('author', 'status')
    admin_search_fields = ('title', 'body', 'author__first_name',
                           'author__last_name')

    # Feed settings

    use_generic_feeds = True
    feed_format = feed_formats.ATOM
    feed_title = None
    feed_link = None
    feed_description = None
    feed_limit = 20

    feed_title_template_name = 'blog_base/feeds/title.html'
    feed_description_template_name = 'blog_base/feeds/description.html'

    def __init__(self, configuration_key, model):
        self.configuration_key = configuration_key
        self.model = model

        # Make sure that we're extending BaseEntry. This isn't strictly
        # necessary, but easier than checking attribute availability and
        # explaining.
        if not issubclass(model, BaseEntry):
            raise ValueError("The model registered must extend "
                             "simpleblog.BaseEntry.")

    def get_queryset(self, request):
        """Simple helper method that will return a ``QuerySet`` of live and
        draft entries if the requesting user is authenticated as a
        staff-member. If not, return only live entries.
        
        """
        if request.user.is_staff:
            return self.model.objects.exclude(status=BaseEntry.HIDDEN)
        return self.model.live.all()

    def entry_list(self, request, queryset=None, extra_context=None):
        if queryset is None:
            queryset = self.get_queryset(request)

        extra_context = extra_context or {}
        extra_context.update({ 'configuration': self })
        return object_list(request, queryset,
                           template_object_name=self.template_object_name,
                           template_name=self.entry_list_template_name,
                           extra_context=extra_context,
                           paginate_by=self.paginate_by)

    def entry_detail(self, request, entry_id, year=None, month=None, day=None,
                     entry_slug=None, extra_context=None):
        queryset = self.get_queryset(request)
        extra_context = extra_context or {}
        extra_context.update({ 'configuration': self })
        return object_detail(request, queryset, object_id=entry_id,
                             template_object_name=self.template_object_name,
                             template_name=self.entry_detail_template_name,
                             extra_context=extra_context)

    # Archive views

    def archive_year(self, request, year, extra_context=None):
        queryset = self.get_queryset(request)
        extra_context = extra_context or {}
        extra_context.update({ 'configuration': self })
        return archive_year(request, year, queryset, 'pub_date',
                            template_object_name=self.template_object_name,
                            make_object_list=True, extra_context=extra_context,
                            template_name=self.archive_year_template_name)

    def archive_month(self, request, year, month, extra_context=None):
        queryset = self.get_queryset(request)
        extra_context = extra_context or {}
        extra_context.update({ 'configuration': self })
        return archive_month(request, year, month, queryset, 'pub_date',
                             template_object_name=self.template_object_name,
                             extra_context=extra_context,
                             template_name=self.archive_month_template_name)

    def archive_day(self, request, year, month, day, extra_context=None):
        queryset = self.get_queryset(request)
        extra_context = extra_context or {}
        extra_context.update({ 'configuration': self })
        return archive_day(request, year, month, day, queryset, 'pub_date',
                           template_object_name=self.template_object_name,
                           extra_context=extra_context,
                           template_name=self.archive_day_template_name)

    # Category views

    def category_detail(self, request, category_slug, extra_context=None):
        category = get_object_or_404(Category, slug=category_slug)
        queryset = self.get_queryset(request)
        queryset = queryset.filter(categories=category)
        
        extra_context = extra_context or {}
        extra_context.update({
            'category': category,
            'configuration': self,
        })

        return object_list(request, queryset,
                           template_object_name=self.template_object_name,
                           template_name=self.category_detail_template_name,
                           extra_context=extra_context,
                           paginate_by=self.paginate_by)


class BlogConfigurationAlreadyRegistered(Exception):
    pass


class BlogConfigurationNotRegistered(Exception):
    pass


class BlogConfigurations(object):
    __shared_state = {
        'configurations': {},
    }
    
    def __init__(self):
        self.__dict__ = self.__shared_state
    
    def register(self, configuration_key, blog_model,
                 configuration_class=BlogConfiguration):
        """Register ``blog_model`` and ``configuration_class`` against
        ``configuration_key``. If configuration class is not given the default
        ``BlogConfiguration`` will be used.
        
        """
        try:
            self.configurations[configuration_key]
            raise BlogConfigurationAlreadyRegistered
        except KeyError:
            configuration = configuration_class(configuration_key, blog_model)
            self.configurations[configuration_key] = configuration
    
    def unregister(self, configuration_key):
        """Unregister model and configuration matching
        ``configuration_key``.
        
        """
        try:
            del(self.configurations[configuration_key])
        except KeyError:
            raise BlogConfigurationNotRegistered
    
    def get_model_and_configuration(self, configuration_key):
        """Return the blog model and configuration associated with
        ``configuration_key``.
        
        """
        try:
            return self.configurations[configuration_key]
        except KeyError:
            raise BlogConfigurationNotRegistered

    def all(self):
        return self.configurations.items()

configurations = BlogConfigurations()

all = configurations.all
register = configurations.register
unregister = configurations.unregister
get_model_and_configuration = configurations.get_model_and_configuration
