from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, DealerProfile, SalesManagerProfile


class DealerProfileInline(admin.StackedInline):
    """
    Додає профіль дилера до сторінки користувача в адмінці.
    """
    model = DealerProfile
    can_delete = True
    verbose_name_plural = "Профіль дилера"
    fk_name = "user"
    extra = 0  # не додає пустих рядків при редагуванні


class SalesManagerProfileInline(admin.StackedInline):
    """
    Додає профіль менеджера з продажів до сторінки користувача.
    """
    model = SalesManagerProfile
    can_delete = True
    verbose_name_plural = "Профіль менеджера з продажів"
    fk_name = "user"
    extra = 0

#  ГОЛОВНА АДМІН-ФОРМА ДЛЯ КОРИСТУВАЧА


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Розширене відображення користувачів у Django Admin.
    Включає додаткові поля (роль, телефон) та профілі.
    """

    list_display = ("username", "email", "role", "phone_number", "is_staff")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email", "phone_number")
    ordering = ("username",)

    # Групування полів у формі редагування користувача
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Особисті дані", {"fields": ("first_name", "last_name", "email", "phone_number")}),
        ("Роль та доступ", {"fields": ("role", "is_active", "is_staff", "is_superuser")}),
        ("Дати", {"fields": ("last_login", "date_joined")}),
    )

    # Які інлайни відображати залежно від ролі користувача
    def get_inlines(self, request, obj=None):
        if obj is None:
            return []
        if obj.role in ["DEALER_HEAD", "DEALER_MANAGER"]:
            return [DealerProfileInline]
        elif obj.role in ["RETAIL_MANAGER", "SALES_HEAD"]:
            return [SalesManagerProfileInline]
        return []

    # Перевизначає збереження, щоб уникнути помилок без профілю
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Можна додати автогенерацію профілю при створенні користувача (за потреби)


# Реєструємо профілі окремо — для доступу напряму, якщо потрібно
@admin.register(DealerProfile)
class DealerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "company_name", "city", "country")
    search_fields = ("company_name", "city", "user__username")


@admin.register(SalesManagerProfile)
class SalesManagerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "salon_name", "city")
    search_fields = ("salon_name", "city", "user__username")