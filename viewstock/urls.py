from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'viewstock'

urlpatterns = [
    path('',views.home,name='home'),
    path('stockinfo/',views.stockinfo,name='stockinfo'),
    path("data.json/",views.get_data,name='get_data'),
    path("initdata.json/",views.init_get_data,name='init_get_data'),
]
