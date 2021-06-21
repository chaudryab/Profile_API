from django.db import models


# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=200)
    profession = models.CharField(max_length=200)
    phone_no = models.CharField(max_length=30, unique=True)
    image = models.ImageField(upload_to='profile/', blank=True)
    # created_at = models.DateTimeField()
    # updated_at = models.DateTimeField()

class Meetings(models.Model):
    # user_sigin = models.OneToOneField("Users",on_delete=models.CASCADE)
    user_id = models.IntegerField()
    link = models.CharField(max_length = 200)
    # created_at = models.DateTimeField()
    # updated_at = models.DateTimeField()

class Social_links(models.Model):
    user_id = models.IntegerField()
    fb = models.CharField(max_length = 200)
    insta = models.CharField(max_length = 200)
    linkedin = models.CharField(max_length = 200)
    youtube = models.CharField(max_length = 200)
    # created_at = models.DateTimeField()
    # updated_at = models.DateTimeField()