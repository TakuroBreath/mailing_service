from django.urls import path

from newletter.apps import NewletterConfig
from newletter.views import MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, \
    MessageDeleteView, MailingLogsListView, SettingsListView, SettingCreateView, SettingUpdateView, SettingDeleteView

app_name = NewletterConfig.name

urlpatterns = [
    path('list/', MessageListView.as_view(), name='message_list'),
    path('list/detail/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('list/create/', MessageCreateView.as_view(), name='message_create'),
    path('list/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('list/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
    path('logs/', MailingLogsListView.as_view(), name='report_list'),
    path('settings/list', SettingsListView.as_view(), name='setting_list'),
    path('settings/create', SettingCreateView.as_view(), name='setting_create'),
    path('settings/update/<int:pk>', SettingUpdateView.as_view(), name='setting_update'),
    path('settings/delete/<int:pk>', SettingDeleteView.as_view(), name='setting_delete'),
]
