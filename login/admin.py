from django.contrib import admin
from login.models import Login

class LoginAdmin(admin.ModelAdmin):
    list_display = ( 'user_name', 'password')


admin.site.register(Login,LoginAdmin)

