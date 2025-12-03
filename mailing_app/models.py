from django.db import models
from django.utils import timezone
from users.models import User


class Recipient(models.Model):
    """Модель получателя"""
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
    """Модель сообщения"""
    topic = models.CharField(max_length=200, verbose_name='Тема письма')
    body = models.TextField()
    owner = models.ForeignKey(User, verbose_name='Владелец', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Mailing(models.Model):
    """Модель рассылки"""
    STATUS_CREATED = 'Создана'
    STATUS_RUNNING = 'Запущена'
    STATUS_FINISHED = 'Завершена'

    STATUS_CHOICES = [
        (STATUS_CREATED, 'Создана'),
        (STATUS_RUNNING, 'Запущена'),
        (STATUS_FINISHED, 'Завершена')
    ]

    start_time = models.DateTimeField(verbose_name='Время начала')
    end_time = models.DateTimeField(verbose_name='Время окончания')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')

    message = models.ForeignKey(Message, verbose_name='Сообщение', blank=True, null=True, on_delete=models.SET_NULL)
    recipients = models.ManyToManyField(Recipient, verbose_name='Получатели')
    owner = models.ForeignKey(User, verbose_name='Владелец', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.get_status_display()} ({self.start_time:%Y-%m-%d %H:%M})"

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

    def current_status(self):
        """Определение статуса в зависимости от времени"""
        now = timezone.now()
        if now < self.start_time:
            return self.STATUS_CREATED
        if self.start_time <= now <= self.end_time:
            return self.STATUS_RUNNING
        return self.STATUS_FINISHED

    def update_status(self):
        """Изменение статуса"""
        new_status = self.current_status()
        if self.status != new_status:
            self.status = new_status
            self.save(update_fields=['status'])


class MailingAttempt(models.Model):
    """Модель попытки рассылки"""
    STATUS_SUCCESS = 'Успешно'
    STATUS_FAIL = 'Не успешно'

    STATUS_CHOICES = [
        (STATUS_SUCCESS, 'Успешно'),
        (STATUS_FAIL, 'Неудачно')
    ]

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attempts')
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    server_response = models.TextField(blank=True, null=True)
    attempt_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mailing} -> {self.recipient.email} ({self.status})"

    class Meta:
        verbose_name = 'попытка'
        verbose_name_plural = 'попытки'

