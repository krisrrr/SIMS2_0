from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин:', widget=forms.TextInput())
    password = forms.CharField(label='Пароль:', widget=forms.PasswordInput())


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    # mac_address = forms.CharField()
    # auth_key = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class UserDeviceDataForm(forms.Form):
    mac_address = forms.CharField(max_length=150, label='MAC-адрес:')
    auth_key = forms.CharField(max_length=150, label='Ключ аутентификации (Auth Key):')
