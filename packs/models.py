from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone


class Pack(models.Model):
    # Basic info
    title = models.CharField(max_length=200)
    club = models.CharField(max_length=200)
    league = models.CharField(max_length=200, blank=True)

    description = models.TextField()
    teaser = models.TextField(help_text="Short preview shown when locked", blank=True)

    # Media
    image = models.ImageField(upload_to='packs/', blank=True, null=True)

    # Pricing & Premium
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    is_premium = models.BooleanField(default=True)

    # Stadium info
    stadium_name = models.CharField(max_length=200, blank=True)
    stadium_capacity = models.CharField(max_length=50, blank=True)
    stadium_location = models.CharField(max_length=200, blank=True)
    stadium_atmosphere = models.CharField(max_length=200, blank=True)
    stadium_description = models.TextField(blank=True)

    # City info
    city_best_areas = models.CharField(max_length=300, blank=True)
    city_food = models.CharField(max_length=300, blank=True)
    city_nightlife = models.CharField(max_length=300, blank=True)
    city_tips = models.TextField(blank=True)

    # Hotel info
    hotel_recommendation = models.CharField(max_length=300, blank=True)
    hotel_area = models.CharField(max_length=300, blank=True)
    hotel_area_reason = models.CharField(max_length=500, blank=True)
    hotel_notes = models.TextField(blank=True)

    # Transport info
    transport_airport = models.CharField(max_length=500, blank=True)
    transport_city = models.CharField(max_length=500, blank=True)
    transport_stadium = models.CharField(max_length=500, blank=True)
    transport_notes = models.TextField(blank=True)

    # Food & Bars
    food_local = models.CharField(max_length=300, blank=True)
    food_restaurants = models.CharField(max_length=500, blank=True)
    food_bars = models.CharField(max_length=500, blank=True)
    food_notes = models.TextField(blank=True)

    # Safety
    safety_general = models.CharField(max_length=500, blank=True)
    safety_matchday = models.CharField(max_length=500, blank=True)
    safety_areas = models.CharField(max_length=500, blank=True)
    safety_notes = models.TextField(blank=True)

    # Local Experiences
    experiences_attractions = models.CharField(max_length=500, blank=True)
    experiences_football = models.CharField(max_length=500, blank=True)
    experiences_nightlife = models.CharField(max_length=500, blank=True)
    experiences_notes = models.TextField(blank=True)

    # Budget Breakdown
    budget_flights = models.CharField(max_length=200, blank=True)
    budget_hotel = models.CharField(max_length=200, blank=True)
    budget_tickets = models.CharField(max_length=200, blank=True)
    budget_food = models.CharField(max_length=200, blank=True)
    budget_transport = models.CharField(max_length=200, blank=True)
    budget_notes = models.TextField(blank=True)

    # Match‑Day Map
    map_stadium = models.CharField(max_length=300, blank=True)
    map_transport = models.CharField(max_length=300, blank=True)
    map_pub = models.CharField(max_length=300, blank=True)
    map_hotel_area = models.CharField(max_length=300, blank=True)
    map_notes = models.TextField(blank=True)

    # Emergency Contacts
    contact_emergency = models.CharField(max_length=100, blank=True)
    contact_police = models.CharField(max_length=200, blank=True)
    contact_taxi = models.CharField(max_length=200, blank=True)
    contact_stadium = models.CharField(max_length=200, blank=True)
    contact_notes = models.TextField(blank=True)

    # Affiliate Links
    flight_link = models.URLField(blank=True)
    hotel_link = models.URLField(blank=True)
    ticket_link = models.URLField(blank=True)
    tour_link = models.URLField(blank=True)

    # Premium Content
    itinerary = models.TextField()

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def is_new(self):
        return self.created_at >= timezone.now() - timedelta(days=7)


class UnlockedPack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'pack')

    def __str__(self):
        return f"{self.user.username} unlocked {self.pack.title}"


class TimelineEntry(models.Model):
    pack = models.ForeignKey(Pack, related_name="timeline_entries", on_delete=models.CASCADE)
    time = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.time} - {self.pack.title}"


class Comment(models.Model):
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} on {self.pack.title}"
