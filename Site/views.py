from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import *

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
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            user = Account.objects.create_user(username, email, password)
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


def create_view(request, *args, **kwargs):
    route = args[0]
    if route == "friend":
        return render(request, 'create/friend.html')
    elif route == "account":
        return render(request, 'create/account.html')
