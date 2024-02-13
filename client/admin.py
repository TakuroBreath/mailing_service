from django.contrib import admin

from client.models import Client


# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'patronymic', 'email',)
    search_fields = ('last_name', 'email',)
