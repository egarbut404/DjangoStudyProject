from django.contrib import admin
from .models import ClientOrder

# Register your models here.

@admin.register(ClientOrder)
class ClientOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "order_number", "client", "status", "total_price", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("order_number", "client__email", "client__username")
    ordering = ("-created_at",)