from django.urls import path
from dashboard.views import dashboard, dashboard_label

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('label/', dashboard_label, name='dashboard_label'),
]