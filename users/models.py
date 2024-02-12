from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': 'True', 'null': 'True'}


# Create your models here.
class User(AbstractUser):
    username = None

    email = models.EmailField(verbose_name='email', unique=True)
    avatar = models.ImageField(verbose_name='avatar', **NULLABLE)
    phone = models.CharField(verbose_name='phone', max_length=30, **NULLABLE)
    country = models.CharField(verbose_name='country', max_length=40, **NULLABLE)
    is_active = models.BooleanField(verbose_name='is_active', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
