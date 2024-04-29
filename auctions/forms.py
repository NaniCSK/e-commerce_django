from .models import Listing, Comment, Bid
from django import forms


class NewListing(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ('created_at', 'user', 'is_active', 'winner', 'winner_bid')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'comment')


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('bid',)
        labels = {'bid': 'Bid(in $)'}

