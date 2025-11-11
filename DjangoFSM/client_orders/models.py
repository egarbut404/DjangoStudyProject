from django.db import models
from django.conf import settings

# Create your models here.

class OrderStatus(models.TextChoices):
    DRAFT = "draft", "Чернетка"
    IN_PROGRESS = "in_progress", "В роботі"
    COMPLETED = "completed", "Завершено"
    CANCELED = "canceled", "Скасовано"


class ClientOrder(models.Model):
    """Основна модель замовлення клієнта"""
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="client_orders",
        verbose_name="Клієнт"
    )
    order_number = models.CharField(max_length=50, unique=True, verbose_name="Номер замовлення")
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.DRAFT,
        verbose_name="Статус"
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Загальна сума")
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Знижка (%)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")
    comment = models.TextField(blank=True, null=True, verbose_name="Коментар")

    def __str__(self):
        return f"Замовлення #{self.order_number} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Замовлення клієнта"
        verbose_name_plural = "Замовлення клієнтів"
        ordering = ["-created_at"]