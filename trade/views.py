from django.shortcuts import render
from portfolio.models import CurrentPortfolio, PortfolioModel
from viewstock.models import StockListModel
# Create your views here.
def home(request):
    return render(request, 'trade/trade.html')

def trade(request,name):
    query_stock = StockListModel.objects.filter(ticker = name.upper())
    if len(query_stock)==0:
        print('stock not found')
        return render(request,'trade/trade.html',{'notfound':True})
    return render(request,'trade/trade.html',{'name':name})
