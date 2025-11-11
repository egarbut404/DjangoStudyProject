from django.contrib import admin
from .models import ProductOrder  # Імпорт локальної моделі

# Реєстрація ProductOrder в адмінці: базовий клас для редагування
@admin.register(ProductOrder)
class ProductOrderAdmin(admin.ModelAdmin):
    # Список полів для таблиці в списку об'єктів
    list_display = ("client_order_item", "final_price", "get_client_order_number")  # Додано обчислюване поле для номеру
    # Фільтри в боковій панелі: по ціні (додано для зручності)
    list_filter = ("final_price",)
    # Пошук по номеру замовлення (через client_order_item)
    search_fields = ("client_order_item__client_order__order_number", "client_order_item__product__name")
    # Поля тільки для читання: final_price (бо обчислюється автоматично)
    readonly_fields = ("final_price",)
    # raw_id_fields: для великих FK — показує popup замість dropdown (корисно, якщо багато items)
    raw_id_fields = ("client_order_item",)

    # Кастомне поле для відображення номера замовлення (для зручності в list_display)
    def get_client_order_number(self, obj):
        # Безпечний доступ до order_number
        if obj.client_order_item and obj.client_order_item.client_order:
            return obj.client_order_item.client_order.order_number
        return "-"
    # Короткий опис стовпця
    get_client_order_number.short_description = "Номер клієнтського замовлення"