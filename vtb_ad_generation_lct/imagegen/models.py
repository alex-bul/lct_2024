# imagegen/models.py
from django.contrib.auth.models import User
from django.db import models


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    image = models.TextField()
    channel = models.CharField(max_length=255, blank=True)  # Поле для канала
    category = models.CharField(max_length=255, blank=True)  # Поле для категории
    product = models.CharField(max_length=255, blank=True)  # Поле для продукта
    created_at = models.DateTimeField(auto_now_add=True)  # Поле для даты создания

    def __str__(self):
        return f"{self.id} - {self.session.user.username} - {self.channel} - {self.category} - {self.product}"
