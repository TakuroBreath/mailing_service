from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from newletter.forms import MessageForm
from newletter.models import Message, MailingLogs, MailingSettings


# Create your views here.
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    ordering = ('title',)
    extra_context = {
        'title': 'Список рассылок'
    }


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    extra_context = {
        'title': 'Просмотр рассылки'
    }


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('newletter:message_list')

    extra_context = {
        'title': 'Создание рассылки'
    }

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    form_class = MessageForm

    extra_context = {
        'title': 'Редактирование рассылки'
    }

    def get_success_url(self):
        return reverse('newletter:message_detail', args=[self.kwargs.get('pk')])

    def test_func(self):
        return self.request.user == self.get_object().owner or self.request.user.is_superuser


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('newletter:message_list')

    extra_context = {
        'title': 'Удаление рассылки'
    }

    def test_func(self):
        return self.request.user == self.get_object().owner or self.request.user.is_superuser


class MailingLogsListView(LoginRequiredMixin, ListView):
    model = MailingLogs
    template_name = "newletter/logs_list.html"
    extra_context = {
        'title': 'Отчет рассылок'
    }

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return MailingLogs.objects.all()
        else:
            return MailingLogs.objects.filter(message__owner=self.request.user)


class SettingsListView(LoginRequiredMixin, ListView):
    model = MailingSettings
    template_name = "newletter/settings_list.html"
    extra_context = {
        'title': 'Настройки рассылок'
    }


class SettingCreateView(LoginRequiredMixin, CreateView):
    model = MailingSettings
    template_name = "newletter/settings_form.html"

    success_url = reverse_lazy('newletter:setting_list')
    fields = ('send_time', 'frequency', 'status',)

    extra_context = {
        'title': 'Создание Настройки'
    }


class SettingUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingSettings
    template_name = "newletter/settings_form.html"
    success_url = reverse_lazy('newletter:setting_list')
    fields = ('send_time', 'frequency', 'status',)

    extra_context = {
        'title': 'Редактирование Настройки'
    }


class SettingDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingSettings
    template_name = "newletter/settings_confirm_delete.html"
    success_url = reverse_lazy('newletter:message_list')

    extra_context = {
        'title': 'Удаление настройки'
    }
