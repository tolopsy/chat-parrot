from django.contrib import admin
from .models import User, Jwt

admin.site.register((User, Jwt))
