from django.conf.urls.defaults import *
from django.contrib import admin

from blog_base import blogs

from example.blog.models import Entry

blogs.register('personal', Entry)
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^comments/', include('simple_comments.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^blogs/', include('blog_base.urls')),
)
