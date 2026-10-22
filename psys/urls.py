from django.urls import path
from . import views

app_name = 'psys'

urlpatterns = [
    path('CustomerSerch',views.CustomerSearch,name='CustomerSearch')
]