from django.urls import path
from . import views

app_name = 'psys'

urlpatterns = [
    path('',views.index,name='index'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('MainMenu',views.MainMenu,name='main_menu'),
    path('CustomerManagementMenu',views.CustomerManagementMenu,name='customer_management_menu'),
    path('CustomerSearch',views.CustomerSearch,name='CustomerSearch')
]