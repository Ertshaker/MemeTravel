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
                               widget=forms.TextInput(attrs={'type': 'text', 'class': 'username_field',
                                                             'placeholder': 'Имя пользователя'}),
                               validators=[UnicodeUsernameValidator(), check_username])
    password = forms.CharField(label='Пароль', required=True, max_length=30,
                               widget=forms.PasswordInput(
                                   attrs={'type': 'password', 'class': 'password_field', 'placeholder': 'Пароль'}),
                               validators=[check_password])
    confirm_password = forms.CharField(label='Повторите пароль', required=True, max_length=30,
                                       widget=forms.PasswordInput(
                                           attrs={'type': 'password', 'placeholder': 'Повторите пароль'}))
    email = forms.CharField(label='Email', min_length=3, max_length=30, widget=forms.TextInput(
        attrs={'type': 'email', 'class': 'email_field', 'placeholder': 'Email'}))
    first_name = forms.CharField(label='Имя', max_length=30,
                                 widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Имя'}))
    last_name = forms.CharField(label='Фамилия', max_length=30,
                                widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Фамилия'}))
    avatar = forms.ImageField(label='Изображение', required=False)
    favorite_memes = forms.ModelMultipleChoiceField(queryset=Meme.objects.all(), required=False)
    status = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', required=True, max_length=30,
                               widget=forms.TextInput(
                                   attrs={'type': 'text', 'class': 'form-input', 'placeholder': 'Логин'}))
    password = forms.CharField(label='Пароль', required=True, max_length=30,
                               widget=forms.PasswordInput(
                                   attrs={'type': 'password', 'class': 'form-input', 'placeholder': 'Пароль'}))


class AddMemeForm(forms.ModelForm):
    class Meta:
        model = Meme
        fields = ['name', 'date', 'description',
                  'history', 'meaning', 'cultural_influence',
                  'using_examples', 'path_to_img']
        labels = {'name': 'Название', 'date': 'Дата появления', 'description': 'Описание',
                  'history': 'История происхождения', 'path_to_img': 'Изображение мема',
                  'meaning': 'Значение и символика', 'cultural_influence': 'Культурное влияние',
                  'using_examples': 'Примеры и использование'}
        widgets = {'date': forms.TextInput(attrs={'type': 'date'})}

    additional_image = forms.ImageField(label='Дополнительное изображение', required=False)


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Старый пароль', required=True, max_length=255,
                                   widget=forms.PasswordInput(
                                       attrs={'type': 'password', 'placeholder': 'Старый пароль'}))
    new_password = forms.CharField(label='Новый пароль', required=True, max_length=255,
                                   widget=forms.PasswordInput(
                                       attrs={'type': 'password', 'placeholder': 'Новый пароль'}),
                                   validators=[check_password])


class AddFriendForm(forms.Form):
    friend_name = forms.CharField(label='Имя друга', max_length=30,
                                  widget=forms.TextInput(attrs={'type': 'text'}))


class ChangeAvatarForm(forms.Form):
    image = forms.ImageField(label='Новый аватар', widget=forms.FileInput(attrs={"id": "image_field"}))
