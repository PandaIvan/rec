from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Promotion

# Создаем кастомный административный сайт
class CustomAdminSite(admin.AdminSite):
    site_header = "Администрация AROY AROY"
    site_title = "AROY AROY Admin"
    index_title = "Добро пожаловать в панель администрирования AROY AROY"

custom_admin_site = CustomAdminSite(name='custom_admin')

# Регистрируем модели для кастомного админсайта
custom_admin_site.register(Category)
custom_admin_site.register(Product)
custom_admin_site.register(Cart)
custom_admin_site.register(CartItem)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    class Media:
        css = {
            'all': ('menu/admin/admin_custom.css',)
        }

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')
    class Media:
        css = {
            'all': ('menu/admin/admin_custom.css',)
        }

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')

    class Media:
        css = {
            'all': ('menu/admin/admin_custom.css',)
        }

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')

    class Media:
        css = {
            'all': ('menu/admin/admin_custom.css',)
        }

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'active')
    search_fields = ('title',)
    list_filter = ('active',)
