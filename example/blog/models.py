from django.db import models

from blog_base.models import BaseEntry

class Entry(BaseEntry):
    extra_field = models.CharField(max_length=20, blank=True)
