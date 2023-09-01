from django.contrib import admin
from django.utils.html import format_html
from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'display_image')

    def display_image(self, obj):
        return format_html('<img src="/images/{}" width="50" height="50" />', obj.image)

    display_image.short_description = 'Image'

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'user_id')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_order', 'complete', 'transaction_id')

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('address', 'city', 'state', 'customer_id', 'order_id')

# Register your models here.
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderItem)
admin.site.register(ShippingAddress,  ShippingAddressAdmin)