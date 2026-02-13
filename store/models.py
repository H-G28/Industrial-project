from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=35)
    number = models.CharField(max_length=10)
    address = models.CharField(max_length=50)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table = 'admin'

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=20)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'customer'

class Category(models.Model):
    name = models.CharField(max_length=35, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'category'
        verbose_name_plural = 'Categories'

class Product(models.Model):
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=50)
    price = models.FloatField(validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    carat = models.IntegerField(validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'product'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_path = models.ImageField(upload_to='products/')
    
    def __str__(self):
        return f"Image for {self.product.name}"
    
    class Meta:
        db_table = 'image'

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    
    def get_total(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.customer.name}'s cart - {self.product.name}"
    
    class Meta:
        db_table = 'cart'

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Delivered', 'Delivered'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=35)
    address = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=50, blank=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    def get_total(self):
        return self.price * self.quantity
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"
    
    class Meta:
        db_table = 'order'
        ordering = ['-date']

class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('Card', 'Credit/Debit Card'),
        ('UPI', 'UPI'),
        ('NetBanking', 'Net Banking'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=30, choices=PAYMENT_TYPE_CHOICES)
    payment_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment for Order #{self.order.id}"
    
    class Meta:
        db_table = 'payment'

class Feedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback from {self.customer.name}"
    
    class Meta:
        db_table = 'feedback'
        ordering = ['-date']

class Complaint(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Complaint from {self.customer.name}"
    
    class Meta:
        db_table = 'complaints'
        ordering = ['-date']