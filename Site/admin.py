from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

# Register your models here.

admin.site.register(Friend)
admin.site.register(Account)


@admin.register(Meme)
class MemeAdmin(admin.ModelAdmin):
    fields = ['name', 'date', 'path_to_img', 'description']
    list_display = ('name', 'date', 'post_photo')

    @admin.display(description="Фотокарточка", ordering='content')
    def post_photo(self, meme: Meme):
        if meme.path_to_img:
            return mark_safe(f"<img src='{meme.path_to_img.url}' width=100>")
        return "Без фото"

#@admin.register(Account)
# class AccountAdmin(admin.ModelAdmin):
#     fields = ['username', 'email', 'last_login', 'avatar']
#     list_display = ('username', 'email', 'last_login', 'post_photo')
#
#     @admin.display(description="Фотокарточка", ordering='content')
#     def post_photo(self, account: Account):
#         if account.avatar:
#             return mark_safe(f"<img src='{account.avatar.url}' width=100>")
#         return "Без фото"

