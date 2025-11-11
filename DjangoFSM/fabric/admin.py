from django.contrib import admin
from .models import FabricCategory, Fabric

# Register your models here.

@admin.register(FabricCategory)
class FabricCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name",)


@admin.register(Fabric)
class FabricAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "category", "color_name", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "code", "color_name")