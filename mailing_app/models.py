from django.db import models
from users.models import User


class Recipient(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=300, verbose_name='Ф.И.О.')
    comment = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, verbose_name='Владелец', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'получатель рассылки'
        verbose_name_plural = 'получатели рассылки'


class Message(models.Model):
    topic = models.CharField(max_length=200, verbose_name='Тема письма')
    body = models.TextField()
    owner = models.ForeignKey(User, verbose_name='Владелец', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('running', 'Запущена'),
        ('finished', 'Завершена')
    ]

    first_sending = models.DateTimeField(auto_now_add=True)
    finish_sending = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='created')
    message = models.ForeignKey(Message, verbose_name='Сообщение', blank=True, null=True, on_delete=models.SET_NULL)
    recipients = models.ManyToManyField(Recipient, verbose_name='Получатель')
    owner = models.ForeignKey(User, verbose_name='Владелец', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.get_status_display()} ({self.first_sending:%Y-%m-%d})"

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

