from django.contrib import admin
from .models import Pack

class PackAdmin(admin.ModelAdmin):
    list_display = ('title', 'club', 'league', 'price', 'created_at')
    search_fields = ('title', 'club', 'league')
    list_filter = ('league',)
    fields = (
        'title', 'club', 'league', 'description', 'itinerary', 'price', 'image',
        'flight_link', 'hotel_link', 'ticket_link', 'tour_link'
    )

admin.site.register(Pack, PackAdmin)
