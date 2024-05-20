from django import forms
from PIL import Image
from django.contrib.auth.validators import UnicodeUsernameValidator
import re
from Site.models import Meme, Account
from django.contrib.auth.models import Group


def check_username(text):
    if re.search('[\u0400-\u04FF]', text):
        raise forms.ValidationError("Username should not have Cyrillic")
    All_users = Account.objects.all().values_list('username', flat=True)
    if text in All_users:
        raise forms.ValidationError("Username is already taken")


def check_password(password):
    if re.search('[\u0400-\u04FF]', password):
        raise forms.ValidationError("Password should not have Cyrillic")
    if " " in password.strip():
        raise forms.ValidationError("Password should not have space")
    if len(password) < 8:
        raise forms.ValidationError("Password should have at least 8 characters")


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Логин', required=True, max_length=30,
                               widget=forms.TextInput(attrs={'type': 'text'}),
                               validators=[UnicodeUsernameValidator(), check_username])
    password = forms.CharField(label='Пароль', required=True, max_length=30,
                               widget=forms.PasswordInput(attrs={'type': 'password'}), validators=[check_password])
    confirm_password = forms.CharField(label='Повторите пароль', required=True, max_length=30,
                                       widget=forms.PasswordInput(attrs={'type': 'password'}))
    email = forms.CharField(label='Email', min_length=3, max_length=30)
    first_name = forms.CharField(label='Имя', max_length=30, widget=forms.TextInput(attrs={'type': 'text'}))
    last_name = forms.CharField(label='Фамилия', max_length=30, widget=forms.TextInput(attrs={'type': 'text'}))
    avatar = forms.ImageField(label='Изображение', required=False)
    favorite_memes = forms.ModelMultipleChoiceField(queryset=Meme.objects.all(), required=False)
    status = forms.ModelChoiceField(queryset=Group.objects.all())
    # class Meta:
    #     model = Account
    #     fields = "__all__"
    #     labels = {'username':'Имя пользователя', 'password':'Пароль', 'email':'Email', 'first_name':'Имя', 'last_name':'Фамилия', 'avatar':'Изображение профиля'}
    #     widgets = {'password': forms.PasswordInput(attrs={'type': 'password'})}
    #
    # confirm_password = forms.CharField(label='Повторите пароль', required=True, max_length=30,
    #                                    widget=forms.PasswordInput(attrs={'type': 'password'}))


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', required=True, max_length=30,
                               widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-input', 'placeholder': 'Логин'}))
    password = forms.CharField(label='Пароль', required=True, max_length=30,
                               widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-input', 'placeholder': 'Пароль'}))


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
        labels = {'name': 'Название', 'date': 'Дата появления', 'date_peek': 'Дата самой высокой популярности',
                  'popularity': 'Популярность', 'description': 'Описание', 'path_to_img': 'Изображение мема'}
        widgets = {'date': forms.TextInput(attrs={'type': 'date'}),
                   'date_peek': forms.TextInput(attrs={'type': 'date'})}


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Старый пароль', required=True, max_length=255, widget=forms.PasswordInput(attrs={'type': 'password'}))
    new_password = forms.CharField(label='Новый пароль', required=True, max_length=255, widget=forms.PasswordInput(attrs={'type': 'password'}), validators=[check_password])


class AddFriendForm(forms.Form):
    friend_name = forms.CharField(label='Имя друга', max_length=30,
                                  widget=forms.TextInput(attrs={'type': 'text'}))
