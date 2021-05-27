from django.urls import path, include
from . import views

app_name = 'trade'

urlpatterns = [
    path('', views.home, name="trade"),
    path('<str:name>',views.trade,name='trade')
]
