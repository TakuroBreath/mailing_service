from datetime import datetime, timedelta
from django.core.mail import send_mail

from newletter.models import Message, MailingLogs


def send_letters():
    messages = Message.objects.all()

    current_date = datetime.now().date()
    current_time = datetime.now().time()

    for message in messages:
        if message.mailing_settings.send_time.time() <= current_time and message.mailing_settings.send_time.date() == current_date:

            subject = message.title
            message_body = message.body
            from_email = 'mailingservice@gmail.com'
            recipient_list = [client.email for client in message.client.all()]

            try:
                send_mail(subject, message_body, from_email, recipient_list, fail_silently=False)

                if message.mailing_settings.frequency == 'Daily':
                    message.mailing_settings.send_time += timedelta(days=1)
                elif message.mailing_settings.frequency == 'Weekly':
                    message.mailing_settings.send_time += timedelta(days=7)
                elif message.mailing_settings.frequency == 'Monthly':
                    message.mailing_settings.send_time += timedelta(days=30)
                message.mailing_settings.save()

                MailingLogs.objects.create(
                    message=message,
                    status='Успешно отправлено',
                    server_response='Рассылка успешно отправлена'
                )

            except Exception as e:
                MailingLogs.objects.create(
                    message=message,
                    status='Ошибка отправки',
                    server_response=str(e)
                )
