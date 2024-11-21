from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'gender', 'phone_number', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    list_filter = ('gender', 'is_active', 'is_staff', 'date_joined')
    ordering = ('-date_joined',)
    list_per_page = 25
