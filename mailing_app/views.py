from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from .models import Recipient, Message, Mailing
from .forms import RecipientForm, MessageForm, MailingForm
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


def main_menu(request):
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status='Запущена').count()
    unique_recipients = Recipient.objects.count()

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_recipients': unique_recipients
    }

    return render(request, 'mailing_app/main_menu.html', context)


@method_decorator(cache_page(60 * 15), name='dispatch')
class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = 'mailing_app/recipients/recipient_list.html'
    context_object_name = 'recipients'

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.role == 'owner':
            qs = qs.filter(owner=self.request.user)
        return qs


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailing_app/recipients/recipient_form.html'
    success_url = reverse_lazy('mailing_app:recipient_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.role == 'manager':
            raise PermissionDenied("У Вас нет прав для создания получателей.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        recipient = form.save()
        user = self.request.user
        recipient.owner = user
        recipient.save()
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailing_app/recipients/recipient_form.html'
    success_url = reverse_lazy('mailing_app:recipient_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.role == 'manager':
            raise PermissionDenied("У Вас нет прав для редактирования получателей.")
        if obj.owner != request.user:
            raise PermissionDenied("Вы можете редактировать только своих получателей.")

        return super().dispatch(request, *args, **kwargs)


@method_decorator(cache_page(60 * 15), name='dispatch')
class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    template_name = 'mailing_app/recipients/recipient_detail.html'
    context_object_name = 'recipient'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.role == 'owner' and obj.owner != request.user:
            raise PermissionDenied("Вы не можете просматривать чужие рассылки.")

        return super().dispatch(request, *args, **kwargs)


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = 'mailing_app/recipients/recipient_delete.html'
    success_url = reverse_lazy('mailing_app:recipient_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.role == 'manager':
            raise PermissionDenied("У Вас нет прав для удаления получателя.")
        if obj.owner != self.request.user:
            raise PermissionDenied('Вы можете удалять только своих получателей')
        return obj


@method_decorator(cache_page(60 * 15), name='dispatch')
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailing_app/messages/messages_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.role == 'owner':
            qs = qs.filter(owner=self.request.user)
        return qs


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing_app/messages/message_form.html'
    success_url = reverse_lazy('mailing_app:messages_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.role == 'manager':
            raise PermissionDenied("У Вас нет прав для создания сообщения.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing_app/messages/message_form.html'
    success_url = reverse_lazy('mailing_app:messages_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.role == 'manager':
            raise PermissionDenied("У Вас нет прав для редактирования получателей.")
        if obj.owner != request.user:
            raise PermissionDenied("Вы можете редактировать только своих получателей.")

        return super().dispatch(request, *args, **kwargs)


@method_decorator(cache_page(60 * 15), name='dispatch')
class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'mailing_app/messages/message_detail.html'
    context_object_name = 'message'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.role == 'owner' and obj.owner != request.user:
            raise PermissionDenied("Вы не можете просматривать чужие сообщения.")

        return super().dispatch(request, *args, **kwargs)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'mailing_app/messages/message_delete.html'
    success_url = reverse_lazy('mailing_app:messages_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.role == 'manager':
            raise PermissionDenied("У Вас нет прав для удаления получателя.")
        if obj.owner != self.request.user:
            raise PermissionDenied('Вы можете удалять только своих получателей')
        return obj


@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing_app/mailings/mailings_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.role == 'owner':
            qs = qs.filter(owner=self.request.user)
        return qs


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_app/mailings/mailing_form.html'
    success_url = reverse_lazy('mailing_app:mailings_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.role == 'manager':
            raise PermissionDenied("У Вас нет прав для создания рассылки.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_app/mailings/mailing_form.html'
    success_url = reverse_lazy('mailing_app:mailings_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.role == 'manager':
            raise PermissionDenied("У Вас нет прав для редактирования рассылки.")
        if obj.owner != request.user:
            raise PermissionDenied("Вы можете редактировать только свои рассылки.")

        return super().dispatch(request, *args, **kwargs)


@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing_app/mailings/mailing_detail.html'
    context_object_name = 'mailing'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.role == 'owner' and obj.owner != request.user:
            raise PermissionDenied("Вы не можете просматривать чужие рассылки.")

        return super().dispatch(request, *args, **kwargs)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailing_app/mailings/mailing_delete.html'
    success_url = reverse_lazy('mailing_app:mailings_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.role == 'manager':
            raise PermissionDenied("У Вас нет прав для удаления получателя.")
        if obj.owner != self.request.user:
            raise PermissionDenied('Вы можете удалять только своих получателей')
        return obj



