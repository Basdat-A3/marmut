from django.urls import path
from . import views
from melihat_chart.views import chart_list, chart_detail

app_name = 'melihat_chart'

urlpatterns = [
    path('chart-list/', chart_list, name='list_chart'),
    path('chart-detail/<uuid:id_chart>/', chart_detail, name='detail_chart'),
]

