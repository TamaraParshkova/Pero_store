from django.contrib import admin
from orders.models import Order, OrderItem

class OrderItemTabularInline(admin.TabularInline):
    model = OrderItem
    fields = ("product", "name", "price", "quantity")
    search_fields = ("product__name", "name")
    extra = 0

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "name", "price", "quantity")
    search_fields = ("order__id", "product__name", "name")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = (
        ('created_timestamp', 'status'),
        ('user', 'phone_number'),
        'requires_delivery', 'delivery_address',
        ("payment_on_get", 'total_price', 'is_paid')
    )
    list_display = (
        "id", "user", "requires_delivery", "status",
        "payment_on_get", "is_paid", "created_timestamp", 'total_price'
    )
    search_fields = ("id", "user__username", "user__first_name", "user__last_name")
    readonly_fields = ("created_timestamp",)
    list_filter = ("requires_delivery", "status", "payment_on_get", "is_paid")
    inlines = (OrderItemTabularInline,)
