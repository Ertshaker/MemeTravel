from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Meme(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateField()
    date_peek = models.DateField()
    popularity = models.IntegerField()
    description = models.TextField()
    path_to_img = models.ImageField(upload_to='memes/')

    def get_absolute_url(self):
        return f'/memes/id{self.id}'


class Account(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/')
    favorites = models.ManyToManyField(Meme)

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"


class Friend(models.Model):
    class Meta:
        unique_together = (('user_id', 'friend_id'))

    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    friend_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='friends')
    accepted = models.BooleanField(default=False)

class MemeGallery(models.Model):
    class Meta:
        unique_together = (('meme_id', 'image'))
    meme_id = models.ForeignKey(Meme, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='galery/memes/')

