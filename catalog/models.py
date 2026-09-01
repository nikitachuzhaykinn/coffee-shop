from django.db import models
from django.urls import reverse
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Адресная строка")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        verbose_name="Изображение"
    )
    order = models.IntegerField(default=0, verbose_name="Порядок сортировки")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["order", "name"]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("catalog:category_detail", kwargs={"slug": self.slug})
    
    
class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Адресная строка")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена"
    )
    image = models.ImageField(upload_to="products/", blank=True, verbose_name="Изображение")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']
        
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'slug': self.slug})
    
    
class Modifier(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название модификатора")
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="modifiers",
        verbose_name="Товар"
    )
    
    class Meta:
        verbose_name = "Модификатор"
        verbose_name_plural = "Модификаторы"
        
    def __str__(self):
        return self.name
    

class ModifierOption(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название опции")
    modifier = models.ForeignKey(
        Modifier,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name="Модификатор"
    )
    price_extra = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Доплата"
    )

    class Meta:
        verbose_name = "Опция модификатора"
        verbose_name_plural = "Опции модификаторов"

    def __str__(self):
        return self.name