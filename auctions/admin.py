from django.contrib import admin
from .models import Listing, Comment, Bid, Watchlist

# Register your models here.
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Watchlist)

# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('name', 'comment', 'created_at', 'active')
#     list_filter = ('active', 'created_at')
#     search_fields = ('name', 'comment')
#     actions = ['approve_comments']

#     def approve_comments(self, request, queryset):
#         queryset.update(active=True)