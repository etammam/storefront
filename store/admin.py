from django.contrib import admin
from django.db.models import Count, QuerySet
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from . import models

admin.sites.AdminSite.site_header = 'Storefront'
admin.sites.AdminSite.site_title = 'Storefront Administration'
admin.sites.AdminSite.index_title = 'Manage Your Storefront'


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'product_count']
    list_editable = ['title']
    list_per_page = 10
    ordering = ['id']
    search_fields = ['title']

    @admin.display(ordering='product_count')
    def product_count(self, collection):
        url = reverse('admin:store_product_changelist') + '?' + urlencode({
            'collection__id': str(collection.id)
        })
        return format_html('<a href="{}">{}</a>', url, collection.product_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count=Count('product'))


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'customer_orders']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(description='Orders')
    def customer_orders(self, customer):
        url = reverse('admin:store_order_changelist') + '?' + urlencode({
            'customer__id': str(customer.id)
        })
        return format_html('<a href={}>View Orders</a>', url)


class InventoryFilter(admin.SimpleListFilter):
    title = 'By inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    list_display = ['title', 'collection', 'inventory_status', 'price', 'inventory']
    list_editable = ['price', 'inventory']
    list_per_page = 10
    list_filter = ['collection', 'last_update', InventoryFilter]
    search_fields = ['title__istartswith']
    ordering = ['title']
    actions = ['clear_inventory']

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory > 10:
            return "OK"
        return "Low"

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset: QuerySet):
        updated_count = queryset.update(inventory=0)
        self.message_user(request, f'{updated_count} products has been updated.')


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'payment_status', 'customer', 'customer_email', 'order_item_count']
    list_select_related = ['customer']
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]

    @admin.display(description='customer email')
    def customer_email(self, order):
        return order.customer.email

    @admin.display(description='order items')
    def order_item_count(self, order):
        order_id = order.id
        return models.OrderItem.objects.filter(order_id=order_id).count()
