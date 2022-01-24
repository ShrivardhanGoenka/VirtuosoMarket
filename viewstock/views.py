from django.shortcuts import render
from .models import StockListModel
from nsetools import Nse
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from portfolio.models import PortfolioModel, CurrentPortfolio, CurrentOrders, TickerSet, PendingOrders
from django.urls import reverse
from django.contrib import messages
from datetime import datetime

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
            q = float(request.POST.get('quantity-mkt'))
            quote = nse.get_quote(name)
            flag = 0
            for i in range (1,6):
                if quote['sellQuantity' + str(i)] is None:
                    flag+=1
                if quote['buyQuantity' + str(i)] is None:
                    flag+=1
                if quote['sellPrice' + str(i)] is None:
                    flag+=1
                if quote['buyPrice' + str(i)] is None:
                    flag+=1
            if flag>=12:
                print('market is closed')
                messages.success(request,'Your order has been placed')
                description = ""
                if 'takeprofit' in request.POST:
                    description+="takeprofit:" + str(request.POST.get('price-profit')) + "\n"
                if 'stoploss' in request.POST:
                    description+="stoploss:" + str(request.POST.get('price-loss'))
                try:
                    PendingOrders.objects.create(username=request.user.username,ordertime=datetime.now(),ticker=instance.get().ticker,quantity=q,type='mkt',condition=description)
                except Exception as e:
                    print('PendingOrders')
                return render(request,'viewstock/stock.html',context={'name': instance.get().name , 'ticker' :instance.get().ticker, 'cash':cash, 'stock':stock})
            price = float(quote['lastPrice'])


            if price*q > cash:
                messages.error(request, 'An error occurred. Please try again!')
                return render(request,'viewstock/stock.html',context={'name': instance.get().name , 'ticker' :instance.get().ticker, 'cash':cash, 'stock':stock})

            n = instance.get().ticker
            str1 = ""
            p = portfolio.split(',')
            flag=0
            for item in p:
                i = item.split(':')
                if i[0] == n:
                    flag = 1
                    str1+= n +':' + str(int(int(i[1])+q)) + ','
                    stock = str(int(int(i[1])+q))
                else:
                    str1+=item + ','
            if flag == 0:
                str1 += n+':'+str(int(q))+','
                stock = str(int(q))
            str1 = str1[:-1]
            print(str1)
            tleft = cash - price*q
            query_portfolio.update(cash=str(tleft),detail=str1)
            cash = tleft
            messages.success(request, 'The stocks have been bought')
            if 'takeprofit' in request.POST:
                PendingOrders.objects.create(username=request.user.username,ordertime=datetime.now(),ticker=instance.get().ticker,quantity=q,amount=request.POST.get('price-profit'),type='sell')
                messages.success(request,'Your take profit order has been placed.')
            if 'stoploss' in request.POST:
                PendingOrders.objects.create(username=request.user.username,ordertime=datetime.now(),ticker=instance.get().ticker,quantity=q,amount=request.POST.get('price-loss'),type='sell')
                messages.success(request,'Your stop loss order has been placed.')
        elif 'lmt' in request.POST:
            description = ""
            q = float(request.POST.get('quantity'))
            price = float(request.POST.get('order-price'))
            if 'takeprofit' in request.POST:
                description+="takeprofit:" + str(request.POST.get('price-profit')) + "\n"
            if 'stoploss' in request.POST:
                description+="stoploss:" + str(request.POST.get('price-loss'))
            PendingOrders.objects.create(username=request.user.username,ordertime=datetime.now(),ticker=instance.get().ticker,amount=price,quantity=q,type='lmt',condition=description)
        elif 'sell' in request.POST:
            print('in sell')
            quote = nse.get_quote(name)
            flag = 0
            for i in range (1,6):
                if quote['sellQuantity' + str(i)] is None:
                    flag+=1
                if quote['buyQuantity' + str(i)] is None:
                    flag+=1
                if quote['sellPrice' + str(i)] is None:
                    flag+=1
                if quote['buyPrice' + str(i)] is None:
                    flag+=1
            q = float(request.POST.get('quantity'))
            print('in sell 1')
            if flag>=12:
                messages.success(request,'Your order has been placed')
                PendingOrders.objects.create(username=request.user.username,ordertime=datetime.now(),ticker=instance.get().ticker,quantity=q,type='sell')
                return render(request,'viewstock/stock.html',context={'name': instance.get().name , 'ticker' :instance.get().ticker, 'cash':cash, 'stock':stock})
            q = float(request.POST.get('quantity'))
            print('in sell 2')
            p = portfolio.split(',')
            flag=0
            str1 = ""
            for item in p:
                i= item.split(':')
                if i[0] == instance.get().ticker:
                    if int(i[1]) >= q:
                        flag=1
                        stock = int(int(i[1]) - q)
                        if int(i[1]) - q == 0:
                            pass
                        else:
                            str1+=i[0]+':'+str(int(int(i[1])-q))+','
                    else:
                        messages.error('You do not have enough stock to sell. Please try again')
                        return render(request,'viewstock/stock.html',context={'name': instance.get().name , 'ticker' :instance.get().ticker, 'cash':cash, 'stock':stock})
                else:
                    str1+=item + ','
            str1 = str1[:-1]
            price = float(quote['lastPrice'])
            tleft = cash + price*q
            print(str1)
            cash = tleft
            query_portfolio.update(cash=str(tleft),detail=str1)
            messages.success(request,'The stock has been sold')

        return render(request,'viewstock/stock.html',context={'name': instance.get().name , 'ticker' :instance.get().ticker, 'cash':cash, 'stock':stock})

    except Exception as e:
        print(e)
        return render(request,'viewstock/stocknotfound.html')
