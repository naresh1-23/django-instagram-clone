from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    fullname = models.CharField(max_length=150)
    is_verified = models.BooleanField(default = False)
    
    def __str__(self):
        return self.username
    
    
class Profile(models.Model):
    profile_img = models.ImageField(upload_to = "user/", default = "user/default.jpg")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

    
class ConfirmationCode(models.Model):
    code = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

# Create your models here.
