from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

CATEGORY = [
    ("Toys", "Toys"),
    ("Electronics", "Electronics"),
    ("Books", "Books"),
    ("Furniture", "Furniture"),
    ("Other", "Other"),
]


class User(AbstractUser):
    pass


class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", default=1)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    starting_bid = models.IntegerField()
    category = models.CharField(max_length=64, choices=CATEGORY, default="Other")
    image = models.ImageField(upload_to="auctions/images/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="won_listings", blank=True, null=True)
    winner_bid = models.IntegerField(blank=True, null=True)


class Bid(models.Model):
    name = models.CharField(max_length=64)
    bid = models.IntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    class Meta:
        ordering = ['bid']

    def __str__(self):
        return f'{self.name} - ${self.bid} on {self.listing.title}'


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=64)
    comment = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.name} \n {self.comment}'


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    watchlist_listing = models.ManyToManyField(Listing)

    def __str__(self):
        return f"{self.user}'s watchlist"