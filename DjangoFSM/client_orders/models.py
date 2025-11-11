from django.db import models
from products.models import Product
from product_orders.models import ProductOrder
from django.conf import settings


class ClientOrder(models.Model):
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    order_number = models.CharField(max_length=50, unique=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def update_total_price(self):
        total = sum([item.product_order.final_price for item in self.items.all() if hasattr(item, "product_order")])
        self.total_price = total
        self.save(update_fields=["total_price"])


class ClientOrderItem(models.Model):
    client_order = models.ForeignKey(ClientOrder, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Создаем/обновляем ProductOrder
        product_order, created = ProductOrder.objects.get_or_create(client_order_item=self)
        if self.product:
            product_order.final_price = self.product.base_price  # или другая логика цены
            product_order.save()
        # Обновляем total_price в ClientOrder
        self.client_order.update_total_price()
