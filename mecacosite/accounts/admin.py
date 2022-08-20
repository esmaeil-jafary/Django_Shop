from django.contrib import admin
from .models import Profile

# baraie namayesh tamam fild haie profile dar safhe admin

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'address']
admin.site.register(Profile, ProfileAdmin)


