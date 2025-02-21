import django
import django.http
from django.shortcuts import *
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum, F, Count
from django.shortcuts import render
from datetime import datetime, timedelta
from django.db.models.functions import TruncMonth



def home(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == "POST":
        # Get form data
        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        # Create a normal user (root user remains False)
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            name=name,
            is_root_user=False  # Normal user
        )
        # The model's save() method auto-generates an account_id for normal users.
        
        # Prepare and send an email with the account ID
        subject = "Your Account ID for Stoxy"
        message = (
            f"Hello {name},\n\n"
            f"Your Account ID is: {user.account_id}\n"
            "Please use this ID along with your password to log in."
        )
        from_email = "puneetsharma2628@gmail.com"  # Replace with your sender email
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)
        
        # Render a success page showing the account ID
        return render(request, "auth/signup_sucess.html", {"account_id": user.account_id})
    
    # For GET requests, render the signup form
    return render(request, "auth/signup.html")


def signin(request):
    if request.method == "POST":
        # Retrieve the login type and credentials from the form
        user_type = request.POST.get("userType")  # "root" or "normal"
        identifier = request.POST.get("identifier")  # Email for root, account_id for normal
        password = request.POST.get("password")
        
        user = None
        if user_type == "root":
            # For root user, the identifier is the email.
            try:
                user = CustomUser.objects.get(email=identifier, is_root_user=True)
            except CustomUser.DoesNotExist:
                user = None
        else:
            # For normal users, the identifier is the account_id.
            try:
                user = CustomUser.objects.get(account_id=identifier, is_root_user=False)
            except CustomUser.DoesNotExist:
                user = None
        
        # Authenticate: check the password.
        if user is not None and user.check_password(password):
            login(request, user)
            return redirect("home")  # Replace "home" with your actual URL name for the home page
        else:
            error = "Invalid credentials"
            return render(request, "auth/signin.html", {"error": error})
    
    # For GET requests, render the signin form
    return render(request, "auth/signin.html")


def logout_view(request):
    logout(request)
    return redirect('signin')



#--------------------------------------------------Categories---------------------------------------------------------

def categories_list(request):
    categories = Category.objects.all()
    return render(request, 'categories/categories.html', {'categories': categories})

# def category_products(request, category_id):
#     category = get_object_or_404(Category, id=category_id)
#     products = Product.objects.filter(category=category)
#     return render(request, 'categories/category_products.html', {'category': category, 'products': products})
def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)

    return render(request, 'categories/category_products.html', {'category': category, 'products': products})

    
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        icon = request.FILES.get('icon')

        if name and icon:  # Ensure required fields are present
            Category.objects.create(name=name, description=description, icon=icon)
            return redirect('categories_list')  # Redirect to category list page

    return render(request, 'categories/add_categories.html')

#------------------------------------------------Products-------=------------------------------------

# ----------------- Product List View -----------------
def product_list(request):
    products = Product.objects.all()
    return render(request, "products/products.html", {"products": products})

# ----------------- Add Product View -----------------
def add_product(request):
    categories = Category.objects.all()
    stores = Store.objects.all()
    
    if request.method == "POST":
        name = request.POST["name"]
        item_code = request.POST["item_code"]
        category_id = request.POST["category"]
        stock = request.POST["stock"]
        price = request.POST["price"]
        description = request.POST["description"]
        store_ids = request.POST.getlist("stores")
        images = request.FILES.getlist("photos")

        category = get_object_or_404(Category, id=category_id)
        product = Product.objects.create(
            category=category,
            name=name,
            item_code=item_code,
            stock=stock,
            price=price,
            description=description,
        )

        for store_id in store_ids:
            store = get_object_or_404(Store, id=store_id)
            product.stores.add(store)

        for image in images:
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            ProductImage.objects.create(product=product, image=filename)

        return redirect("product_list")

    return render(request, "products/add_products.html", {"categories": categories, "stores": stores})


#--------------------------------------------Store---------------------------------------------------------


def store_list(request):
    stores = Store.objects.all()
    return render(request, "stores/stores.html", {"stores": stores})

def add_store(request):
    if request.method == "POST":
        name = request.POST.get("name")
        category = request.POST.get("category")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        address = request.POST.get("address")
        description = request.POST.get("description")
        images = request.FILES.getlist("images")  

        if name and category and phone_number and email and address:
            store = Store.objects.create(
                name=name,
                category=category,
                phone_number=phone_number,
                email=email,
                address=address,
                description=description
            )

            for image in images:
                StoreImage.objects.create(store=store, image=image)

            return redirect("store_list")  

    return render(request, "stores/add_store.html")

def store_details(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    return render(request, 'stores/partials/store_details_partial.html', {'store': store})


#---------------------------------------settings-------------------------------------------------------

@login_required
def settings_view(request):
    return render(request, 'settings.html', {'user': request.user})

def update_settings(request):
    if request.method == "POST":
        user = request.user

       
        user.name = request.POST.get("name")  
        user.email = request.POST.get("email")
        user.phone_number = request.POST.get("phone_number")
        user.username = request.POST.get("username")

        user.save()  

        return redirect("settings") 

    return redirect("settings") 




def finance_dashboard(request):
    # 1. Category-wise Total Sales
    category_sales = (
        Product.objects.values("category__name")
        .annotate(total_sales=Sum(F("price") * F("stock")))
        .order_by("-total_sales")
    )

    # 2. Store-wise Stock Value
    store_stock_value = (
        Store.objects.annotate(
            stock_value=Sum(F("products__stock") * F("products__price"))
        )
        .values("name", "stock_value")
        .order_by("-stock_value")
    )

    # 3. Top Products by Total Stock Value
    top_products = (
        Product.objects.annotate(total_value=F("price") * F("stock"))
        .values("name", "total_value")
        .order_by("-total_value")[:5]
    )

    # 4. Dummy Data for Monthly Sales Trend (Last 12 Months)
    current_month = datetime.today().replace(day=1)
    monthly_sales = []
    for i in range(12):
        month = (current_month - timedelta(days=30 * i)).strftime("%b %Y")
        total_sales = 100000 + (i * 5000)  # Dummy sales data with an increasing trend
        monthly_sales.append({"month": month, "total_sales": total_sales})
    monthly_sales.reverse()  # To display in chronological order

    # 5. Product Category Distribution
    category_distribution = (
        Product.objects.values("category__name")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    # 6. Dummy Data for Sales Growth Rate (Month-over-Month)
    sales_growth = []
    prev_sales = 0
    for month_data in monthly_sales:
        total_sales = month_data["total_sales"]
        growth_rate = (
            ((total_sales - prev_sales) / prev_sales * 100) if prev_sales > 0 else 0
        )
        sales_growth.append({
            "month": month_data["month"],
            "growth_rate": round(growth_rate, 2)
        })
        prev_sales = total_sales

    return render(
        request,
        "finance/finance.html",
        {
            "category_sales": list(category_sales),
            "store_stock_value": list(store_stock_value),
            "top_products": list(top_products),
            "monthly_sales": monthly_sales,
            "category_distribution": list(category_distribution),
            "sales_growth": sales_growth,
        }
    )
