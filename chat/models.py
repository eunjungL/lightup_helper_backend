from django.db import models
from lightup.models import UserInfo


class Message(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, null=True)
    room = models.CharField(max_length=255)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date', )