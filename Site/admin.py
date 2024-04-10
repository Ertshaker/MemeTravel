from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Meme)
admin.site.register(Account)
admin.site.register(Status)
admin.site.register(Friend)
admin.site.register(UserPermission)
