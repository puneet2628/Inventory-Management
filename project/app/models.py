from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

#-------------------------------- Signup and SignIn Model ---------------------------------------

class CustomUser(AbstractUser):
    # Flag to mark the single fixed root (admin) user.
    is_root_user = models.BooleanField(default=False)
    
    # For normal users, this field will store an automatically generated account ID.
    account_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    
    # Extra field for the full name (in addition to the username field).
    name = models.CharField(max_length=100, blank=True)
    
    # We use the inherited 'email' and 'password' fields from AbstractUser.
    
    def save(self, *args, **kwargs):
        # For normal users (not root), generate an account_id automatically if not set.
        if not self.is_root_user and not self.account_id:
            self.account_id = str(uuid.uuid4())[:8]  # 8-character ID
        super().save(*args, **kwargs)
    
    def __str__(self):
        # For the root user, show the email; for normal users, show the account ID.
        return self.email if self.is_root_user else self.account_id
    

#```````````````````````````````````````````Categories Model``````````````````````````````````````````````

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to='category_icons/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def product_count(self):
        return self.products.count()  # Counts products in this category

#------------------------------------------Store & Products----------------------------------------------------------
class Store(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    item_code = models.CharField(max_length=50, unique=True)  # New field
    stock = models.CharField(max_length=20, blank=True, null=True)  # New field
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stores = models.ManyToManyField(Store, related_name="products")  # New relation
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.item_code}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='product_images/')  # Supports multiple images

    def __str__(self):
        return f"Image for {self.product.name}"