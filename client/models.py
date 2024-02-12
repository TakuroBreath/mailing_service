from django.db import models

from users.models import NULLABLE


# Create your models here.
class Client(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    patronymic = models.CharField(**NULLABLE, max_length=100, verbose_name='Отчество')
    email = models.EmailField(unique=True, max_length=255, verbose_name='Почта')
    comment = models.TextField(**NULLABLE, verbose_name='Комментарий')

    def __str__(self):
        return f'Клиент {self.first_name} с почтой {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
