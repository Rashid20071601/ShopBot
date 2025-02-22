from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')  # Отображение в админ панели
    search_fields = ('name', 'category')  # Поиск по имени и категориям
    list_filter = ('category',)  # Филтрация по категориям


admin.site.site_header = 'Панель администратора'
admin.site.site_title = 'Управление магазином'