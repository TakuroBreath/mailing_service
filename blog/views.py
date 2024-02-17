
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView, UpdateView, DetailView, CreateView, ListView

from blog.models import Blog


# Create your views here.
class BlogListView(LoginRequiredMixin, ListView):
    model = Blog
    extra_context = {
        'title': 'Blog'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['content_manager'] = user.groups.filter(name='content_manager').exists() or user.is_superuser
        return context


class BlogCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Blog
    fields = ('title', 'content', 'preview')
    success_url = reverse_lazy('blog:blog_list')
    extra_context = {
        'title': 'Add new article',
    }

    def test_func(self):
        return self.request.user.groups.filter(name='content_manager').exists() or self.request.user.is_superuser


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    extra_context = {
        'title': 'View blog article'
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    fields = ('title', 'content', 'preview')
    success_url = reverse_lazy('blog:blog_list')
    extra_context = {
        'title': 'Edit article',
    }

    def test_func(self):
        return self.request.user.groups.filter(name='content_manager').exists() or self.request.user.is_superuser


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
    extra_context = {
        'title': 'Delete article',
    }

    def test_func(self):
        return self.request.user.groups.filter(name='content_manager').exists() or self.request.user.is_superuser
