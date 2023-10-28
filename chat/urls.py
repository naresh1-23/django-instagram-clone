from django.urls import path
from .import views
urlpatterns = [
    path("", views.chat, name = "chat"),
    path("<int:pk>/", views.chat_room, name = "chat-room"),
    path("check/<int:pk>/", views.check_room, name = "check-room")
]
