from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

# Create your models here.


class User(AbstractUser):
    """
    Кастомна модель користувача з ролями.
    Використовується замість стандартного User від Django.
    """

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Адміністратор"
        OWNER = "OWNER", "Власник"
        DESIGNER = "DESIGNER", "Дизайнер"
        SALES_HEAD = "SALES_HEAD", "Керівник з продажів"
        RETAIL_HEAD = "RETAIL_HEAD", "Керівник роздрібного продажу"
        RETAIL_MANAGER = "RETAIL_MANAGER", "Менеджер з продажу"
        DEALER_HEAD = "DEALER_HEAD", "Керівник дилерів"
        DEALER_MANAGER = "DEALER_MANAGER", "Партнер / дилер"
        PRODUCT_HEAD = "PRODUCT_HEAD", "Керівник виробництва"
        PRODUCT_MANAGER = "PRODUCT_MANAGER", "Менеджер виробництва"
        LOGIST_MANAGER = "LOGIST_MANAGER", "Менеджер з логістики"
        QUALITY_MANAGER = "QUALITY_MANAGER", "Менеджер ОТК"

    # Основна роль користувача
    role = models.CharField(
        max_length=32,
        choices=Role.choices,
        default=Role.RETAIL_MANAGER,
        db_index=True,
        verbose_name="Роль"
    )

    # Унікальний телефон з валідацією українського формату
    phone_validator = RegexValidator(
        regex=r'^\+?380?\d{9,12}$',
        message="Введіть номер телефону у форматі +380501234567"
    )
    phone_number = models.CharField(
        max_length=20,
        validators=[phone_validator],
        unique=True,
        help_text="Контактний номер телефону",
        verbose_name="Телефон"
    )

    # Email тепер обов’язковий
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        verbose_name="Електронна пошта"
    )

    def __str__(self):
        """Повертає зрозуміле представлення користувача."""
        return f"{self.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"

class DealerProfile(models.Model):
    """
    Профіль для партнерів / дилерів.
    Зберігає додаткову інформацію про компанію та місцезнаходження.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='dealer_profile',
        verbose_name="Користувач"
    )
    company_name = models.CharField(max_length=150, verbose_name="Назва компанії")
    city = models.CharField(max_length=100, verbose_name="Місто")
    country = models.CharField(max_length=100, verbose_name="Країна")

    def __str__(self):
        return f"{self.company_name} ({self.user.username})"

    class Meta:
        verbose_name = "Профіль дилера"
        verbose_name_plural = "Профілі дилерів"


class SalesManagerProfile(models.Model):
    """
    Профіль для менеджерів з продажів.
    Зберігає назву салону та місто.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='sales_profile',
        verbose_name="Користувач"
    )
    salon_name = models.CharField(max_length=150, verbose_name="Назва салону")
    city = models.CharField(max_length=100, verbose_name="Місто")

    def __str__(self):
        return f"{self.salon_name} ({self.user.username})"

    class Meta:
        verbose_name = "Профіль менеджера з продажів"
        verbose_name_plural = "Профілі менеджерів з продажів"