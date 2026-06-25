from django.contrib import admin
from .models import Pack, UnlockedPack, TimelineEntry, Comment


class TimelineEntryInline(admin.TabularInline):
    model = TimelineEntry
    extra = 1
    classes = ["collapse"]


@admin.register(Pack)
class PackAdmin(admin.ModelAdmin):
    list_display = ("title", "club", "league", "price", "is_premium", "created_at", "preview_image")
    list_filter = ("league", "is_premium")
    search_fields = ("title", "club", "league")
    fields = ("title", "club", "league", "price", "is_premium", "image_name")
    ordering = ("-created_at",)
    inlines = [TimelineEntryInline]

    readonly_fields = ("preview_image",)

    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "club", "league", "image_name", "preview_image", "description", "teaser")
        }),

        ("Stadium Information", {
            "fields": (
                "stadium_name",
                "stadium_capacity",
                "stadium_location",
                "stadium_atmosphere",
                "stadium_description",
            ),
            "classes": ("collapse",)
        }),

        ("City Travel Tips", {
            "fields": (
                "city_best_areas",
                "city_food",
                "city_nightlife",
                "city_tips",
            ),
            "classes": ("collapse",)
        }),

        ("Hotel & Area Recommendations", {
            "fields": (
                "hotel_recommendation",
                "hotel_area",
                "hotel_area_reason",
                "hotel_notes",
            ),
            "classes": ("collapse",)
        }),

        ("Transport Guide", {
            "fields": (
                "transport_airport",
                "transport_city",
                "transport_stadium",
                "transport_notes",
            ),
            "classes": ("collapse",)
        }),

        ("Food & Bars Recommendations", {
            "fields": (
                "food_local",
                "food_restaurants",
                "food_bars",
                "food_notes",
            ),
            "classes": ("collapse",)
        }),

        ("Safety Tips", {
            "fields": (
                "safety_general",
                "safety_matchday",
                "safety_areas",
                "safety_notes",
            ),
            "classes": ("collapse",)
        }),

        ("Local Experiences", {
            "fields": (
                "experiences_attractions",
                "experiences_football",
                "experiences_nightlife",
                "experiences_notes",
            ),
            "classes": ("collapse",)
        }),

        ("Budget Breakdown", {
            "fields": (
                "budget_flights",
                "budget_hotel",
                "budget_tickets",
                "budget_food",
                "budget_transport",
                "budget_notes",
            ),
            "classes": ("collapse",)
        }),

        ("Match‑Day Map (Static)", {
            "fields": (
                "map_stadium",
                "map_transport",
                "map_pub",
                "map_hotel_area",
                "map_notes",
            ),
            "classes": ("collapse",)
        }),

        ("Emergency & Useful Contacts", {
            "fields": (
                "contact_emergency",
                "contact_police",
                "contact_taxi",
                "contact_stadium",
                "contact_notes",
            ),
            "classes": ("collapse",)
        }),

        ("Itinerary", {
            "fields": ("itinerary",),
            "classes": ("collapse",)
        }),

        ("Affiliate Booking Links", {
            "fields": (
                "flight_link",
                "hotel_link",
                "ticket_link",
                "tour_link",
            ),
            "classes": ("collapse",)
        }),

        ("Pricing & Premium Settings", {
            "fields": ("price", "is_premium"),
        }),
    )

    def preview_image(self, obj):
        if obj.image_name:
            return f'<img src="/static/packs/{obj.image_name}" style="max-height:150px;border-radius:6px;" />'
        return "No image uploaded"

    preview_image.allow_tags = True
    preview_image.short_description = "Image Preview"


@admin.register(UnlockedPack)
class UnlockedPackAdmin(admin.ModelAdmin):
    list_display = ("user", "pack", "unlocked_at")
    search_fields = ("user__username", "pack__title")
    ordering = ("-unlocked_at",)


@admin.register(TimelineEntry)
class TimelineEntryAdmin(admin.ModelAdmin):
    list_display = ("pack", "time", "description")
    search_fields = ("pack__title", "time", "description")
    ordering = ("pack", "time")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("pack", "user", "created_at")
    search_fields = ("pack__title", "user__username", "text")
    ordering = ("-created_at",)
