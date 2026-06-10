from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.core.validators import MinValueValidator

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username} created on {self.created_at}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(
    default=1,
    validators=[MinValueValidator(1)]
    )
   

    def __str__(self):
        return f"CartItem: User {self.cart.user.username}, Product {self.product.name}, Quantity {self.quantity}"
    
