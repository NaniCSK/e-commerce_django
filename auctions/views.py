from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Watchlist, Comment, Bid
from .forms import NewListing, CommentForm, BidForm

def index(request):
    return render(request, "auctions/index.html", {
        'listings':Listing.objects.filter(is_active=True)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords didn't match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def new_listing(request):
    if request.method == "POST":
        new_entry = NewListing(request.POST, request.FILES)
        if new_entry.is_valid():
            new_entry.instance.user = request.user
            new_entry.save()
            return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/new_listing.html",{"new_listing": NewListing()})


def listing_view(request, id, title):
    listing = Listing.objects.get(id=id)
    comments = listing.comments.all()
    new_comment = None
    if request.method == "POST":
        commentform = CommentForm(request.POST)
        if commentform.is_valid():
            new_comment = commentform.save(commit=False)
            new_comment.listing = listing
            new_comment.save()
            return HttpResponseRedirect(reverse("listing", args=(id,title)))
    if Watchlist.objects.filter(user=request.user).exists():
        instance = Watchlist.objects.get(user=request.user)
    else:
        instance = Watchlist.objects.create(user=request.user)
    user_watchlist = instance.watchlist_listing.all()
    if Bid.objects.filter(listing=listing).exists():
        bids_on_listing_list = [i.bid for i in Bid.objects.filter(listing=listing).order_by('-bid')]
        current_bid = max(bids_on_listing_list)
        hightest_bider = Bid.objects.get(listing=listing, bid=current_bid).name
    else:
        current_bid = 'No bids yet'
        hightest_bider = None
    if Bid.objects.filter(listing=listing, name=request.user.username).exists():
        current_users_bid = Bid.objects.get(listing=listing, name=request.user.username).bid
    else:
        current_users_bid = None
    return render(request, "auctions/listing_view.html", {
        "listing": listing, "comments": comments, "new_comment": new_comment, "commentform": CommentForm(),
        'user_watchlist': user_watchlist, 'current_bid': current_bid ,
        'highest_bider': hightest_bider, 'current_users_bid': current_users_bid
    })


def category(request):
    categories = [i[0] for i in Listing.category.field.choices]
    return render(request, "auctions/category.html", {
        "Categories": categories
    })


def category_name(request, category):
    listings = Listing.objects.filter(category=category, is_active=True)
    return render(request, "auctions/category_name.html", {
        "listings": listings, "category": category
    })


@login_required
def place_bid(request, id):
    listing = Listing.objects.get(id=id)
    if request.method == "POST":
        if Bid.objects.filter(listing=listing, name=request.user.username).exists():
            Bid.objects.filter(listing=listing, name=request.user.username).update(bid=request.POST['bid'])
            return HttpResponseRedirect(reverse("listing", args=(id,listing.title)))
        else:
            bidform = BidForm(request.POST)
            if bidform.is_valid():
                new_bid = bidform.save(commit=False)
                new_bid.name = request.user.username
                new_bid.listing = listing
                new_bid.save()
                return HttpResponseRedirect(reverse("listing", args=(id,listing.title)))
    return render(request, "auctions/place_bid.html", {
        "listing": listing, 'bidform': BidForm()
    })


@login_required
def watchlist (request, username):
    return render(request, "auctions/watchlist.html", {
        "listings": Watchlist.objects.get(user=request.user).watchlist_listing.all(), 'username': username
    })


@login_required
def add_or_remove_to_watchlist(request, id):
    listing = Listing.objects.get(id=id)
    if Watchlist.objects.filter(user=request.user).exists():
        instance = Watchlist.objects.get(user=request.user)
    else:
        instance = Watchlist.objects.create(user=request.user)
    user_watchlist = instance.watchlist_listing.all()
    if listing in user_watchlist:
        Watchlist.objects.get(user=request.user).watchlist_listing.remove(listing)
        Watchlist.objects.get(user=request.user).save()
        return HttpResponseRedirect(reverse("listing", args=(id,listing.title)))
    else:
        Watchlist.objects.get(user=request.user).watchlist_listing.add(listing)
        Watchlist.objects.get(user=request.user).save()
        return HttpResponseRedirect(reverse("listing", args=(id,listing.title)) )


@login_required
def mylistings(request, username):
    listings = Listing.objects.filter(user=request.user)
    return render(request, "auctions/mylistings.html", {
        "listings": listings, 'username': username,
    })


@login_required
def mywinnings(request, username):
    listings = Listing.objects.filter(winner=request.user)
    return render(request, "auctions/mywinnings.html", {
        "listings": listings, 'username': username
    })    


@login_required
def close_auction(request, id):
    listing = Listing.objects.get(id=id)
    listing.is_active = False
    if Bid.objects.filter(listing=listing).exists():
        bids_on_listing_list = [i.bid for i in Bid.objects.filter(listing=listing).order_by('-bid')]
        winner_bid = max(bids_on_listing_list)
        winner_name = Bid.objects.get(listing=listing, bid=winner_bid).name
        winner = User.objects.get(username=winner_name)
    else:
        winner = None
        winner_bid = 0
    listing.winner = winner
    listing.winner_bid = winner_bid
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(id,listing.title)))


