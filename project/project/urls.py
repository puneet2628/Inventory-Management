"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# from flask import views
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name= 'home'),
    # path('products/', products),
    # path('add_products/', add_products),
    path('addstore/', add_store),
    path('stores/', store),
    path('settings/', setting),
    path('categories/', categories_list, name='categories_list'),
    path('category/<int:category_id>/', category_products, name='category_products'),
    path('categories/add/', add_category, name='add_category'),
    path('signin/',signin,name='signin'  ),
    path('signup/', signup,name='signup' ),
    path('logout/', logout_view,name='logout' ),
    path("products/", product_list, name="product_list"),
    path("add_products/", add_product, name="add_product"),
   
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)