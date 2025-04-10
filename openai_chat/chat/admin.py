from django.contrib import admin
from .models import ClientAPIKey

@admin.register(ClientAPIKey)
class ClientAPIKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'is_active', 'created_at')
    readonly_fields = ('key', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'key')
