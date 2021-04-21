from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

class Advisor(AbstractBaseUser):
    name = models.CharField(max_length=200)
    photo_url = models.ImageField(upload_to = 'advisor_photo')

    username = None
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []


class Booking(AbstractBaseUser):

    time = models.DateTimeField(auto_now=False, auto_now_add=False, input_formats=['%Y-%m-%dT%H:%M:%SZ',])
    user_id = models.CharField(max_length = 200)
    advisor_id = models.CharField(max_length = 200)


    username = None
    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = []

class User(AbstractBaseUser):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length = 250)

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
