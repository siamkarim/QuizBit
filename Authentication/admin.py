from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'gender', 'phone_number')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('gender', 'is_active', 'is_staff')
