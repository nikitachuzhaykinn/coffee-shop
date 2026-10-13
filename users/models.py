from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses', verbose_name="Пользователь")
    title = models.CharField(max_length=100, verbose_name="Название (например, 'Дом', 'Офис')")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=200, verbose_name="Улица")
    building = models.CharField(max_length=20, verbose_name="Дом")
    apartment = models.CharField(max_length=20, blank=True, verbose_name="Квартира")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    is_default = models.BooleanField(default=False, verbose_name="Адрес по умолчанию")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"{self.title}: {self.city}, {self.street}, {self.building}"

    def full_address(self):
        apt = f", кв. {self.apartment}" if self.apartment else ""
        return f"{self.city}, {self.street}, {self.building}{apt}"

# Добавляем поле phone в профиль пользователя
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
    
    def __str__(self):
        return f"Профиль {self.user.username}"