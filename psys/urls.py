from django.urls import path
from . import views

app_name = 'psys'

urlpatterns = [
    path('CustomerSearch',views.CustomerSearch,name='CustomerSearch')
]