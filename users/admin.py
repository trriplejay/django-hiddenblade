from django.contrib import admin

from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):

    fields = ("username","email","first_name", "last_name", "home_address", "work_address", )
    list_display = ["username", "date_joined", "last_login", "is_active"]
    list_filter = ["date_joined", "username"] 
    search_fields= ["username", "email"]
    

admin.site.register(User, UserAdmin)
