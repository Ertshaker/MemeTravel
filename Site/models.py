from django.db import models

# Create your models here.

class Meme(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateField()
    date_peek = models.DateField()
    popularity = models.IntegerField()
    path_to_img = models.ImageField(upload_to='memes/')
    description = models.TextField()


class Account(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    login = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/')
    email = models.CharField(max_length=100)
    favorites = models.ManyToManyField(Meme)


class Status(models.Model):
    id = models.AutoField(primary_key=True, default=1)
    name = models.CharField(max_length=100)


class Friend(models.Model):
    class Meta:
        unique_together = (('user_id', 'friend_id'),)

    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    friend_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='friends')
    link = models.BooleanField(default=False)


class UserPermission(models.Model):
    id = models.AutoField(primary_key=True, default=1)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING)
