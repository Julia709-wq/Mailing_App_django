from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.conf.urls.static import static

from users.apps import UsersConfig
from users.views import UserRegisterView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='mailing_app:main_menu'), name='logout'),
    path('register/', UserRegisterView.as_view(template_name='register.html'), name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)