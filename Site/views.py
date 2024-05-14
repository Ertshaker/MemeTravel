from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView

from .forms import *
from django.contrib import messages
from django.conf import settings

from Site.models import *

class UserDetailView(DetailView):
    model = Account
    template_name = 'user.html'
    context_object_name = 'user'
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.extra_context["is_current_user"] = request.user.username == kwargs["username"]
        self.extra_context["ChangePasswordForm"] = ChangePasswordForm()

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = Account.objects.get(username=kwargs["username"])
        form = ChangePasswordForm(request.POST)
        if not form.is_valid():
            return HttpResponse(
                '<img src="/media/svofard_404.png"/> <br>ТВОЙ ПАПАША ГНИДА СЛУЖИЛ ВО ВЬЕТНАМЕ?!!?!??!?!!?!?? <br> СЕР, ДА, СЕР!!!!')
        if not user.check_password(form.cleaned_data['old_password']):
            messages.error(request, "ТЫ ДОЛБАЁБ")
            return render(request, 'profile.html', {"user": user, "ChangePasswordForm": form})

        # form.full_clean()
        username = user.username
        new_password = form.cleaned_data['new_password']
        user.set_password(new_password)
        user.save()

        login(request, authenticate(username=username, password=new_password))
        return render(request, 'user.html', {"user": user, "ChangePasswordForm": form})

    def get_object(self, queryset=None):
        username = self.kwargs['username']
        return Account.objects.get(username=username)


class MemeDetailView(DetailView):
    model = Meme
    template_name = 'meme.html'
    context_object_name = 'meme'


def index(request):
    context = {
        "user": request.user
    }
    return render(request, 'inxex.html', context=context)


def encyclopedia(request):
    memes = Meme.objects.all()
    user = request.user

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
            messages.error(request, 'Какое то из полей заполнено неверно!')
            messages.error(request, form.errors)
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
            messages.error(request, 'Какое то из полей заполнено неверно!')
            messages.error(request, form.errors)
            return HttpResponseRedirect('/authorization', locals())
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


@login_required(redirect_field_name='next', login_url=settings.LOGIN_URL)
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if not form.is_valid():
            return HttpResponse(
                '<img src="/media/svofard_404.png"/> <br>ТВОЙ ПАПАША ГНИДА СЛУЖИЛ ВО ВЬЕТНАМЕ?!!?!??!?!!?!?? <br> СЕР, ДА, СЕР!!!!')
        if not user.check_password(form.cleaned_data['old_password']):
            messages.error(request, "ТЫ ДОЛБАЁБ")
            return render(request, 'profile.html', {"user": user, "ChangePasswordForm": form})

        # form.full_clean()
        new_password = form.cleaned_data['new_password']
        user.set_password(new_password)
        user.save()

        login(request, authenticate(username=user.username, password=user.password))
        return render(request, 'profile.html', {"user": user, "ChangePasswordForm": form})

    form = ChangePasswordForm()
    favorites = user.favorites.all()
    return render(request, 'profile.html', {"user": user, "ChangePasswordForm": form, 'favorites': favorites})


def test_view(request):
    return render(request, 'test.html')


def friends_view(request, name: str):
    user = Account.objects.get(username=name)
    friends = Friend.objects.filter(user_id=user.id, accepted=True) | Friend.objects.filter(friend_id=user.id,
                                                                                            accepted=True)
    sended_requests = Friend.objects.filter(user_id=user.id, accepted=False)
    got_requests = Friend.objects.filter(friend_id=user.id, accepted=False)
    return render(request, 'friends.html',
                  {'friends': friends, 'is_current_user': request.user == user, 'sended_requests': sended_requests, 'got_requests': got_requests, 'user': user})


def friends_add(request):
    if request.method == 'POST':
        user = request.user
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


def accept_friend(request, user_id: int):
    user = request.user
    friend = Friend.objects.get(user_id=user_id, friend_id=user.id)
    friend.accepted = True
    return HttpResponseRedirect('/friends', locals())
