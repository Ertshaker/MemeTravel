from django import forms
from PIL import Image

from Site.models import Meme


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Логин', required=True, max_length=30,
                               widget=forms.TextInput(attrs={'type': 'text'}))
    password = forms.CharField(label='Пароль', required=True, max_length=30,
                               widget=forms.PasswordInput(attrs={'type': 'password'}))
    confirm_password = forms.CharField(label='Повторите пароль', required=True, max_length=30,
                                       widget=forms.PasswordInput(attrs={'type': 'password'}))
    email = forms.CharField(label='Email', min_length=3, max_length=30)
    first_name = forms.CharField(label='Имя', max_length=30, widget=forms.TextInput(attrs={'type': 'text'}))
    last_name = forms.CharField(label='Фамилия', max_length=30, widget=forms.TextInput(attrs={'type': 'text'}))


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', required=True, max_length=30,
                               widget=forms.TextInput(attrs={'type': 'text'}))
    password = forms.CharField(label='Пароль', required=True, max_length=30,
                               widget=forms.PasswordInput(attrs={'type': 'password'}))

# class AddMemeForm(forms.Form):
#     name = forms.CharField(label='Название', required=True, max_length=30,
#                                widget=forms.TextInput(attrs={'type': 'text'}))
#     date = forms.DateField(label='Дата появления', widget=forms.TextInput(attrs={'type': 'date'}))
#     date_peek = forms.DateField(label='Дата самой высокой популярности', widget=forms.TextInput(attrs={'type': 'date'}))
#     popularity = forms.IntegerField(label='Популярность', widget=forms.NumberInput(attrs={'type': 'number'}))
#     path_to_img = forms.ImageField(label='Изображение')
#     description = forms.CharField(label='Описание', required=True, widget=forms.Textarea(attrs={'type': 'text'}))

class AddMemeForm(forms.ModelForm):
    class Meta:
        model = Meme
        fields = ['name', 'date', 'date_peek', 'popularity', 'path_to_img', 'description']