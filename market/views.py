from django.views.generic import TemplateView
from django.shortcuts import render

class HomePage(TemplateView):
    template_name = "index.html"

class LoggedoutPage(TemplateView):
    template_name = 'loggedout.html'

def LoggedinPage(request):
    return render(request,'loggedin.html')
