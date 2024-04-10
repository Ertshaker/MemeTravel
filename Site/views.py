from django.shortcuts import render
from django.http import HttpResponse

from Site.models import *


# Create your views here.

def index(request):
    return render(request, 'inxex.html')
def encyclopedia(request):
    memes = Meme.objects.all()
    return render(request, 'encyclopedia.html', {"memes": memes})
def authorization(request):
    if request.method == 'POST':
        User = Account()
        User.name = request.POST.get('name')
        User.password = request.POST.get('password')
    return render(request, 'authorization.html')