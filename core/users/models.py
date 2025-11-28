from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    ROLES = (
        ('admin', 'Администратор'),
        ('moder', 'Модератор'),
        ('user', 'Пользователь')
    )
    role = models.CharField(max_length=14, verbose_name='Роли', choices=ROLES, default='user')
