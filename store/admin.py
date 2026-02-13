from django.contrib import admin
from .models import Admin, Customer, Category, Product, ProductImage, Cart, Order, Payment, Feedback, Complaint

@admin.register(Admin)
class AdminModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'number']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']
    search_fields = ['name', 'email']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'carat', 'created_at']
    list_filter = ['category']
    search_fields = ['name']
    inlines = [ProductImageInline]

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['customer', 'product', 'quantity', 'get_total']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'product', 'quantity', 'price', 'status', 'date']
    list_filter = ['status', 'date']
    search_fields = ['customer__name']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'payment_type', 'payment_date']
    list_filter = ['payment_type']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['customer', 'description', 'date']
    list_filter = ['date']

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['customer', 'product', 'description', 'date']
    list_filter = ['date']