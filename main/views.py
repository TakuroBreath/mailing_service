from django.shortcuts import render
from django.views.generic import TemplateView
from random import sample
from blog.models import Blog
from main.services import get_cached_clients
from newletter.models import Message


# Create your views here


class MainView(TemplateView):
    template_name = 'main/main.html'
    extra_context = {
        'title': 'Mailing'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['all_messages'] = Message.objects.all()
        context_data['active_messages'] = Message.objects.filter(is_active=True)
        context_data['all_clients'] = get_cached_clients()
        if len(list(Blog.objects.all())) < 3:
            return context_data
        else:
            context_data['articles'] = sample(list(Blog.objects.all()), 3)
        return context_data
