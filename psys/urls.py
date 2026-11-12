from django.urls import path
from . import views

app_name = 'psys'

urlpatterns = [
    path('',views.index,name='index'),
    path('login',views.login,name='login'),
    path('MainMenu',views.MainMenu,name='main_menu'),
    path('CustomerSearch',views.CustomerSearch,name='CustomerSearch')
]