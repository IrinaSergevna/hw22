from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Регистрация пользователя"""

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password1', 'password2', 'avatar', 'phone_number', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Электронная почта'})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Имя пользователя'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Подтверждение пароля'})
        self.fields['avatar'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Номер телефона'})
        self.fields['country'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Страна'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        if commit:
            user.save()
        return user


class CustomUserUpdateForm(forms.ModelForm):
    """Форма для обновления профиля пользователя"""

    class Meta:
        model = CustomUser
        fields = ['username', 'avatar', 'phone_number', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Имя пользователя'})
        self.fields['avatar'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Номер телефона'})
        self.fields['country'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Страна'})


class CustomAuthenticationForm(AuthenticationForm):
    """Форма для аутентификации пользователей"""

    class Meta:
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Электронная почта"
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Электронная почта'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Пароль'})