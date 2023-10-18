from django.db import models
from user.models import User, Profile
from datetime import datetime


class Post(models.Model):
    caption = models.TextField()
    post_image = models.ImageField(upload_to = "post/",blank = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null = True)
    posted_date = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}"
    
# Create your models here.
