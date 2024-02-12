from django.conf import settings
from django.db import models

from client.models import Client
from users.models import NULLABLE


# Create your models here.
class MailingSettings(models.Model):
    send_time = models.DateTimeField(verbose_name='Время рассылки')

    frequency_choices = [
        ('Daily', 'Ежедневно'),
        ('Weekly', 'Еженедельно'),
        ('Monthly', 'Ежемесячно'),
    ]
    frequency = models.CharField(max_length=30, choices=frequency_choices, verbose_name='Регулярность')

    status_choices = [
        ('Created', 'Создана'),
        ('Started', 'Запущена'),
        ('Completed', 'Завершена'),
    ]
    status = models.CharField(max_length=30, choices=status_choices, verbose_name='статус рассылки')

    def __str__(self):
        return f'{self.send_time} - {self.frequency}'

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'


class Message(models.Model):
    client = models.ManyToManyField(Client, verbose_name='Клиент')
    mailing_settings = models.ForeignKey(MailingSettings, on_delete=models.SET_NULL, null=True,
                                         verbose_name='Настройки')

    title = models.CharField(max_length=255, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Текст письма')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец')
    is_active = models.BooleanField(default=True, verbose_name='Активна?')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingLogs(models.Model):
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, verbose_name='Рассылка')
    datetime_attempt = models.DateTimeField(auto_now_add=True, verbose_name='Время попытки')
    status = models.CharField(max_length=30, verbose_name='Статус')
    server_response = models.TextField(**NULLABLE, verbose_name='Ответ сервиса')

    def __str__(self):
        return f'{self.status} в {self.datetime_attempt}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
