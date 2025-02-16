from django.contrib import admin
from .models import CustomUser, Category, Store, StoreImage, Product, ProductImage
from django.contrib.auth.admin import UserAdmin

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    # Define the fields to display in the user list view
    list_display = (
        'id', 'email', 'account_id', 'is_root_user', 'name', 
        'phone_number', 'store', 'role', 'is_active', 'is_staff', 'is_superuser'
    )

    # Fields to search for in the admin panel
    search_fields = ('email', 'account_id', 'name', 'phone_number')

    # Filters on the right side
    list_filter = ('is_root_user', 'role', 'is_active', 'is_staff')

    # Customize the user edit form in the admin panel
    fieldsets = (
        ("User Info", {"fields": ("email", "name", "phone_number", "store", "role")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Root User", {"fields": ("is_root_user",)}),
        ("Account Details", {"fields": ("account_id", "password")}),
    )

    # Fields for the "Add User" form
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "name", "phone_number", "store", "role", "password1", "password2"),
        }),
    )

    ordering = ("email",)
    readonly_fields = ('date_joined', 'last_login')

# Category Admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

# Store Image Inline (Allows adding images within the Store admin page)
class StoreImageInline(admin.TabularInline):
    model = StoreImage
    extra = 1  # Number of empty image fields shown

# Store Admin
class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'phone_number', 'email', 'location', 'address')
    search_fields = ('name', 'location', 'category', 'phone_number', 'email')
    list_filter = ('category',)
    inlines = [StoreImageInline]  # Allow adding images in Store admin page

# Product Image Inline (Allows adding images inside the Product admin page)
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2  # Number of empty image fields shown

# Product Admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'item_code', 'category', 'price', 'stock', 'created_at')
    search_fields = ('name', 'item_code')
    list_filter = ('category', 'stores', 'created_at')
    filter_horizontal = ('stores',)  # Enables multi-select for ManyToManyField
    inlines = [ProductImageInline]  # Allow adding images in Product admin page
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
