from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls .static import static

urlpatterns = [
    path("profile/<int:pk>/", views.profile, name = 'profile'),
    path("post/<int:pk>/", views.single_post, name = 'single-post'),
    path("post/add/", views.add_post, name ='add-post'),
    path("", views.home, name = "home"),
    path("search/", views.search, name = 'search'), 
    path("search/<str:data>/", views.search_data, name = 'saerch-data')
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
