import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, reverse
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, UpdateView

from Site.models import *
from .forms import *


class MemesUpdateView(UpdateView):
    model = Meme
    template_name = 'create/meme_test.html'

    form_class = AddMemeForm

    @cache_page(60 * 15)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meme = self.get_object()  # Получаем объект Meme
        form = self.form_class(instance=meme)  # Создаем форму, связанную с объектом Meme
        context['addmeme_form'] = form  # Передаем форму в контекст
        return context

    def form_valid(self, form):
        instance = form.save()
        addit_im = form.cleaned_data['additional_image']
        if addit_im:
            MemeGallery.objects.create(meme=instance, image=addit_im)
        return super(MemesUpdateView, self).form_valid(form)


class UserDetailView(DetailView):
    model = Account
    template_name = 'user.html'
    context_object_name = 'user'
    extra_context = {}

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            HttpResponseRedirect('/login', locals())
        user = self.get_object()
        self.extra_context["is_current_user"] = request.user.username == kwargs["username"]
        self.extra_context["ChangePasswordForm"] = ChangePasswordForm()
        self.extra_context["ChangeAvatarForm"] = ChangeAvatarForm()
        friends = (Friend.objects.filter(user=user.id, accepted=True) |
                   Friend.objects.filter(friend=user.id, accepted=True))
        sent_requests = Friend.objects.filter(user=user.id, accepted=False)
        got_requests = Friend.objects.filter(friend=user.id, accepted=False)
        self.extra_context["friends"] = friends
        self.extra_context["send_requests"] = sent_requests
        self.extra_context["got_requests"] = got_requests
        self.extra_context["Users"] = Account.objects.all()
        self.extra_context['page_name'] = user.username
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user: Account = request.user
        if request.POST.get("change_password_input"):
            change_password_form = ChangePasswordForm(request.POST)
            if not change_password_form.is_valid():
                messages.error(request, 'Какое то из полей заполнено неверно!')
                return HttpResponseRedirect(reverse('user-detail', kwargs={'username': user.username}))

            if not user.check_password(change_password_form.cleaned_data['old_password']):
                messages.error(request, 'Старый пароль введен неверно!')
                return HttpResponseRedirect(reverse('user-detail', kwargs={'username': user.username}))

            username = user.username
            new_password = change_password_form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            change_password_form.clean()

            login(request, authenticate(username=username, password=new_password))

        elif request.POST.get("change_avatar_input"):
            change_avatar_form = ChangeAvatarForm(request.POST, request.FILES)
            if not change_avatar_form.is_valid():
                messages.error(request,
                               "ОТ ТЕБЯ ТРЕБОВАЛОСЬ ЗАПОЛНИТЬ ОДНО ПОЛЕ И ТЫ ДАЖЕ С ЭТИМ НЕ СПРАВИЛСЯ. ВЫЙДИ НЕ ПОЗОРЬСЯ")
                return HttpResponseRedirect(reverse('user-detail', kwargs={'username': user.username}))

            user.avatar = change_avatar_form.cleaned_data['image']
            user.save()

            change_avatar_form.clean()
            return HttpResponseRedirect(reverse('user-detail', kwargs={'username': user.username}))

        change_password_form = ChangePasswordForm()
        change_avatar_form = ChangeAvatarForm()

        return render(request, 'user.html',
                      {"user": user,
                       'is_current_user': request.user == user,
                       "ChangePasswordForm": change_password_form,
                       "ChangeAvatarForm": change_avatar_form})

    def get_object(self, queryset=None):
        username = self.kwargs['username']
        return Account.objects.get(username=username)


class MemeDetailView(DetailView):
    model = Meme
    template_name = 'meme.html'
    context_object_name = 'meme'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meme = self.get_object()  # Получаем объект Meme
        meme_gallery = MemeGallery.objects.filter(meme=meme.id)
        context['page_name'] = meme.name
        context['meme_gallery'] = meme_gallery
        return context


def index(request):
    context = {
        'page_name': 'MemeTravel'
    }
    return render(request, 'index.html', context=context)


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

        return HttpResponseRedirect(f'/user/{request.user.username}', locals())
    else:
        form = LoginForm()
        return render(request, 'login.html', {'login_form': form})


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
        status = Group.objects.get(name="Пользователь")
        user = Account.objects.create_user(username, email, password)
        user.last_name = last_name
        user.first_name = first_name

        if user is None:
            return HttpResponseRedirect('/login', locals())

        user.save()
        status.user_set.add(user)
        login(request, user)

        return HttpResponseRedirect('/', locals())
    else:
        form = RegistrationForm()
        return render(request, 'registration.html', {'registration_form': form})


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
        description = form.cleaned_data.get('description')
        history = form.cleaned_data.get('history')
        meaning = form.cleaned_data.get('meaning')
        cultural_influence = form.cleaned_data.get('cultural_influence')
        using_examples = form.cleaned_data.get('using_examples')
        image = form.cleaned_data.get('path_to_img')
        additional_image = form.cleaned_data.get('additional_image')

        meme = Meme(name=name, date=date, description=description, path_to_img=image, meaning=meaning,
                    cultural_influence=cultural_influence, using_examples=using_examples, history=history)

        if meme is None:
            print("Invalid meme details: {0}, {1}, {2}, {3}".format(name, date, description, image))
            messages.error(request, 'Что то пошло не так!')
            return HttpResponseRedirect('/add_meme', locals())

        meme.save()
        if additional_image:
            MemeGallery.objects.create(meme=meme, image=additional_image)
        return HttpResponseRedirect('/encyclopedia', locals())

    else:
        form = AddMemeForm()
        return render(request, 'create/meme_test.html', {'addmeme_form': form, 'page_name': 'ДОБАВЛЕНИЕ МЕМА'})


