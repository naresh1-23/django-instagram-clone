from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.login, name = 'login'),
    path("accounts/emailsignup/", views.signup, name = 'signup'),
    path("accounts/emailsignup/confirmation_code/", views.confirmation_code, name = 'confirmation-code'),
    path("logout/", views.logout_user, name = 'logout'),
    path("follow/<int:pk>/", views.follow, name = 'follow')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
