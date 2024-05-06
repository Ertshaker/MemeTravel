from PIL import Image
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib import messages

from Site.models import *


# Create your views here.

def index(request):
    return render(request, 'inxex.html')
def encyclopedia(request):
    memes = Meme.objects.all()
    return render(request, 'encyclopedia.html', {"memes": memes})
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                print("Invalid login details: {0}, {1}".format(username, password))
                messages.error(request, 'Неверные логин или пароль!.')
                return HttpResponseRedirect('/login', locals())
        else:
            return HttpResponseRedirect('/login', locals())
        return HttpResponseRedirect('/', locals())
    else:
        form = LoginForm()
        return render(request, 'login.html', {'login_form': form})

def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            confirmed_password = form.cleaned_data.get('confirm_password')
            if password != confirmed_password:
                print("Invalid password details: {0}, {1}".format(password, confirmed_password))
                messages.error(request, 'Пароли не совпадают!.')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            user = Account.objects.create_user(username, email, password)
            user.last_name = last_name
            user.first_name = first_name
            user.save()
            if user is not None:
                login(request, user)
            else:
                return HttpResponseRedirect('/login', locals())
        else:
            return HttpResponseRedirect('/login', locals())
        return HttpResponseRedirect('/', locals())
    else:
        form = RegistrationForm()
        return render(request, 'authorization.html', {'registration_form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/', locals())

def add_meme(request):
    if request.method == 'POST':
        form = AddMemeForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            instance = form.save(commit=False)

            name = form.cleaned_data.get('name')
            date = form.cleaned_data.get('date')
            date_peek = form.cleaned_data.get('date_peek')
            popularity = form.cleaned_data.get('popularity')
            path_to_img = form.cleaned_data.get('path_to_img')
            description = form.cleaned_data.get('description')
            meme = Meme(name=name, date=date, date_peek=date_peek, popularity=popularity, description=description, path_to_img=img)
            if meme is not None:
                meme.save()
            else:
                print("Invalid meme details: {0}, {1}, {2}, {3}, {4}, {5}".format(name, date, date_peek, popularity, path_to_img, description))
                messages.error(request, 'Что то пошло не так!')
                return HttpResponseRedirect('/add_meme', locals())
            return HttpResponseRedirect('/encyclopedia', locals())
        else:
            return HttpResponseRedirect('/encyclopedia', locals())
    else:
        form = AddMemeForm()
        return render(request, 'addmeme.html', {'addmeme_form': form})


def create_view(request, *args, **kwargs):
    route = args[0]
    if route == "friend":
        return render(request, 'create/friend.html')
    elif route == "account":
        return render(request, 'create/account.html')
