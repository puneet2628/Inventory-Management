from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

#-------------------------------- Signup and SignIn Model ---------------------------------------
class CustomUser(AbstractUser):
    # Root user flag (Fixed super admin user)
    is_root_user = models.BooleanField(default=False)

    # Unique account ID (only for normal users, auto-generated)
    account_id = models.CharField(max_length=20, unique=True, null=True, blank=True)

    # Ensure email is unique
    email = models.EmailField(unique=True)  # FIXED

    # User details
    name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    store = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)

    USERNAME_FIELD = 'email'  # Login using email
    REQUIRED_FIELDS = ['username']  # Keep username for Django compatibility

    def save(self, *args, **kwargs):
        """ Auto-generate an 8-character account ID for normal users. """
        if not self.is_root_user and not self.account_id:
            while True:
                new_account_id = str(uuid.uuid4())[:8]  # Generate unique 8-char ID
                if not CustomUser.objects.filter(account_id=new_account_id).exists():
                    self.account_id = new_account_id
                    break
        super().save(*args, **kwargs)

    def __str__(self):
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
    category = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class StoreImage(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="store_images/")


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    item_code = models.CharField(max_length=50, unique=True)  # New field
    stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stores = models.ManyToManyField(Store, related_name="products")  # New relation
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.item_code}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='product_images/')  # Store in 'media/product_images/'
    
    def __str__(self):
        return f"Image for {self.product.name}"