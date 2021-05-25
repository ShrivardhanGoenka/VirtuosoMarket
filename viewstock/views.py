from django.shortcuts import render
from .models import StockListModel
from nsetools import Nse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def home(request):
    if 'term' in request.GET:
        qs = StockListModel.objects.filter(name__icontains=request.GET.get('term'))
        titles = list()
        for product in qs:
            titles.append(product.name + "(" + product.ticker + ")")

        if(len(titles) < 20):
            qs = StockListModel.objects.filter(ticker__icontains=request.GET.get('term'))
            for product in qs:
                titles.append(product.name  + "(" + product.ticker + ")")

        titles = list(set(titles))
        return JsonResponse(titles[:20], safe=False)
    return render(request,'viewstock/searchbar.html')

def stockinfo(request):
    try:
        instance = StockListModel.objects.get(name=request.POST.get('stock').split('(')[0])
        return render(request,'viewstock/stock.html',context={'name': instance.name , 'ticker' :instance.ticker})
    except:
        try:
            instance = StockListModel.objects.get(ticker=request.POST.get('stock').upper())
            return render(request,'viewstock/stock.html',context={'name': instance.name , 'ticker' :instance.ticker})

        except:
            return render(request,'viewstock/stocknotfound.html')

def get_data(request):
    nse=Nse()
    a = nse.get_quote(eval(request.GET.get('data'))['stock'])
    dict = {
        'current': a['lastPrice'],
        'pchange': abs(float(a['pChange'])),
        'change' : a['change']
    }
    return JsonResponse(dict)

def init_get_data(request):
    nse=Nse()
    a = nse.get_quote(eval(request.GET.get('data'))['stock'])
    dict = {
        'current': a['lastPrice'],
        'pchange': abs(float(a['pChange'])),
        'previousclose' : a['previousClose'],
        'open' : a['open'],
        'change' : a['change'],
        'closeprice' : a['closePrice'],
        'dayhigh' : a['dayHigh'],
        'daylow' : a['dayLow'],
        'high52' : a['high52'],
        'low52' : a['low52']
    }
    return JsonResponse(dict)
