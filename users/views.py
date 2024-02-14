import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, View, ListView, DeleteView

from newletter.models import Message
from users.forms import UserRegisterForm, UserForm, VerificationForm
from users.models import User


# Create your views here.
class LoginView(BaseLoginView):
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Log in to account'
    }

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Вы успешно авторизовались')
        return response


def logout_view(request):
    logout(request)
    reverse_lazy('main:main_window')


class RegisterView(CreateView):
    model = User
    extra_context = {
        'title': 'Registration'
    }
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        generate_code = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        user.verify_code = generate_code
        user.save()

        send_mail(
            subject='Код верификации',
            message=f'Пожалуйста, для вашей верификации и активации аккаунта введите код: {generate_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return redirect(reverse('users:verification', kwargs={'pk': user.pk}))


class UserVerifyView(View):
    template_name = 'users/verification.html'
    extra_context = {
        'title': 'Verification'
    }

    def get(self, request, *args, **kwargs):
        form = VerificationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = VerificationForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['verify_code']
            user_pk = kwargs.get('pk')
            user = get_object_or_404(User, pk=user_pk)

            if entered_code == user.verify_code:
                user.is_active = True
                user.save()
                messages.success(request, 'Аккаунт активирован')
                return redirect(reverse('users:login'))
            else:
                messages.error(request, 'Неверный код верификации.')

        return render(request, self.template_name, {'form': form})


class UserListView(UserPassesTestMixin, ListView):
    model = User
    extra_context = {
        'title': 'Users'
    }

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser


class UserUpdateView(UpdateView):
    model = User
    extra_context = {
        'title': 'Edit profile'
    }
    success_url = reverse_lazy('users:profile_edit')
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('main:main_window')
    extra_context = {
        'title': 'Delete account',
    }


class ManagerView(UserPassesTestMixin, View):
    template_name = 'users/manager.html'

    def get(self, request, *args, **kwargs):
        context = {
            'title': 'Manager account',
        }
        return render(request, self.template_name, context)

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser


class DisableUserView(UserPassesTestMixin, View):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)

        if user.is_active:
            user.is_active = False
        elif not user.is_active:
            user.is_active = True

        user.save()
        return redirect('users:users_list')

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser


class DisableMessageView(UserPassesTestMixin, View):
    def get(self, request, pk):
        message = Message.objects.get(pk=pk)

        if message.is_active:
            message.is_active = False
        elif not message.is_active:
            message.is_active = True

        message.save()
        return redirect('newsletter:message_detail', pk=pk)

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser
