from django.contrib import admin
from .models import PortfolioModel, CurrentPortfolio
# Register your models here.
admin.site.register(PortfolioModel)
admin.site.register(CurrentPortfolio)
