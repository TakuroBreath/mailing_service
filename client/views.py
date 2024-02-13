from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from client.forms import ClientForm
from client.models import Client


# Create your views here.
class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client:client_list')

    extra_context = {
        'title': 'Создание клиента'
    }


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm

    extra_context = {
        'title': 'Редактирование клиента'
    }

    def get_success_url(self):
        return reverse('client:client_view', args=[self.kwargs.get('pk')])

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    ordering = ('last_name',)
    extra_context = {
        'title': 'Клиенты сервиса'
    }


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    extra_context = {
        'title': 'Просмотр клиента'
    }


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('client:client_list')

    extra_context = {
        'title': 'Удаление клиента'
    }

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser
