from django.shortcuts import *

def home(request):
    return render(request, 'index.html')

def products(request):
    return render(request, 'products.html')

def add_products(request):
    return render(request, 'add_products.html')

def store(request):
    return render(request, 'stores.html')

def setting(request):
    return render(request, 'settings.html')

def categories(request):
    return render(request, 'categories.html')

# Create your views here.
