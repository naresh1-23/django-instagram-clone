from django.db import models
from user.models import User

class Room(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1_obj")
    user2 = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "user2_obj")
    
    def __str__(self):
        return f"room of {self.user1.username} and {self.user2.username}"
    
    
class Chat(models.Model):
    message = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    msg_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="msg_from", null = True)
    msg_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="msg_to", null= True)
    def __str__(self):
        return f"message from {self.msg_from.username} to {self.msg_to.username}"
    
    