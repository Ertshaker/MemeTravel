from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, UpdateView
from .forms import *
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import Group

from Site.models import *

class MemesUpdateView(UpdateView):
    model = Meme
    template_name = 'create/meme.html'

    form_class = AddMemeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meme = self.get_object()  # Получаем объект Meme
        form = self.form_class(instance=meme)  # Создаем форму, связанную с объектом Meme
        context['addmeme_form'] = form  # Передаем форму в контекст
        return context


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
            messages.error(request, 'Какое то из полей заполнено неверно!')
            return render(request, 'user.html',
                          {"user": user, 'is_current_user': request.user == user, "ChangePasswordForm": form})
        if not user.check_password(form.cleaned_data['old_password']):
            messages.error(request, 'Старый пароль введен неверно!')
            return render(request, 'user.html',
                          {"user": user, 'is_current_user': request.user == user, "ChangePasswordForm": form})

        # form.full_clean()
        username = user.username
        new_password = form.cleaned_data['new_password']
        user.set_password(new_password)
        user.save()

        login(request, authenticate(username=username, password=new_password))
        return render(request, 'user.html',
                      {"user": user, 'is_current_user': request.user == user, "ChangePasswordForm": form})

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
        if not form.is_valid():
            messages.error(request, 'Какое то из полей заполнено неверно!')
            messages.error(request, form.errors)
            return HttpResponseRedirect('/login', locals())

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            print("Invalid login details: {0}, {1}".format(username, password))
            messages.info(request, 'Неверные логин или пароль!')
            return HttpResponseRedirect('/login', locals())

        login(request, user)

        return HttpResponseRedirect('/', locals())
    else:
        form = LoginForm()
        return render(request, 'login_test.html', {'login_form': form})


def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        print(form.errors)
        if not form.is_valid():
            messages.error(request, 'Какое то из полей заполнено неверно!')
            messages.error(request, form.errors)
            return HttpResponseRedirect('/authorization', locals())

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
        # avatar = form.cleaned_data.get('avatar')
        status = Group.objects.get(name="Пользователь")
        # favorites = form.cleaned_data.get('favorite_memes')
        user = Account.objects.create_user(username, email, password)
        user.last_name = last_name
        user.first_name = first_name
        # user.avatar = avatar
        # user.favorites.set(favorites)


        if user is None:
            return HttpResponseRedirect('/login', locals())

        user.save()
        status.user_set.add(user)
        login(request, user)

        return HttpResponseRedirect('/', locals())
    else:
        form = RegistrationForm()
        return render(request, 'registration.html', {'registration_form': form})

    # def user_register(request):
    #     if request.method == 'POST':
    #         form = RegistrationForm(request.POST, request.FILES)
    #         print(form.errors)
    #         if not form.is_valid():
    #             messages.error(request, 'Какое то из полей заполнено неверно!')
    #             messages.error(request, form.errors)
    #             return HttpResponseRedirect('/authorization', locals())
    #
    #         username = form.cleaned_data.get('username')
    #         password = form.cleaned_data.get('password')
    #         confirmed_password = form.cleaned_data.get('confirm_password')
    #         if password != confirmed_password:
    #             print("Invalid password details: {0}, {1}".format(password, confirmed_password))
    #             messages.error(request, 'Пароли не совпадают!')
    #             return HttpResponseRedirect('/authorization', locals())
    #
    #         email = form.cleaned_data.get('email')
    #         first_name = form.cleaned_data.get('first_name')
    #         last_name = form.cleaned_data.get('last_name')
    #         avatar = form.cleaned_data.get('avatar')
    #         status = form.cleaned_data.get('status')
    #         favorites = form.cleaned_data.get('favorite_memes')
    #         user = Account.objects.create_user(username, email, password)
    #         user.last_name = last_name
    #         user.first_name = first_name
    #         user.avatar = avatar
    #         user.favorites.set(favorites)
    #
    #         if user is None:
    #             return HttpResponseRedirect('/login', locals())
    #
    #         user.save()
    #         status.user_set.add(user)
    #         login(request, user)
    #
    #         return HttpResponseRedirect('/', locals())
    #     else:
    #         form = RegistrationForm()
    #         return render(request, 'registration.html', {'registration_form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/', locals())


