from django.core.mail import send_mail
from django.core.management import BaseCommand

from newletter.models import MailingLogs, Message


class Command(BaseCommand):
    help = 'Отправить все сообщения'

    def handle(self, *args, **options):
        messages = Message.objects.all()

        for message in messages:
            subject = message.title
            message_body = message.body
            from_email = 'mailingservice@gmail.com'
            recipient_list = [client.email for client in message.client.all()]

            try:
                send_mail(subject, message_body, from_email, recipient_list, fail_silently=False)

                MailingLogs.objects.create(
                    message=message,
                    status='Успешно отправлено',
                    server_response='Рассылка успешно отправлена'
                )

                self.stdout.write(self.style.SUCCESS('Сообщения отправлены!'))

            except Exception as e:
                MailingLogs.objects.create(
                    message=message,
                    status='Ошибка отправки',
                    server_response=str(e)
                )
