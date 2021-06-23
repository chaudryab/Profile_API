from django.db import models

# Create your models here.

#------------- Users Model Table --------------
class Users(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=200)
    profession = models.CharField(max_length=200, null=True)
    phone_no = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=100, null=True)
    image = models.ImageField(default='profile/default_pic.png',upload_to='profile/', null=True)


#------------- User Meetings Model Table --------------
class Meetings(models.Model):
    user_id = models.IntegerField()
    link = models.CharField(max_length = 200)
    

#------------- User Social Links Model Table --------------
class Social_links(models.Model):
    user_id = models.IntegerField()
    fb = models.CharField(max_length = 200)
    insta = models.CharField(max_length = 200)
    linkedin = models.CharField(max_length = 200)
    youtube = models.CharField(max_length = 200)
