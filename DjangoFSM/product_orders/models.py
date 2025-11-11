from django.db import models
from client_orders.models import ClientOrder, ClientOrderItem
from products.models import Product

class ProductOrder(models.Model):
    """Замовлення на конкретний виріб з ClientOrder"""
    client_order_item = models.OneToOneField(
        ClientOrderItem,
        on_delete=models.CASCADE,
        related_name="product_order",
        verbose_name="Елемент замовлення"
    )
    final_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Фінальна ціна"
    )

    def save(self, *args, **kwargs):
        # Если final_price не установлен, берем из изделия
        if not self.final_price:
            self.final_price = self.client_order_item.product.final_price
        # Обновляем total_price заказа клиента
        client_order = self.client_order_item.client_order
        client_order.update_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client_order_item.product.name} в заказе #{self.client_order_item.client_order.order_number}"

    class Meta:
        verbose_name = "Замовлення виробу"
        verbose_name_plural = "Замовлення виробів"
