from django.db import models
from django.conf import settings
from products.models import Product  # Імпортуємо тільки Product (без циклу); ProductOrder — всередині методу


# Модель головного замовлення клієнта: пов'язує користувача з елементами замовлення
class ClientOrder(models.Model):
    # Зв'язок з користувачем: якщо користувач видалено, поле стає NULL (SET_NULL), необов'язкове (null=True, blank=True)
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Використовуємо AUTH_USER_MODEL для гнучкості (замість жорсткого User)
        on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name="Клієнт"  # Назва поля в адмінці/формах
    )
    # Унікальний номер замовлення: для ідентифікації, макс. 50 символів
    order_number = models.CharField(max_length=50, unique=True, verbose_name="Номер замовлення")
    # Загальна ціна: десяткове число (до 10 цифр, 2 після коми), за замовчуванням 0.00
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Загальна ціна")

    # Метод для оновлення загальної ціни: сумує final_price з усіх пов'язаних ProductOrder
    def update_total_price(self):
        # Ініціалізуємо total як 0; використовуємо sum з generator для ефективності
        total = sum(
            item.product_order.final_price  # Беремо final_price з product_order елемента
            for item in self.items.all()  # Цикл по всіх пов'язаних ClientOrderItem (related_name="items")
            if hasattr(item, "product_order") and item.product_order
            # Перевірка: існує product_order і не None (фікс помилок)
        )
        # Оновлюємо поле total_price тільки цим значенням (update_fields — для ефективності, не тригерить інші сигнали)
        self.total_price = total
        self.save(update_fields=["total_price"])

    # Строкове представлення моделі: для адмінки та дебагу
    def __str__(self):
        return f"Замовлення {self.order_number} (клієнт: {self.client.username if self.client else 'Анонім'})"

    class Meta:
        verbose_name = "Замовлення клієнта"  # Назва в адмінці (однина)
        verbose_name_plural = "Замовлення клієнтів"  # Множина
        ordering = ['-id']  # Сортування: новіші перші (за ID)


# Модель елемента замовлення клієнта: пов'язує ClientOrder з конкретним продуктом
class ClientOrderItem(models.Model):
    # Зв'язок з ClientOrder: каскадне видалення (якщо order видалено, item теж); related_name для зворотного доступу
    client_order = models.ForeignKey(ClientOrder, on_delete=models.CASCADE, related_name="items",
                                     verbose_name="Замовлення")
    # Зв'язок з продуктом: SET_NULL якщо продукт видалено (щоб item не зникав); необов'язкове
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Продукт")

    # Перевизначений метод save: викликається автоматично при збереженні/оновленні об'єкта
    def save(self, *args, **kwargs):
        # Спочатку зберігаємо базовий об'єкт (super() — виклик батьківського методу)
        super().save(*args, **kwargs)

        # Lazy import: імпортуємо ProductOrder тільки тут, щоб уникнути циклічних імпортів на рівні модуля
        from product_orders.models import ProductOrder

        # Створюємо або отримуємо пов'язаний ProductOrder (OneToOne, тому get_or_create по client_order_item=self)
        product_order, created = ProductOrder.objects.get_or_create(client_order_item=self)

        # Якщо продукт існує, встановлюємо final_price = base_price продукту (фікс: використовуємо base_price всюди для consistency)
        if self.product:
            product_order.final_price = self.product.base_price  # Логіка ціни: беремо базову ціну; якщо потрібно — додай модифікатори
            product_order.save()  # Зберігаємо ProductOrder (тригерить його save(), де оновиться total)

        # Оновлюємо загальну ціну в батьківському ClientOrder (якщо існує)
        if self.client_order:
            self.client_order.update_total_price()

    # Строкове представлення: для адмінки
    def __str__(self):
        product_name = self.product.name if self.product else "Без продукту"
        return f"Елемент: {product_name} (замовлення {self.client_order.order_number})"

    class Meta:
        verbose_name = "Елемент замовлення клієнта"
        verbose_name_plural = "Елементи замовлень клієнтів"
        unique_together = ['client_order',
                           'product']  # Унікальність: один продукт на одне замовлення (опціонально, для уникнення дублікатів)