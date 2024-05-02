from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, "login.html")

def home(request):
    return render(request, "home.html")

def register(request):
    return render(request, "register.html")

def register_user(request):
    return render(request, "register_user.html")

def register_label(request):
    return render(request, "register_label.html")