from django.db import models
from products.models import Product  # Імпортуємо Product; ClientOrderItem — через string для уникнення циклу


# Модель замовлення на конкретний продукт: OneToOne з ClientOrderItem (щоб розширити елемент ціною)
class ProductOrder(models.Model):
    # OneToOne зв'язок з ClientOrderItem: використовуємо string 'client_orders.ClientOrderItem' (фікс циклу імпортів)
    # Каскадне видалення: якщо item видалено, ProductOrder теж
    client_order_item = models.OneToOneField(
        'client_orders.ClientOrderItem',  # String reference: Django завантажить модель пізніше
        on_delete=models.CASCADE,
        related_name="product_order",  # Зворотний доступ: item.product_order
        null=True,  # Тимчасово: дозволяє NULL
        blank=True,  # Для форм: необов'язкове
        verbose_name="Елемент замовлення клієнта"
    )
    # Фінальна ціна: десяткове число (до 10 цифр, 2 після коми)
    final_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Фінальна ціна"
    )

    # Перевизначений метод save: автоматично встановлює ціну, якщо не задано, і оновлює total
    def save(self, *args, **kwargs):
        # Якщо final_price не встановлено (None або 0), беремо з base_price продукту
        if not self.final_price:
            # Доступ до продукту через client_order_item (може бути None — додаємо перевірку)
            if self.client_order_item and self.client_order_item.product:
                self.final_price = self.client_order_item.product.base_price  # Фікс: base_price для consistency
            else:
                self.final_price = 0.00  # Дефолт, якщо продукту немає (фікс помилок)

        # Отримуємо батьківське ClientOrder для оновлення total_price
        client_order = None
        try:
            # Доступ через зв'язки: client_order_item.client_order (string reference розв'язано Django)
            client_order = self.client_order_item.client_order
        except AttributeError:
            # Якщо зв'язок не завантажено (рідко) — ігноруємо (фікс стабільності)
            pass

        # Оновлюємо total_price, якщо client_order існує
        if client_order:
            client_order.update_total_price()

        # Зберігаємо об'єкт (super() — батьківський метод)
        super().save(*args, **kwargs)

    # Строкове представлення: для адмінки та дебагу
    def __str__(self):
        # Безпечний доступ: якщо product існує
        product_name = self.client_order_item.product.name if self.client_order_item and self.client_order_item.product else "Без продукту"
        order_num = self.client_order_item.client_order.order_number if self.client_order_item and self.client_order_item.client_order else "Невідомо"
        return f"{product_name} в замовленні #{order_num} (ціна: {self.final_price})"

    class Meta:
        verbose_name = "Замовлення виробу"  # Назва в адмінці
        verbose_name_plural = "Замовлення виробів"
        # Індекс для швидкого пошуку по client_order_item
        indexes = [models.Index(fields=['client_order_item'])]