from django.shortcuts import render
from django.http import HttpResponse

def CustomerSearch(request):
    return render(request,"psys/CustomerSearch.html")