def create_route(request, *args, **kwargs):
    route = args[0]
    if route == "friend":
        return friends_add(request)
    elif route == "account":
        return render(request, 'create/account.html')
    elif route == "meme":
        return add_meme(request)


def friends_add(request):
    if request.method == 'POST':
        user = request.user
        form = AddFriendForm(request.POST)
        if not form.is_valid():
            return JsonResponse({'error': 'Форма заполнена неверно.'}, status=400)

        name = form.cleaned_data.get('friend_name')
        if not Account.objects.filter(username=name).exists():
            return JsonResponse({'error': 'Пользователь не найден.'}, status=404)

        possible_friend = Account.objects.get(username=name)
        if Friend.objects.filter(user_id=user.id, friend_id=possible_friend.id).exists() or Friend.objects.filter(
                user_id=possible_friend.id, friend_id=user.id).exists():
            return JsonResponse({'error': 'Заявка уже существует или вы уже друзья.'}, status=409)

        friend_request = Friend(user=user, friend=possible_friend, accepted=False)
        friend_request.save()

        return JsonResponse({'message': 'Запрос в друзья отправлен!'}, status=201)
    else:
        return JsonResponse({'error': 'Неверный метод запроса.'}, status=405)


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
            return JsonResponse({'success': False, 'error': 'Мем уже в избранном!'})
    return JsonResponse({'success': False, 'error': 'ИНВАЛИД'})


def remove_from_favorites(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        current_user = request.user
        meme = Meme.objects.get(id=request.POST.get('meme_id'))

        try:
            current_user.favorites.remove(meme)
            return JsonResponse({'success': True})
        except current_user.favorites.ObjectDoesNotExist:
            return JsonResponse({'success': False, 'error': 'Мем не найден?'})
    return JsonResponse({'success': False, 'error': 'IИНВАЛИИД'})


@cache_page(60 * 15)
def encyclopedia(request):
    query = request.GET.get('q')
    memes = Meme.objects.all()

    if query:
        memes = memes.filter(name__icontains=query)

    years = {
        'до 2000': (datetime.date.min, datetime.date(2000, 1, 1)),
        '2000-2005': (datetime.date(2000, 1, 2), datetime.date(2005, 1, 1)),
        '2005-2010': (datetime.date(2005, 1, 2), datetime.date(2010, 1, 1)),
        '2010-2015': (datetime.date(2010, 1, 2), datetime.date(2015, 1, 1)),
        '2015-2020': (datetime.date(2015, 1, 2), datetime.date(2020, 1, 1)),
        'после 2020': (datetime.date(2020, 1, 2), datetime.date.max),
    }

    filtered_memes = {}

    for key, date in years.items():
        memes = Meme.objects.filter(date__range=date)
        if memes:
            filtered_memes[key] = memes

    return render(request, 'encyclopedia.html',
                  {'filtered_memes': filtered_memes, 'page_name': 'ЭНЦИКЛОПЕДИЯ'})


def autocomplete(request):
    if 'term' in request.GET:
        query = request.GET.get('term')
        memes = Meme.objects.filter(name__icontains=query)
        results = []
        for meme in memes:
            item = {
                'name': meme.name,
                'url': meme.get_absolute_url(),
                # Замените 'meme_detail' на имя вашего URL шаблона для деталей объекта
                'img': meme.path_to_img.url  # Предполагая, что 'path_to_img' - это ImageField или FileField
            }
            results.append(item)
        print(results)  # Добавьте это для отладки
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)


@cache_page(60 * 15)
def travel_view(request):
    return render(request, 'travel.html', context={'page_name': 'ПУТЕШЕСТВИЕ'})


def delete_meme(request, meme_id):
    if request.method == 'POST':
        try:
            meme = Meme.objects.get(id=meme_id)
            print(f"Удаление мема с ID: {meme_id}")
            meme.delete()
            return JsonResponse({'success': True})
        except Meme.DoesNotExist:
            print(f"Мем с ID {meme_id} не найден")
            return JsonResponse({'success': False, 'error': 'Мем не найден'})
        except Exception as e:
            print(f"Ошибка при удалении мема: {e}")
            return JsonResponse({'success': False, 'error': 'Произошла ошибка при удалении мема'})
    else:
        print("Неверный метод запроса")
        return JsonResponse({'success': False, 'error': 'Неверный метод запроса'})
