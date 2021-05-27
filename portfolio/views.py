from django.shortcuts import render
from portfolio.models import CurrentPortfolio,PortfolioModel

# Create your views here.
def home(request):
    query_current = CurrentPortfolio.objects.filter(username=request.user.username)
    current = query_current.get().current
    query_portfolio = PortfolioModel.objects.filter(username=request.user.username, type=current)
    cash = float(query_portfolio.get().cash)
    marketvalue = float(query_portfolio.get().market)
    return render(request,'portfolio/portfolio.html', {'type':current, 'cash':cash,'market':marketvalue})
