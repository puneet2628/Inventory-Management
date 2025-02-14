from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Category

class CustomUserAdmin(UserAdmin):
    # Fields to display in the user list
    list_display = ('username', 'email', 'name', 'account_id', 'is_root_user', 'is_staff', 'is_superuser')

    # Fields to search by in the admin
    search_fields = ('username', 'email', 'account_id', 'name')

    # Fields to filter by in the admin
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_root_user')

    # Fieldsets control how fields are grouped on the "change user" page
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('name', 'email', 'account_id')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_root_user', 'groups', 'user_permissions'),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count', 'icon_preview')  # Display name, product count & icon
    search_fields = ('name',)  # Enable search by category name
    list_filter = ('name',)  # Add filter options
    ordering = ('name',)  # Order categories alphabetically

    def product_count(self, obj):
        return obj.products.count()  # Show number of products in category
    product_count.short_description = 'Products Count'  # Rename column header

    def icon_preview(self, obj):
        if obj.icon:
            return f'<img src="{obj.icon.url}" width="40" height="40" style="border-radius:5px;">'
        return "No Image"
    icon_preview.allow_tags = True
    icon_preview.short_description = 'Icon Preview'