from django.contrib import admin

# Register your models here.
from django.contrib.contenttypes.admin import GenericTabularInline

from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    min_num = 0
    max_num = 10
    extra = 1


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)