from django.db import models

class Pack(models.Model):
    title = models.CharField(max_length=200)
    club = models.CharField(max_length=200)
    league = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    itinerary = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='packs/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
