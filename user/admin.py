from django.contrib import admin
from .models import User, Profile, ConfirmationCode


admin.site.register(User)
admin.site.register(Profile)
admin.site.register(ConfirmationCode)
# Register your models here.
