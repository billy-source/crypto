from django.contrib import admin
from .models import UserProfile, Wallet, Holding, Trade, PriceHistory

admin.site.register(UserProfile)
admin.site.register(Wallet)
admin.site.register(Holding)
admin.site.register(Trade)
admin.site.register(PriceHistory)

