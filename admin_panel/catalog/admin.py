from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')  # 
    search_fields = ('name', 'category')  # 
    list_filter = ('category',)  # 


admin.site.site_header = 'Панель администратора'
admin.site.site_title = 'Управление магазином'