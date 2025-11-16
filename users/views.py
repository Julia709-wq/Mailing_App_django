from django.urls import reverse_lazy
from django.views.generic import CreateView
from users.forms import MyUserCreationForm

from users.models import User


class UserRegisterView(CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = MyUserCreationForm
    success_url = reverse_lazy('users:login')


