from django.core.mail import send_mail
from django.conf import settings
from .models import Mailing, MailingAttempt
from django.utils import timezone


def send_mailing(mailing):
    """Отправка писем в рамках конкретной рассылки"""

    succeed = 0
    failed = 0

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
                status=MailingAttempt.STATUS_SUCCESS,
                server_response='OK'
            )
            succeed += 1
        except Exception as e:
            MailingAttempt.objects.create(
                mailing=mailing,
                recipient=recipient,
                status=MailingAttempt.STATUS_FAIL,
                server_response=str(e)
            )
            failed += 1

    return succeed, failed


def run_mailing(mailing_id):
    """Запуск рассылки"""

    mailing = Mailing.objects.get(id=mailing_id)
    mailing.update_status()
    now = timezone.now()

    if not (mailing.start_time <= now <= mailing.end_time):
        return False, 'Отправка запрещена: текущее время вне интервала рассылки.'

    mailing.status = Mailing.STATUS_RUNNING
    mailing.save(update_fields=['status'])
    succeed, failed = send_mailing(mailing)

    mailing.update_status()
    return True, f"Отправка завершена: успешно {succeed}, неуспешно {failed}", (succeed, failed)
