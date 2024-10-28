from django.contrib import admin
from .models import User, PasswordReset


class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "first_name", "last_name", "is_active", "date_joined"]


class PasswordRestAdmin(admin.ModelAdmin):
    list_display = ["user", "token"]
    search_fields = ['email']

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(PasswordReset, PasswordRestAdmin)
