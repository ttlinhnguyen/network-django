from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE


class User(AbstractUser):
    following = models.ManyToManyField('self', symmetrical=False, blank=True, null=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=3000, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(blank=False, default=False)

class Like(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    like_person = models.ForeignKey(User, on_delete=models.CASCADE)
    