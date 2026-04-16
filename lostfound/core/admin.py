from django.contrib import admin
from .models import Item, ClaimRequest, Notification

admin.site.register(Item)
admin.site.register(Notification)

@admin.register(ClaimRequest)
class ClaimRequestAdmin(admin.ModelAdmin):
    list_display = ['item', 'user', 'status']