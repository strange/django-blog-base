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

    class Admin(admin.ModelAdmin):
        configuration = _configuration
        configuration_key = _configuration_key

        prepopulated_fields = { 'slug': ('title', ) }
        list_display = _configuration.admin_list_display
        list_filter = _configuration.admin_list_filter
        search_fields = _configuration.admin_search_fields

        def get_fieldsets(self, request, obj=None):
            regular_fields = self.configuration.admin_regular_fields
            advanced_fields = self.configuration.admin_advanced_fields

            fields = (None, { 'fields': regular_fields })
            advanced = ('Advanced options', {
                'classes': ('collapse', ),
                'fields': advanced_fields
            })
            return fields, advanced

        def formfield_for_foreignkey(self, db_field, request, **kwargs):
            if db_field.name == 'author':
                kwargs['initial'] = request.user.pk
            if db_field.name == 'input_format':
                kwargs['initial'] = self.configuration.markup_format
            return super(Admin, self).formfield_for_foreignkey(db_field,
                                                               request,
                                                               **kwargs)
    admin.site.register(_configuration.model, Admin)

admin.site.register(Category, CategoryOptions)
