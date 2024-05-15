from django.shortcuts import render
from utils.query import *

def chart_list(request):
    return render(request, 'chart_list.html')

def chart_detail(request):
    return render(request, 'chart_detail.html')
