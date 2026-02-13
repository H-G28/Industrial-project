from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Sum
from .models import Product, Category, Order, Customer, Feedback, Complaint, ProductImage, Admin
from .forms import ProductForm, CategoryForm, ProductImageForm

def is_admin(user):
    """Check if user is admin"""
    try:
        return Admin.objects.filter(user=user).exists()
    except:
        return False

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard with statistics"""
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='Pending').count()
    total_customers = Customer.objects.count()
    total_revenue = Order.objects.filter(status='Delivered').aggregate(
        total=Sum('price')
    )['total'] or 0
    
    recent_orders = Order.objects.all()[:5]
    recent_feedbacks = Feedback.objects.all()[:5]
    recent_complaints = Complaint.objects.all()[:5]
    
    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_customers': total_customers,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'recent_feedbacks': recent_feedbacks,
        'recent_complaints': recent_complaints,
    }
    return render(request, 'admin_panel/dashboard.html', context)

# ============= CATEGORY MANAGEMENT =============

@login_required
@user_passes_test(is_admin)
def manage_categories(request):
    """List all categories"""
    categories = Category.objects.all()
    return render(request, 'admin_panel/categories.html', {'categories': categories})

@login_required
@user_passes_test(is_admin)
def add_category(request):
    """Add new category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('manage_categories')
    else:
        form = CategoryForm()
    return render(request, 'admin_panel/add_category.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_category(request, pk):
    """Edit category"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('manage_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'admin_panel/edit_category.html', {'form': form, 'category': category})

@login_required
@user_passes_test(is_admin)
def delete_category(request, pk):
    """Delete category"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('manage_categories')
    return render(request, 'admin_panel/delete_category.html', {'category': category})

# ============= PRODUCT MANAGEMENT =============

@login_required
@user_passes_test(is_admin)
def manage_products(request):
    """List all products"""
    products = Product.objects.all().select_related('category')
    return render(request, 'admin_panel/products.html', {'products': products})

@login_required
@user_passes_test(is_admin)
def add_product(request):
    """Add new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        images = request.FILES.getlist('images')
        
        if form.is_valid():
            product = form.save()
            
            # Save product images
            for image in images:
                ProductImage.objects.create(product=product, image_path=image)
            
            messages.success(request, 'Product added successfully!')
            return redirect('manage_products')
    else:
        form = ProductForm()
    return render(request, 'admin_panel/add_product.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_product(request, pk):
    """Edit product"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        images = request.FILES.getlist('images')
        
        if form.is_valid():
            form.save()
            
            # Add new images
            for image in images:
                ProductImage.objects.create(product=product, image_path=image)
            
            messages.success(request, 'Product updated successfully!')
            return redirect('manage_products')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'admin_panel/edit_product.html', {
        'form': form,
        'product': product
    })

@login_required
@user_passes_test(is_admin)
def delete_product(request, pk):
    """Delete product"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('manage_products')
    return render(request, 'admin_panel/delete_product.html', {'product': product})

@login_required
@user_passes_test(is_admin)
def delete_product_image(request, pk):
    """Delete product image"""
    image = get_object_or_404(ProductImage, pk=pk)
    product_id = image.product.id
    image.delete()
    messages.success(request, 'Image deleted successfully!')
    return redirect('edit_product', pk=product_id)

# ============= ORDER MANAGEMENT =============

@login_required
@user_passes_test(is_admin)
def manage_orders(request):
    """List all orders"""
    orders = Order.objects.all().select_related('customer', 'product')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
    
    return render(request, 'admin_panel/orders.html', {'orders': orders})

@login_required
@user_passes_test(is_admin)
def update_order_status(request, pk):
    """Update order status"""
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        messages.success(request, f'Order #{order.id} status updated to {new_status}!')
        return redirect('manage_orders')
    
    return render(request, 'admin_panel/update_order.html', {'order': order})

# ============= USER MANAGEMENT =============

@login_required
@user_passes_test(is_admin)
def manage_users(request):
    """List all customers"""
    customers = Customer.objects.all().select_related('user')
    return render(request, 'admin_panel/users.html', {'customers': customers})

# ============= FEEDBACK & COMPLAINTS =============

@login_required
@user_passes_test(is_admin)
def manage_feedback(request):
    """View all feedback"""
    feedbacks = Feedback.objects.all().select_related('customer')
    return render(request, 'admin_panel/feedback.html', {'feedbacks': feedbacks})

@login_required
@user_passes_test(is_admin)
def manage_complaints(request):
    """View all complaints"""
    complaints = Complaint.objects.all().select_related('customer', 'product')
    return render(request, 'admin_panel/complaints.html', {'complaints': complaints})

# ============= REPORTS =============

@login_required
@user_passes_test(is_admin)
def reports(request):
    """Generate reports"""
    # Sales by category
    category_sales = Order.objects.filter(status='Delivered').values(
        'product__category__name'
    ).annotate(
        total_sales=Sum('price'),
        total_orders=Count('id')
    )
    
    # Monthly revenue
    from django.db.models.functions import TruncMonth
    monthly_revenue = Order.objects.filter(status='Delivered').annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        revenue=Sum('price')
    ).order_by('month')
    
    context = {
        'category_sales': category_sales,
        'monthly_revenue': monthly_revenue,
    }
    return render(request, 'admin_panel/reports.html', context)