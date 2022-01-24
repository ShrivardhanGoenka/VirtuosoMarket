from django.contrib import admin
from .models import PortfolioModel, CurrentPortfolio, CurrentOrders, TickerSet, PendingOrders
# Register your models here.
admin.site.register(PortfolioModel)
admin.site.register(CurrentPortfolio)
admin.site.register(CurrentOrders)
admin.site.register(TickerSet)
admin.site.register(PendingOrders)
