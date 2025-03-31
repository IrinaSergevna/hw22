from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserUpdateForm
from .models import CustomUser
import secrets


class UserCreateView(CreateView):
    """Представление для регистрации нового пользователя с подтверждением по email."""

    model = CustomUser #модель пользователя.
    form_class = CustomUserCreationForm # форма для создания пользователя.
    success_url = reverse_lazy('users:login') # URL для перенаправления после успешной регистрации.
    template_name = 'register.html'

    def form_valid(self, form):
        """Подтверждение регистрации."""

        user = form.save()
        user.is_active = False
        user.token = secrets.token_hex(16)
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{user.token}/'
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет, перейди по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    """Подтверждает email пользователя по токену и активирует аккаунт."""

    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.token = None
    user.save()
    return redirect('users:login') # Перенаправление на страницу входа.


class LoginView(LoginView):
    """Представление для входа пользователя в систему."""

    form_class = CustomAuthenticationForm
    template_name = 'login.html'
    redirect_authenticated_user = True # Перенаправляет авторизованных пользователей.


class LogoutView(LogoutView):
    """Представление для выхода пользователя из системы."""

    next_page = reverse_lazy('catalog:home') # URL для перенаправления после выхода.


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для обновления профиля текущего пользователя."""

    model = CustomUser
    form_class = CustomUserUpdateForm # форма для обновления профиля.
    template_name = 'profile.html'
    success_url = reverse_lazy('catalog:home') # URL для перенаправления после успешного обновления.

    def get_object(self):
        """Возвращает текущего пользователя для редактирования."""

        return self.request.user