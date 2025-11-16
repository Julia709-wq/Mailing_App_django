from django import forms
from django.utils import timezone

from .models import Recipient, Message, Mailing


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['name', 'email', 'comment', ]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['topic', 'body',]


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['finish_sending', 'status', 'message', 'recipients', ]

    widgets = {
        'finish_sending': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'placeholder': 'дд.мм.гггг чч:мм',
                'min': timezone.now().strftime('%Y-%m-%dT%H:%M')
            }),
        'recipients': forms.SelectMultiple(attrs={
            'class': 'form-select',
            'size': '5'
        }),
        'status': forms.Select(attrs={'class': 'form-control'}),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['finish_sending'].required = False
        self.fields['finish_sending'].help_text = 'Формат: дд.мм.гггг чч:мм (например: 25.12.2024 14:30)'
        self.fields['finish_sending'].label = 'Окончание отправки (необязательно)'

        self.fields['recipients'].queryset = Recipient.objects.all()
        self.fields[
            'recipients'].help_text = 'Для выбора нескольких получателей: Ctrl+клик (Windows) или Cmd+клик (Mac)'

