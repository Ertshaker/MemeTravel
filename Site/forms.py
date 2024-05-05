from django import forms

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=30, widget=forms.TextInput(attrs={'type': 'text'}))
    password = forms.CharField(label='Пароль', max_length=30, widget=forms.PasswordInput(attrs={'type': 'password'}))
    confirm_password = forms.CharField(label='Повторите пароль', max_length=30, widget=forms.PasswordInput(attrs={'type': 'password'}))
    email = forms.CharField(label='Email', min_length=3, max_length=30)
    first_name = forms.CharField(label='Имя', max_length=30, widget=forms.TextInput(attrs={'type': 'text'}))
    last_name = forms.CharField(label='Фамилия', max_length=30, widget=forms.TextInput(attrs={'type': 'text'}))

class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=30, widget=forms.TextInput(attrs={'type': 'text'}))
    password = forms.CharField(label='Пароль', max_length=30, widget=forms.PasswordInput(attrs={'type': 'password'}))
