from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from orders.models import Order

class OrderInline(admin.TabularInline):
    model = Order
    fields = ('id', 'created_timestamp', 'total_price', 'status')
    readonly_fields = ('id', 'created_timestamp', 'total_price', 'status')
    can_delete = False
    extra = 0

class UserAdmin(BaseUserAdmin):
    inlines = (OrderInline,)

# Отменяем регистрацию UserAdmin по умолчанию и регистрируем нашу версию с добавленным OrderInline
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
