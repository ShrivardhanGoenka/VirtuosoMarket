from django.shortcuts import render
from .models import StockListModel
from nsetools import Nse
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from portfolio.models import PortfolioModel, CurrentPortfolio
from django.urls import reverse
from django.contrib import messages
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
    # print('reached stock info')
    # print(request.POST)
    # query_current = CurrentPortfolio.objects.filter(username=request.user.username)
    # current = query_current.get().current
    # query_portfolio = PortfolioModel.objects.filter(username=request.user.username, type=current)
    # cash = float(query_portfolio.get().cash)
    # try:
    #     instance = StockListModel.objects.get(name=request.POST.get('stock').split('(')[0])
    #     return render(request,'viewstock/stock.html',context={'name': instance.name , 'ticker' :instance.ticker, 'cash':cash})
    # except:
    #     try:
    #         instance = StockListModel.objects.get(ticker=request.POST.get('stock').upper())
    #         return render(request,'viewstock/stock.html',context={'name': instance.name , 'ticker' :instance.ticker, 'cash':cash})
    #
    #         if 'mkt' in request.POST:
    #             print('It is a market buy request')
    #             if 'takeprofit' in request.POST:
    #                 print('It is a takeprofit request')
    #             if 'stoploss' in request.POST:
    #                 print('It is a stoploss request')
    #
    #     except Exception as e:
    #         print(e)
    #         return render(request,'viewstock/stocknotfound.html')
    return HttpResponseRedirect('/viewstock/stockinfo/NOTFOUND')

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

def buystock(request):
    print('reached buy stock')
    return stockinfo(request)

def stockredirect(request):
    try:
        instance = StockListModel.objects.get(name=request.POST.get('stock').split('(')[0])
        return HttpResponseRedirect('/viewstock/stockinfo/'+instance.ticker)
    except Exception as e:
        print(e)
        try:
            instance = StockListModel.objects.get(ticker=request.POST.get('stock').upper())
            return HttpResponseRedirect('/viewstock/stockinfo/'+instance.ticker)
        except Exception as z:
            print(z)
            return HttpResponseRedirect('/viewstock/stockinfo/NOTFOUND')

#stockinfo
def test(request,name):
    print(request.POST)
    nse = Nse()
    query_current = CurrentPortfolio.objects.filter(username=request.user.username)
    current = query_current.get().current
    query_portfolio = PortfolioModel.objects.filter(username=request.user.username, type=current)
    cash = float(query_portfolio.get().cash)
    portfolio = query_portfolio.get().detail
    stock = 0
    for n in portfolio.split(','):
        if n.split(':')[0] == name:
            stock = n.split(':')[1]
    if name == 'NOTFOUND':
        return render(request,'viewstock/stocknotfound.html')
    try:
        instance = StockListModel.objects.filter(ticker = name)
        if 'mkt' in request.POST:
            price = float(nse.get_quote(name))

            messages.success(request, 'Your order has been placed')

            print('It is a market buy request')
            if 'takeprofit' in request.POST:
                print('It is a takeprofit request')
            if 'stoploss' in request.POST:
                print('It is a stoploss request')
        elif 'lmt' in request.POST:
            print('It is a limit buy request')
            if 'takeprofit' in request.POST:
                print('It is a takeprofit request')
            if 'stoploss' in request.POST:
                print('It is a stoploss request')
        elif 'sell' in request.POST:
            print('it is a sell request')

        return render(request,'viewstock/stock.html',context={'name': instance.get().name , 'ticker' :instance.get().ticker, 'cash':cash, 'stock':stock})

    except:
        return render(request,'viewstock/stocknotfound.html')
