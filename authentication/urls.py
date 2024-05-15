from django.urls import path
from authentication.views import login, home, register, register_label, register_user, logout_user

app_name = 'authentication'

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register, name='register'),
    path('register/label', register_label, name='register_label'),
    path('register/user', register_user, name='register_user'),
]
