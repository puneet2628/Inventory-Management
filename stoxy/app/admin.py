from django.contrib import admin
from .models import CustomUser, Category, Store, StoreImage, Product, ProductImage
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = (
        'id', 'email', 'account_id', 'is_root_user', 'name', 'username',    
        'phone_number', 'store', 'role', 'is_active', 'is_staff', 'is_superuser'
    )

    search_fields = ('email', 'account_id', 'name', 'phone_number')

    list_filter = ('is_root_user', 'role', 'is_active', 'is_staff')

    fieldsets = (
        ("User Info", {"fields": ("email", "name","username", "phone_number", "store", "role")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Root User", {"fields": ("is_root_user",)}),
        ("Account Details", {"fields": ("account_id", "password")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "name", "phone_number", "store", "role", "password1", "password2"),
        }),
    )

    ordering = ("email",)
    readonly_fields = ('date_joined', 'last_login')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)


class StoreImageInline(admin.TabularInline):
    model = StoreImage
    extra = 1  

# Store Admin
class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'phone_number', 'email', 'location', 'address')
    search_fields = ('name', 'location', 'category', 'phone_number', 'email')
    list_filter = ('category',)
    inlines = [StoreImageInline]  

# Product Image Inline
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2  

# Product Admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'item_code', 'category', 'price', 'stock', 'created_at')
    search_fields = ('name', 'item_code')
    list_filter = ('category', 'stores', 'created_at')
    filter_horizontal = ('stores',) 
    inlines = [ProductImageInline] 
    readonly_fields = ('created_at',)

# Product Image Admin
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image')

# Store Image Admin
class StoreImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'store', 'image')

# Registering the models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(StoreImage, StoreImageAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
