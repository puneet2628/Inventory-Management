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

def signin(request):
    return render(request,'auth/admin_signin.html ')
   

# def admin_signin(request):
#     return render(request,'auth/admin_signin.html ')

def signup(request):
    return render(request,'auth/signup.html ')

def add_store(request):
    return render(request,"add_store.html")
# Create your views here.
