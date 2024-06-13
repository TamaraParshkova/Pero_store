from django.contrib import admin
from .models import *

@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display=('name', 'price', 'stock', 'available', 'discount', "hit", 'category')
    list_editable =('price', 'stock', 'discount', 'available', 'hit')
    #readonly_fields = ('slug',)
    list_filter = ('category','available')
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 6



# Register your models here.
admin.site.register(Category)