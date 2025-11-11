from django.db import models

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


class Product(models.Model):
    """Основна модель меблів """
    name = models.CharField(max_length=150, verbose_name="Назва виробу")
    code = models.CharField(max_length=50, unique=True, verbose_name="Артикул")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    length = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Довжина (см)")
    width = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Ширина (см)")
    height = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Висота (см)")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Базова ціна (грн)")
    description = models.TextField(blank=True, null=True, verbose_name="Опис виробу")
    is_active = models.BooleanField(default=True, verbose_name="Активний в каталозі")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = "Виріб"
        verbose_name_plural = "Вироби"


class ProductImage(models.Model):
    """Фото виробу"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name="Виріб")
    image = models.ImageField(upload_to="product_images/", verbose_name="Фото виробу")
    is_main = models.BooleanField(default=False, verbose_name="Головне фото")

    def __str__(self):
        return f"Фото для {self.product.name}"

    class Meta:
        verbose_name = "Фото виробу"
        verbose_name_plural = "Фото виробів"
