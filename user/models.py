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

class Follow(models.Model):
    followed_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_user")
    followed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    
    def __str__(self):
        return f"{self.followed_by.username} followed {self.followed_to.username}"
    

# Create your models here.
