from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from mailing_app.apps import MailingAppConfig
from mailing_app.views import (main_menu, RecipientListView, RecipientCreateView, RecipientUpdateView,
                               RecipientDetailView, RecipientDeleteView, MessageListView, MessageCreateView,
                               MessageUpdateView, MessageDetailView, MessageDeleteView, MailingListView,
                               MailingCreateView, MailingUpdateView, MailingDetailView, MailingDeleteView, MailingAttemptListView)

app_name = MailingAppConfig.name

urlpatterns = [
    path('', main_menu, name='main_menu'),
    path('recipient/list/', RecipientListView.as_view(), name='recipient_list'),
    path('recipient/create/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipient/update/<int:pk>/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipient/detail/<int:pk>/', RecipientDetailView.as_view(), name='recipient_detail'),
    path('recipient/delete/<int:pk>/', RecipientDeleteView.as_view(), name='recipient_delete'),

    path('message/list/', MessageListView.as_view(), name='messages_list'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message/detail/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    path('mailing/list/', MailingListView.as_view(), name='mailings_list'),
    path('mailing/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/detail/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),

    path('mailing_attempts/', MailingAttemptListView.as_view(), name='mailing_attempts'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)