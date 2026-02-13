from django.urls import path
from . import views, admin_views

urlpatterns = [
    # Public URLs
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Cart
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:pk>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Orders
    path('checkout/', views.checkout, name='checkout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    
    # Feedback & Complaints
    path('feedback/', views.submit_feedback, name='submit_feedback'),
    path('complaint/', views.submit_complaint, name='submit_complaint'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
    
    # ============= ADMIN PANEL URLs =============
    path('admin-panel/', admin_views.admin_dashboard, name='admin_dashboard'),
    
    # Category Management
    path('admin-panel/categories/', admin_views.manage_categories, name='manage_categories'),
    path('admin-panel/categories/add/', admin_views.add_category, name='add_category'),
    path('admin-panel/categories/edit/<int:pk>/', admin_views.edit_category, name='edit_category'),
    path('admin-panel/categories/delete/<int:pk>/', admin_views.delete_category, name='delete_category'),
    
    # Product Management
    path('admin-panel/products/', admin_views.manage_products, name='manage_products'),
    path('admin-panel/products/add/', admin_views.add_product, name='add_product'),
    path('admin-panel/products/edit/<int:pk>/', admin_views.edit_product, name='edit_product'),
    path('admin-panel/products/delete/<int:pk>/', admin_views.delete_product, name='delete_product'),
    path('admin-panel/products/delete-image/<int:pk>/', admin_views.delete_product_image, name='delete_product_image'),
    
    # Order Management
    path('admin-panel/orders/', admin_views.manage_orders, name='manage_orders'),
    path('admin-panel/orders/update/<int:pk>/', admin_views.update_order_status, name='update_order_status'),
    
    # User Management
    path('admin-panel/users/', admin_views.manage_users, name='manage_users'),
    
    # Feedback & Complaints
    path('admin-panel/feedback/', admin_views.manage_feedback, name='manage_feedback'),
    path('admin-panel/complaints/', admin_views.manage_complaints, name='manage_complaints'),
    
    # Reports
    path('admin-panel/reports/', admin_views.reports, name='reports'),
]