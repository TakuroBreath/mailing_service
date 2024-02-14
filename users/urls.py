from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, logout_view, RegisterView, UserUpdateView, UserVerifyView, \
    ManagerView, UserListView, DisableUserView, DisableMessageView, UserDeleteView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/verify/<int:pk>/', UserVerifyView.as_view(), name='verification'),
    path('profile_edit/', UserUpdateView.as_view(), name='profile_edit'),
    path('profile_delete/<int:pk>/', UserDeleteView.as_view(), name='profile_delete'),
    path('manager/', ManagerView.as_view(), name='manager_profile'),
    path('users_list/', UserListView.as_view(), name='users_list'),
    path('disable_user/<int:pk>/', DisableUserView.as_view(), name='user_disable'),
    path('disable_message/<int:pk>/', DisableMessageView.as_view(), name='message_disable'),
]
