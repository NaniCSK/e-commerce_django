from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("category", views.category, name="category"),
    path("category/<str:category>", views.category_name, name="category_name"),
    path("add_to_watchlist/<str:id>", views.add_or_remove_to_watchlist, name="add_to_watchlist"),
    path("<str:username>/mywinnings", views.mywinnings, name="my_winnings"),
    path("watchlist/<str:username>", views.watchlist, name="watchlist"),
    path("<str:id>/close_auction", views.close_auction, name="close_auction"),
    path("<str:id>/place_bid", views.place_bid, name="place_bid"),
    path("<str:username>/mylistings", views.mylistings, name="my_listings"),
    path("<str:id>/<str:title>", views.listing_view, name="listing"),
]
