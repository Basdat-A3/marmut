from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, "dashboard.html")

def dashboard_label(request):
    return render(request, "dashboard_label.html")