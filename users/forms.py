from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')
