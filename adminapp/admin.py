from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from django.db import models

# Base admin classes for specific configurations
class BaseUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')
    list_filter = ("username",)
    search_fields = ['username']

class BaseTokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user')
    list_filter = ("user",)
    search_fields = ['user']

# Custom admin classes mapping
custom_admin_classes = {
    'User': BaseUserAdmin,
    'Customer': BaseUserAdmin,
    'UserToken': BaseTokenAdmin,
    'CustomerToken': BaseTokenAdmin,
}

# Generic admin class with common attributes for all models
class GenericAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        self.list_filter = [field.name for field in model._meta.fields if isinstance(field, (models.CharField, models.TextField))]
        self.search_fields = [field.name for field in model._meta.fields if isinstance(field, (models.CharField, models.TextField))]
        super().__init__(model, admin_site)

app_models = apps.get_app_config('adminapp').get_models()
for model in app_models:
    model_name = model.__name__
    try:
        if model_name in custom_admin_classes:
            admin.site.register(model, custom_admin_classes[model_name])
        else:
            admin.site.register(model, type(f'{model_name}Admin', (GenericAdmin,), {}))
    except AlreadyRegistered:
        pass


