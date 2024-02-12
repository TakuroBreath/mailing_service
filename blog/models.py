from django.db import models

from users.models import NULLABLE


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(**NULLABLE, upload_to='articles/', verbose_name='Превью')
    views_count = models.IntegerField(default=0, verbose_name='Просмотры')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания публикации')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
