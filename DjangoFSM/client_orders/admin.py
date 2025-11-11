from django.contrib import admin
from .models import ClientOrder, ClientOrderItem

class ClientOrderItemInline(admin.TabularInline):
    model = ClientOrderItem
    extra = 1
    readonly_fields = ("product_order_price",)

    def product_order_price(self, obj):
        if hasattr(obj, "product_order"):
            return obj.product_order.final_price
        return "-"
    product_order_price.short_description = "Ціна виробу"

@admin.register(ClientOrder)
class ClientOrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "client", "total_price")
    readonly_fields = ("total_price",)
    inlines = [ClientOrderItemInline]
