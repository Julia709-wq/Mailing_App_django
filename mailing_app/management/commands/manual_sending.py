from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = "Отправить письмо вручную: тема, текст, email получателя."

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email получателя')
        parser.add_argument('subject', type=str, help='Тема письма')
        parser.add_argument('message', type=str, help='Текст письма')

    def handle(self, *args, **kwargs):
        email = kwargs['email']
        subject = kwargs['subject']
        message = kwargs['message']

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка: {e}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Письмо отправлено на {email}"))
