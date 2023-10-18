from django.contrib import admin
from .models import User, Profile, ConfirmationCode, Follow


admin.site.register(User)
admin.site.register(Profile)
admin.site.register(ConfirmationCode)
admin.site.register(Follow)
# Register your models here.
