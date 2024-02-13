from django import forms

from client.models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'patronymic', 'email', 'comment')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Surname'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Patronymic'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Comment here:'}),
        }

        labels = {
            'patronymic': 'Отчество',
            'comment': 'Комментарий',
        }
