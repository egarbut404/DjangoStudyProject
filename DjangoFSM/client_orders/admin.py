from django.contrib import admin
from .models import ClientOrder, ClientOrderItem  # Імпорти локальних моделей

# Inline клас для ClientOrderItem: дозволяє додавати/редагувати елементи безпосередньо в формі ClientOrder
class ClientOrderItemInline(admin.TabularInline):
    # Модель для inline: ClientOrderItem
    model = ClientOrderItem
    # Кількість порожніх рядків для додавання: 1 (для зручності)
    extra = 1
    # Поля, що тільки для читання: product_order_price (обчислюване)
    readonly_fields = ("product_order_price",)

    # Кастомне поле для відображення ціни з ProductOrder: метод, що повертає значення
    def product_order_price(self, obj):
        # Перевіряємо наявність product_order (OneToOne, тому має бути)
        if hasattr(obj, "product_order") and obj.product_order:
            return obj.product_order.final_price  # Повертаємо final_price
        return "-"  # Якщо немає — дефіс (фікс: уникнути помилок)
    # Короткий опис стовпця в адмінці
    product_order_price.short_description = "Ціна виробу"

# Реєстрація ClientOrder в адмінці: основний клас для редагування
@admin.register(ClientOrder)
class ClientOrderAdmin(admin.ModelAdmin):
    # Список полів для таблиці в списку об'єктів
    list_display = ("order_number", "client", "total_price")  # Показуємо: номер, клієнт, загальна ціна
    # Фільтри в боковій панелі: по клієнту та даті (додано для зручності)
    list_filter = ("client", "total_price")
    # Пошук по номеру та імені клієнта
    search_fields = ("order_number", "client__username")
    # Поля тільки для читання: total_price (бо обчислюється автоматично)
    readonly_fields = ("total_price",)
    # Inline класи: дозволяють додавати елементи в формі замовлення
    inlines = [ClientOrderItemInline]

# Окрема реєстрація ClientOrderItem: для прямого редагування, якщо потрібно (додано для повноти)
@admin.register(ClientOrderItem)
class ClientOrderItemAdmin(admin.ModelAdmin):
    # Список полів для таблиці
    list_display = ("client_order", "product", "get_product_order_price")  # Додано обчислюване поле
    # Фільтри: по замовленню та продукту
    list_filter = ("client_order", "product")
    # Пошук по продукту
    search_fields = ("product__name",)

    # Кастомне поле для ціни (аналогічно inline)
    def get_product_order_price(self, obj):
        if hasattr(obj, "product_order") and obj.product_order:
            return obj.product_order.final_price
        return "-"
    get_product_order_price.short_description = "Ціна з ProductOrder"