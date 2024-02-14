from django.core.exceptions import ValidationError


def validate_mail(value):
    prohibited_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                        'радар']

    for word in prohibited_words:
        if word in value.lower():
            raise ValidationError(f"Вы используете запрещенное слово '{word}' в тексте")
