from django.contrib import admin

from .models import Category, Component, Manufacturer

admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(Component)
