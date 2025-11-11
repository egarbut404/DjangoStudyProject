from django.contrib import admin
from .models import ProductOrder

@admin.register(ProductOrder)
class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ("client_order_item", "final_price")
    readonly_fields = ("final_price",)
