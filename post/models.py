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
    
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"
    
    
class Comment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    posted_date = models.DateTimeField(auto_now_add=True, blank=True)
    
    
    def __str__(self):
        return f"{self.user.username} commented on post {self.post.id}"
    
    
# Create your models here.
