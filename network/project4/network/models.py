from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    pub_user = models.ForeignKey(User, on_delete=models.CASCADE)
    Post_text = models.CharField(max_length=250)
    pub_dateTime = models.DateTimeField(auto_now_add=True)
    Post_likes = models.IntegerField(default=0)

