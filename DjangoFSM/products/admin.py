from django.contrib import admin
from .models import Category, Product, ProductImage

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name",)
    ordering = ("name",)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "category", "base_price", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "code")
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "is_main")
