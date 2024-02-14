from django import forms

from newletter.models import Message
from newletter.validators import validate_mail


class MessageForm(forms.ModelForm):
    title = forms.CharField(validators=[validate_mail],
                            label='Название рассылки',
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Название',
                                }
                            ))

    body = forms.CharField(validators=[validate_mail],
                           label='Содержимое рассылки',
                           widget=forms.Textarea(
                               attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Содержимое рассылки',
                               }
                           ))

    class Meta:
        model = Message
        fields = ('client', 'title', 'body', 'mailing_settings',)
        widgets = {
            'client': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'mailing_settings': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'client': 'Выберите клиентов',
            'mailing_settings': 'Выберите настройки',
        }
