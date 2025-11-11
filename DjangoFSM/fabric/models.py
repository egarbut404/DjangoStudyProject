from django.db import models

# Create your models here.

class FabricCategory(models.Model):
    """Категорія тканини (наприклад: Велюр, Шеніл, Мікровелюр)"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва категорії")
    description = models.TextField(blank=True, null=True, verbose_name="Опис категорії")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія тканини"
        verbose_name_plural = "Категорії тканин"


class Fabric(models.Model):
    """Модель тканини, яка може використовуватись у виробах."""
    name = models.CharField(max_length=100, verbose_name="Назва тканини")
    code = models.CharField(max_length=50, unique=True, verbose_name="Код тканини")
    category = models.ForeignKey(FabricCategory, on_delete=models.SET_NULL, null=True, related_name="fabrics")
    color_name = models.CharField(max_length=100, verbose_name="Назва кольору")
    color_code = models.CharField(max_length=20, verbose_name="Код кольору (наприклад HEX або RGB)")
    image = models.ImageField(upload_to="fabric_images/", blank=True, null=True, verbose_name="Фото зразка")
    price_multiplier = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.00,
        verbose_name="Коефіцієнт ціни (множник для базової ціни виробу)"
    )
    is_active = models.BooleanField(default=True, verbose_name="Доступна для вибору")

    def __str__(self):
        return f"{self.name} ({self.color_name})"

    class Meta:
        verbose_name = "Тканина"
        verbose_name_plural = "Тканини"