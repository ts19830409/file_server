from django.contrib import admin
from users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['login', 'email', 'files_count', 'total_size', 'created_at']
    search_fields = ['login', 'email']


