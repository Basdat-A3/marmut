from django.shortcuts import render
from utils.query import *

def chart_list(request):
    connection, cursor = get_database_cursor()
    
    # close connection
    cursor.close()
    connection.close()

    
    return render(request, 'chart_list.html')

def chart_detail(request):
    connection, cursor = get_database_cursor()


    # close connection
    cursor.close()
    connection.close()


    return render(request, 'chart_detail.html')
