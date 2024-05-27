from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class Meme(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()
    history = models.TextField()
    meaning = models.TextField()
    cultural_influence = models.TextField()
    using_examples = models.TextField()
    path_to_img = models.ImageField(upload_to='memes/')

    def get_absolute_url(self):
        return f'/meme/id{self.id}'


class Account(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/')
    favorites = models.ManyToManyField(Meme)

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"


class Friend(models.Model):
    class Meta:
        unique_together = ('user', 'friend')

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    friend = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='friends')
    accepted = models.BooleanField(default=False)


class MemeGallery(models.Model):
    class Meta:
        unique_together = ('meme', 'image')

    meme = models.ForeignKey(Meme, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='galery/memes/')
