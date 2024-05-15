from django.urls import path
from authentication.views import login, home, register, register_label, register_user
from authentication.views import logout

app_name = 'authentication'

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('register/label', register_label, name='register_label'),
    path('register/user', register_user, name='register_user'),
]