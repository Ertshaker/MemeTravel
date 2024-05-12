from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib import messages

from Site.models import *


# Create your views here.

def index(request):
    context = {
        "user": get_user(request.session)
    }
    return render(request, 'inxex.html', context=context)


def encyclopedia(request):
    memes = Meme.objects.all()
    user = get_user(request.session)

    galery = MemeGallery.objects.all()
    try:
        user = Account.objects.get(id=request.session.get("_auth_user_id"))
    except Account.DoesNotExist:
        user = Account(username="Обыватель бездны")

    context = {
        "memes": memes,
        "user": user,
        "MemeGallery": galery
    }

    return render(request, 'encyclopedia.html', context=context)


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
                messages.info(request, 'Неверные логин или пароль!')
                return HttpResponseRedirect('/login', locals())
        else:
            return HttpResponseRedirect('/login', locals())
        return HttpResponseRedirect('/', locals())
    else:
        form = LoginForm()
        return render(request, 'login.html', {'login_form': form})


def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            confirmed_password = form.cleaned_data.get('confirm_password')
            if password != confirmed_password:
                print("Invalid password details: {0}, {1}".format(password, confirmed_password))
                messages.error(request, 'Пароли не совпадают!')
                return HttpResponseRedirect('/authorization', locals())

            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            avatar = form.cleaned_data.get('avatar')
            status = form.cleaned_data.get('status')
            favorites = form.cleaned_data.get('favorite_memes')

            All_users = Account.objects.all().values_list('username', flat=True)
            if username in All_users:
                print("This username is already taken! ({0})".format(username))
                messages.error(request, 'Это имя уже занято!')
                return HttpResponseRedirect('/authorization', locals())

            user = Account.objects.create_user(username, email, password)
            user.last_name = last_name
            user.first_name = first_name
            user.avatar = avatar
            user.favorites.set(favorites)

            if user is not None:
                user.save()
                status.user_set.add(user)
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
            description = form.cleaned_data.get('description')
            image = form.cleaned_data.get('path_to_img')

            meme = Meme(name=name, date=date, date_peek=date_peek, popularity=popularity, description=description,
                        path_to_img=image)

            if meme is not None:
                meme.save()
            else:
                print("Invalid meme details: {0}, {1}, {2}, {3}, {4}, {5}".format(name, date, date_peek, popularity,
                                                                                  description, image))
                messages.error(request, 'Что то пошло не так!')
                return HttpResponseRedirect('/add_meme', locals())
            return HttpResponseRedirect('/encyclopedia', locals())
        else:
            messages.error(request, 'Что то пошло не так!')
            return HttpResponseRedirect('/encyclopedia', locals())
    else:
        form = AddMemeForm()
        return render(request, 'create/meme.html', {'addmeme_form': form})


def create_route(request, *args, **kwargs):
    route = args[0]
    if route == "friend":
        return friends_add(request)
    elif route == "account":
        return render(request, 'create/account.html')
    elif route == "meme":
        return add_meme(request)


def get_user(session):
    try:
        user = Account.objects.get(id=session.get("_auth_user_id"))
    except Account.DoesNotExist:
        user = Account(username="Обыватель бездны")

    return user


def profile_view(request):
    user = get_user(request.session)
    if user.username == "Обыватель бездны":
        messages.error(request, "Войди в аккаунт сначала дурень")
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if not form.is_valid():
            return HttpResponse(
                '<img src="/media/svofard_404.png"/> <br>ТВОЙ ПАПАША ГНИДА СЛУЖИЛ ВО ВЬЕТНАМЕ?!!?!??!?!!?!?? <br> СЕР, ДА, СЕР!!!!')
        new_password = form.cleaned_data['new_password']
        user.set_password(new_password)
        user.save()

    return render(request, 'profile.html', {"user": user, "ChangePasswordForm": ChangePasswordForm()})


def friends_view(request):
    user = get_user(request.session)
    friends = Friend.objects.filter(user_id=user.id, accepted=True) | Friend.objects.filter(friend_id=user.id,
                                                                                            accepted=True)
    sended_requests = Friend.objects.filter(user_id=user.id, accepted=False)
    got_requests = Friend.objects.filter(friend_id=user.id, accepted=False)
    return render(request, 'friends.html',
                  {'friends': friends, 'sended_requests': sended_requests, 'got_requests': got_requests})


def friends_add(request):
    if request.method == 'POST':
        user = get_user(request.session)
        form = AddFriendForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('friend_name')
            possible_friend = Account.objects.get(username=name)
            all_friends = Friend.objects.all()
            friend_request = Friend(user_id=user, friend_id=possible_friend, accepted=False)


            if friend_request is not None:
                if not Friend.objects.filter(user_id=user.id, friend_id=possible_friend.id):
                    friend_request.save()
                else:
                    print("Objects already friends or requested!".format(user.username, name))
                    messages.error(request, 'Кажется эта заявка уже есть или вы уже друзья!')
                    return HttpResponseRedirect('/friends', locals())
            else:
                print("Invalid friend details: {0}".format(name))
                messages.error(request, 'Что то пошло не так!')
                return HttpResponseRedirect('/create/friend', locals())
            return HttpResponseRedirect('/friends', locals())
        else:
            messages.error(request, 'Что то пошло не так!')
            return HttpResponseRedirect('/profile', locals())
    else:
        form = AddFriendForm()
        return render(request, 'create/friend.html', {'addfriend_form': form})

def accept_friend(request, user_id):
    user = get_user(request.session)
    friend = Friend.objects.get(user_id=user_id, friend_id=user.id)
    friend.accepted = True
    return HttpResponseRedirect('/friends', locals())
