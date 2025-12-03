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
        fields = ['start_time', 'end_time', 'status', 'message', 'recipients', ]

        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'recipients': forms.SelectMultiple(attrs={'size': '5'}),
            'status': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['start_time'].required = True
        self.fields['end_time'].required = True
        self.fields['recipients'].help_text = 'Для выбора нескольких получателей: Ctrl+клик (Windows) или Cmd+клик (Mac)'

        if user is not None:
            if hasattr(user, 'role') and user.role == 'owner':
                self.fields['recipients'].queryset = Recipient.objects.filter(owner=user)
            else:
                self.fields['recipients'].queryset = Recipient.all()
        else:
            self.fields['recipients'].queryset = Recipient.objects.all()


    def clean(self):
        """Валидация времени начала и окончания"""
        cleaned = super().clean()
        start = cleaned.get('start_time')
        end = cleaned.get('end_time')
        now = timezone.now()

        if start and start < now:
            self.add_error('start_time', 'Время начала должно быть в прошлом.')
        if start and end and start >= end:
            self.add_error('end_time', 'Время окончания должно быть позже времени начала.')
        return cleaned
