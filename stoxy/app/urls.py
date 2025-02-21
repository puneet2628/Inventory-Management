from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('categories/', categories_list, name='categories_list'),
    path('category/<int:category_id>/', category_products, name='category_products'),
    path('categories/add/', add_category, name='add_category'),
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),
    path("products/", product_list, name="product_list"),
    path("add_products/", add_product, name="add_product"),
    path("stores/", store_list, name="store_list"),
    path('add_store/', add_store, name='add_store'),
    path('store-details/<int:store_id>/', store_details, name='store_details'),
    path('settings/', settings_view, name='settings'),
    path('settings/update/', update_settings, name='update_settings'),
    path("finance/", finance_dashboard, name="finance"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
