from django.shortcuts import *
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from .models import *


def home(request):
    return render(request, 'index.html')

def products(request):
    return render(request, 'products/products.html')

def add_products(request):
    return render(request, 'products/add_products.html')
def add_store(request):
    return render(request, 'stores/add_store.html')

def store(request):
    return render(request, 'stores/stores.html')

def setting(request):
    return render(request, 'settings.html')

def categories(request):
    return render(request, 'categories/categories.html')

def add_categories(request):
    return render(request, 'categories/add_categories.html')



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

