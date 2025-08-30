from django.contrib import admin
from .models import UserProfile, Holding, Trade, PriceHistory

admin.site.register(UserProfile)
admin.site.register(Holding)
admin.site.register(Trade)
admin.site.register(PriceHistory)