from django.conf.urls.defaults import *
from django.contrib import admin

from blog_base import blogs

from example.blog.models import Entry

blogs.register('personal', Entry)
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^blogs/', include('blog_base.urls')),
)
