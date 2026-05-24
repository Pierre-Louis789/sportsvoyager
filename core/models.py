from django.db import models
from django.contrib.auth.models import User

class Pack(models.Model):
    title = models.CharField(max_length=200)
    club = models.CharField(max_length=200)
    league = models.CharField(max_length=200, blank=True)
    description = models.TextField()

    # Premium content
    itinerary = models.TextField() 
    teaser = models.TextField(help_text="Short preview shown when locked")

    # Pricing
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    is_premium = models.BooleanField(default=True)

    # Media
    image = models.ImageField(upload_to='packs/', blank=True)

    # Affiliate Links
    flight_link = models.URLField(blank=True)
    hotel_link = models.URLField(blank=True)
    ticket_link = models.URLField(blank=True)
    tour_link = models.URLField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UnlockedPack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'pack')

    def __str__(self):
        return f"{self.user.username} unlocked {self.pack.title}"
