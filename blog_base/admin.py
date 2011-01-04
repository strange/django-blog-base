from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from blog_base.models import Category
from blog_base import blogs

class CategoryOptions(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('name', ) }


# Create and register dynamic ModelAdmin subclasses for each configuration
# that has use_generic_admin set to True.
for (_configuration_key, _configuration) in blogs.all():
    if not _configuration.use_generic_admin:
        continue

    # Define a custom form to set initial value of input format field.
    class Form(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super(Form, self).__init__(*args, **kwargs)
            self.fields['input_format'].initial = _configuration.markup_format

            class Meta:
                model = _configuration.model


    class Admin(admin.ModelAdmin):
        configuration = _configuration
        configuration_key = _configuration_key

        prepopulated_fields = { 'slug': ('title', ) }
        list_display = _configuration.admin_list_display
        list_filter = _configuration.admin_list_filter
        search_fields = _configuration.admin_search_fields

        form = Form

        def formfield_for_foreignkey(self, db_field, request, **kwargs):
            if db_field.name == 'author':
                kwargs['initial'] = request.user.pk
            return super(Admin, self).formfield_for_foreignkey(db_field,
                                                               request,
                                                               **kwargs)

    admin.site.register(_configuration.model, Admin)

admin.site.register(Category, CategoryOptions)
