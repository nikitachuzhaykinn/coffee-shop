import uuid
from django.db import models
from django.conf import settings
from catalog.models import Product


class Order(models.Model):
    order_id = models.CharField(max_length=20, unique=True, verbose_name="Номер заказа")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name="Пользователь"
    )
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")

    DELIVERY_CHOICES = [('pickup', 'Самовывоз'), ('delivery', 'Доставка')]
    delivery_type = models.CharField(
        max_length=20, choices=DELIVERY_CHOICES, default='pickup', verbose_name="Тип получения"
    )

    address = models.TextField(blank=True, verbose_name="Адрес доставки")
    pickup_time = models.DateTimeField(null=True, blank=True, verbose_name="Время самовывоза")

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итоговая сумма")

    STATUS_CHOICES = [
        ('new', 'Новый'), ('confirmed', 'Подтверждён'), ('preparing', 'Готовится'),
        ('ready', 'Готов к выдаче'), ('completed', 'Выдан/Доставлен'), ('cancelled', 'Отменён')
    ]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.order_id}"

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = f"CS-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу")
    modifiers = models.JSONField(default=list, verbose_name="Выбранные модификаторы")

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказов"

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"