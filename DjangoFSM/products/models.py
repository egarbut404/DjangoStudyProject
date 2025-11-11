from django.db import models
from fabric.models import Fabric

# Create your models here.


class Category(models.Model):
    """Категорія товару (наприклад: дивани, крісла, ліжка)."""
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва категорії")
    description = models.TextField(blank=True, null=True, verbose_name="Опис категорії")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


# ==========================================================================


class Product(models.Model):
    """Основна модель меблів (виріб з тканини, категорії тощо)."""

    name = models.CharField(max_length=150, verbose_name="Назва виробу")
    code = models.CharField(max_length=50, unique=True, verbose_name="Артикул")

    # Категорія (наприклад: дивани, крісла, ліжка)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="Категорія"
    )

    # Розміри виробу
    length = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Довжина (см)")
    width = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Ширина (см)")
    height = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Висота (см)")

    # Базова ціна без урахування тканини
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Базова ціна (грн)")

    # Тканина (з моделі Fabric)
    fabric = models.ForeignKey(
        Fabric,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="Основна тканина"
    )

    # Кінцева ціна з урахуванням тканини
    final_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Кінцева ціна (грн)"
    )

    description = models.TextField(blank=True, null=True, verbose_name="Опис виробу")

    is_active = models.BooleanField(default=True, verbose_name="Активний в каталозі")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Під час збереження автоматично розраховує кінцеву ціну виробу."""
        if self.fabric and hasattr(self.fabric, "price_multiplier"):
            # Якщо у тканини заданий множник ціни — рахуємо фінальну вартість
            self.final_price = self.base_price * self.fabric.price_multiplier
        else:
            # Якщо тканина не обрана або без коефіцієнта — залишаємо базову ціну
            self.final_price = self.base_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = "Виріб"
        verbose_name_plural = "Вироби"


# ==========================================================================


class ProductImage(models.Model):
    """Фото виробу (може бути кілька, одне — головне)."""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Виріб"
    )
    image = models.ImageField(upload_to="product_images/", verbose_name="Фото виробу")
    is_main = models.BooleanField(default=False, verbose_name="Головне фото")

    def __str__(self):
        return f"Фото для {self.product.name}"

    class Meta:
        verbose_name = "Фото виробу"
        verbose_name_plural = "Фото виробів"