def add_meme(request):
    if request.method == 'POST':
        form = AddMemeForm(request.POST, request.FILES)
        print(form.errors)
        if not form.is_valid():
            messages.error(request, 'Что то пошло не так!')
            return HttpResponseRedirect('/encyclopedia', locals())

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

        if meme is None:
            print("Invalid meme details: {0}, {1}, {2}, {3}, {4}, {5}".format(name, date, date_peek, popularity,
                                                                              description, image))
            messages.error(request, 'Что то пошло не так!')
            return HttpResponseRedirect('/add_meme', locals())

        meme.save()

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
            messages.error(request, "ТЫ ЧЁ ТВОРИШЬ???")
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
                  {'friends': friends, 'is_current_user': request.user == user, 'sended_requests': sended_requests,
                   'got_requests': got_requests, 'user': user})


def friends_add(request):
    if request.method == 'POST':
        user = request.user
        form = AddFriendForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'Что то пошло не так!')
            return HttpResponseRedirect(f'/user/{user.username}', locals())

        name = form.cleaned_data.get('friend_name')
        possible_friend = Account.objects.get(username=name)
        all_friends = Friend.objects.all()
        friend_request = Friend(user_id=user, friend_id=possible_friend, accepted=False)

        if friend_request is None:
            print("Invalid friend details: {0}".format(name))
            messages.error(request, 'Что то пошло не так!')
            return HttpResponseRedirect('/create/friend', locals())

        if Friend.objects.filter(user_id=user.id, friend_id=possible_friend.id):
            print("Objects already friends or requested!".format(user.username, name))
            messages.error(request, 'Кажется эта заявка уже есть или вы уже друзья!')
            return HttpResponseRedirect(f'/user/{user.username}/friends', locals())

        friend_request.save()

        return HttpResponseRedirect(f'/user/{user.username}/friends', locals())
    else:
        form = AddFriendForm()
        return render(request, 'create/friend.html', {'addfriend_form': form})


def accept_friend(request, user_id: int):
    user = request.user
    friend = Friend.objects.get(user_id=user_id, friend_id=user.id)
    friend.accepted = True
    return HttpResponseRedirect('/friends', locals())


def add_friend_request(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        friend_id = request.POST.get('friend_id')
        try:
            friend = Friend.objects.get(id=friend_id)
            friend.accepted = True
            friend.save()
            return JsonResponse({'success': True})
        except Friend.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'НЕСУЩЕСТВФУЕТ ААААА'})
    return JsonResponse({'success': False, 'error': 'ИНВАЛИД'})


def remove_friend_request(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        friend_id = request.POST.get('friend_id')
        try:
            friend = Friend.objects.get(id=friend_id)
            friend.accepted = False  # тут фолс вместо тру, как кнопка сверху ток наоборот крч
            friend.save()
            return JsonResponse({'success': True})
        except Friend.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'НЕСУЩЕСТВФУЕТ АААААА'})
    return JsonResponse({'success': False, 'error': 'ИНВАЛИД'})


def add_to_favorites(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        current_user = request.user
        meme = Meme.objects.get(id=request.POST.get('meme_id'))
        user_memes = current_user.favorites.all()

        if not user_memes.filter(id=meme.id):
            current_user.favorites.add(meme)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'МЕМ УЖЕ ДОБАВЛЕН ДУРА'})
    return JsonResponse({'success': False, 'error': 'ИНВАЛИД'})


def remove_from_favorites(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        current_user = request.user
        meme = Meme.objects.get(id=request.POST.get('meme_id'))

        try:
            current_user.favorites.remove(meme)
            return JsonResponse({'success': True})
        except current_user.favorites.ObjectDoesNotExist:
            return JsonResponse({'success': False, 'error': 'МЕМ НЕ НАЙДЕН блин'})
    return JsonResponse({'success': False, 'error': 'IИНВАЛИИД'})
