from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# class User(models.Model):
#     #id = models.IntegerField(unique=True,primary_key=True)
#     name = models.CharField(max_length=200)
#     password = models.CharField(max_length=200)

class Message(models.Model):
    msg=models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
class Comment(models.Model):
    MessageId = models.ForeignKey(Message,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    message=models.CharField(max_length=200)

