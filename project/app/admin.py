from django.contrib import admin
from .models import CustomUser, Category, Store, Product, ProductImage
from django.contrib.auth.admin import UserAdmin

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'email', 'account_id', 'is_root_user', 'is_staff', 'is_active')
    list_filter = ('is_root_user', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'account_id', 'name', 'is_root_user')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'account_id', 'is_root_user')}
        ),
    )
    search_fields = ('email', 'account_id')
    ordering = ('email',)

# Category Admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

# Store Admin
class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location')
    search_fields = ('name', 'location')

# Product Admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'item_code', 'category', 'price', 'stock', 'created_at')
    search_fields = ('name', 'item_code')
    list_filter = ('category', 'stores', 'created_at')
    filter_horizontal = ('stores',)  # Enables multi-select for ManyToManyField

# Product Image Admin
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image')

# Registering the models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
