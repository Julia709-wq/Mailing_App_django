from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from users.forms import MyUserCreationForm
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View

from users.models import User


class UserRegisterView(CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = MyUserCreationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        activation_link = self.request.build_absolute_uri(
            reverse('users:email_activate', kwargs={'uidb64': uid, 'token': token})
        )

        send_mail(
            "Подтверждение email",
            f"Для активации перейдите по ссылке: {activation_link}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )

        # return HttpResponse("На Ваш email отправлено письмо для подтверждения")
        return render(self.request, 'users/email_verification.html', context={'user': user})


def email_activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        return HttpResponse("Неверная ссылка")

    if not default_token_generator.check_token(user, token):
        return HttpResponse("Ссылка недействительна или устарела")

    user.email_verified = True
    user.is_active = True
    user.save()

    return redirect('users:login')


class UsersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'manager':
            raise PermissionDenied("Недостаточно прав")
        return super().dispatch(request, *args, **kwargs)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'users'

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'manager':
            raise PermissionDenied("Недостаточно прав")
        return super().dispatch(request, *args, **kwargs)


@login_required
def deactivate_user(request, pk):
    if request.user.role != "manager":
        raise PermissionDenied("Недостаточно прав")

    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        raise PermissionDenied("Вы не можете заблокировать сами себя.")

    user.is_active = False
    user.save()
    return redirect('users:user_list')


@login_required
def activate_user(request, pk):
    if request.user.role != "manager":
        raise PermissionDenied("Недостаточно прав")

    user = get_object_or_404(User, pk=pk)
    user.is_active = True
    user.save()
    return redirect('users:user_list')


