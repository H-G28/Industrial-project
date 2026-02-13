from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Cart, Order, Customer, Feedback, Complaint, Payment
from .forms import CustomerRegistrationForm, FeedbackForm, ComplaintForm

# ============= PUBLIC VIEWS =============

def home(request):
    """Homepage with featured products"""
    categories = Category.objects.all()
    featured_products = Product.objects.all()[:8]
    return render(request, 'store/home.html', {
        'categories': categories,
        'featured_products': featured_products
    })

def product_list(request):
    """Display all products with filtering"""
    products = Product.objects.all()
    categories = Category.objects.all()
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id
    })

def product_detail(request, pk):
    """Product detail page"""
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related_products': related_products
    })

# ============= AUTHENTICATION VIEWS =============

def register(request):
    """Customer registration"""
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Diamond Aura.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'store/register.html', {'form': form})

def user_login(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'store/login.html')

def user_logout(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

# ============= CART VIEWS =============

@login_required
def add_to_cart(request, pk):
    """Add product to cart"""
    product = get_object_or_404(Product, pk=pk)
    customer = get_object_or_404(Customer, user=request.user)
    
    cart_item, created = Cart.objects.get_or_create(
        customer=customer,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect('cart')

@login_required
def cart(request):
    """View cart"""
    customer = get_object_or_404(Customer, user=request.user)
    cart_items = Cart.objects.filter(customer=customer)
    total = sum(item.get_total() for item in cart_items)
    
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def update_cart(request, pk):
    """Update cart item quantity"""
    cart_item = get_object_or_404(Cart, pk=pk, customer__user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated!')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
    
    return redirect('cart')

@login_required
def remove_from_cart(request, pk):
    """Remove item from cart"""
    cart_item = get_object_or_404(Cart, pk=pk, customer__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')

# ============= ORDER VIEWS =============

@login_required
def checkout(request):
    """Checkout process"""
    customer = get_object_or_404(Customer, user=request.user)
    cart_items = Cart.objects.filter(customer=customer)
    
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')
    
    total = sum(item.get_total() for item in cart_items)
    
    if request.method == 'POST':
        payment_type = request.POST.get('payment_type')
        address = request.POST.get('address', customer.address)
        
        # Create orders for each cart item
        for item in cart_items:
            order = Order.objects.create(
                customer=customer,
                product=item.product,
                name=customer.name,
                address=address,
                price=item.product.price,
                quantity=item.quantity,
                status='Pending'
            )
            
            # Create payment record
            Payment.objects.create(
                order=order,
                payment_type=payment_type
            )
        
        # Clear cart
        cart_items.delete()
        
        messages.success(request, 'Order placed successfully! We will contact you soon.')
        return redirect('my_orders')
    
    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'customer': customer
    })

@login_required
def my_orders(request):
    """View customer orders"""
    customer = get_object_or_404(Customer, user=request.user)
    orders = Order.objects.filter(customer=customer)
    return render(request, 'store/my_orders.html', {'orders': orders})

# ============= FEEDBACK & COMPLAINT VIEWS =============

@login_required
def submit_feedback(request):
    """Submit feedback"""
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.customer = get_object_or_404(Customer, user=request.user)
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('home')
    else:
        form = FeedbackForm()
    return render(request, 'store/feedback.html', {'form': form})

@login_required
def submit_complaint(request):
    """Submit complaint"""
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.customer = get_object_or_404(Customer, user=request.user)
            complaint.save()
            messages.success(request, 'Your complaint has been registered.')
            return redirect('home')
    else:
        form = ComplaintForm()
    return render(request, 'store/complaint.html', {'form': form})

@login_required
def profile(request):
    """User profile"""
    customer = get_object_or_404(Customer, user=request.user)
    
    if request.method == 'POST':
        customer.name = request.POST.get('name', customer.name)
        customer.phone = request.POST.get('phone', customer.phone)
        customer.address = request.POST.get('address', customer.address)
        customer.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'store/profile.html', {'customer': customer})