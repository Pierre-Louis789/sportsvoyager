from django.contrib import admin
from .models import Pack, UnlockedPack

@admin.register(Pack)
class PackAdmin(admin.ModelAdmin):
    list_display = ('title', 'club', 'league', 'price', 'is_premium', 'created_at')
    list_filter = ('league', 'is_premium')
    search_fields = ('title', 'club', 'league')
    ordering = ('-created_at',)

@admin.register(UnlockedPack)
class UnlockedPackAdmin(admin.ModelAdmin):
    list_display = ('user', 'pack', 'unlocked_at')
    search_fields = ('user__username', 'pack__title')
    ordering = ('-unlocked_at',)
