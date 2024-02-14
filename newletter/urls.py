from django.urls import path

from newletter.apps import NewletterConfig
from newletter.views import MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, \
    MessageDeleteView, MailingLogsListView

app_name = NewletterConfig.name

urlpatterns = [
    path('list/', MessageListView.as_view(), name='message_list'),
    path('list/detail/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('list/create/', MessageCreateView.as_view(), name='message_create'),
    path('list/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('list/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
    path('logs/', MailingLogsListView.as_view(), name='log_list'),
]