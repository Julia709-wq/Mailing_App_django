from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('owner', 'Владелец'),
        ('manager', 'Менеджер'),
    )

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, verbose_name='Email')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='owner')
    email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    @property
    def successful_attempts(self):
        from mailing_app.models import MailingAttempt
        return MailingAttempt.objects.filter(
            mailing__owner=self, status="success"
        ).count()

    @property
    def failed_attempts(self):
        from mailing_app.models import MailingAttempt
        return MailingAttempt.objects.filter(
            mailing__owner=self, status="fail"
        ).count()

    @property
    def sent_messages_count(self):
        from mailing_app.models import MailingAttempt
        return MailingAttempt.objects.filter(
            mailing__owner=self, status="success"
        ).count()
