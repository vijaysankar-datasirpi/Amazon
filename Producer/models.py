from django.db import models

class User(models.Model):
    Uname=models.CharField(max_length=50)
    Password=models.CharField(max_length=50)
    Mail=models.CharField(max_length=50)
