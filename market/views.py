from django.views.generic import TemplateView
from django.shortcuts import render
from portfolio.models import PortfolioModel,CurrentPortfolio

class HomePage(TemplateView):
    template_name = "index.html"

class LoggedoutPage(TemplateView):
    template_name = 'loggedout.html'

def LoggedinPage(request):
    a = PortfolioModel.objects.filter(username = request.user.username)
    if len(a)==0:
        PortfolioModel.objects.create(username = request.user.username, cash = '100000', market= '0', type='PERSONAL')
        CurrentPortfolio.objects.create(username = request.user.username, current = "PERSONAL")
    return render(request,'loggedin.html')
