from django.core.mail import send_mail
from django.conf import settings
from .models import Mailing, MailingAttempt
from django.utils import timezone


def send_mailing(mailing):
    recipients = mailing.recipients.all()
    message = mailing.message

    for recipient in recipients:
        try:
            send_mail(
                subject=message.topic,
                message=message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            MailingAttempt.objects.create(
                mailing=mailing,
                recipient=recipient,
                status='success',
                server_response='OK'
            )
        except Exception as e:
            MailingAttempt.objects.create(
                mailing=mailing,
                recipient=recipient,
                status='fail',
                server_response=str(e)
            )

def run_mailing(mailing_id):
    mailing = Mailing.objects.get(id=mailing_id)
    mailing.status = 'Запущена'
    mailing.save()

    send_mailing(mailing)

    mailing.finish_sending = timezone.now()
    mailing.status = 'Завершена'
    mailing.save()
