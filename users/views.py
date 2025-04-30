from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserUpdateForm
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponseRedirect


class UserCreateView(CreateView):
    """Представление для регистрации нового пользователя с подтверждением по email."""

    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'register.html'

    def form_valid(self, form):
        """Обработка валидной формы, отправка приветственного письма."""

        user = form.save()
        send_mail(
            subject=f"Привет, {user.username}!",
            message="Спасибо за регистрацию на нашем сайте.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        messages.success(self.request, f"Привет, {user.username}! Спасибо за регистрацию на нашем сайте.")
        login(self.request, user)

        return HttpResponseRedirect(reverse('users:profile'))


class LoginView(LoginView):
    """Представление для входа пользователя в систему."""
    form_class = CustomAuthenticationForm
    template_name = 'login.html'
    redirect_authenticated_user = True  # Перенаправляет авторизованных пользователей.


class LogoutView(LogoutView):
    """Представление для выхода пользователя из системы."""

    next_page = reverse_lazy('catalog:home')  # URL для перенаправления после выхода.


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для обновления профиля текущего пользователя."""

    model = CustomUser
    form_class = CustomUserUpdateForm  # форма для обновления профиля.
    template_name = 'profile.html'
    success_url = reverse_lazy('catalog:home')  # URL для перенаправления после успешного обновления.

    def get_object(self):
        """Возвращает текущего пользователя для редактирования."""
        return self.request.user
