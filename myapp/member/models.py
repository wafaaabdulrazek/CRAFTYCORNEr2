from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    Clotheschoices = [
        ('Accessories', 'Accessories'),
        ('Men Clothes', 'Men Clothes'),
        ('Women Clothes', 'Women Clothes'),
        ('Kids Clothes', 'Kids Clothes'),
    ]
    sizechoices = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ]
    Accessorychoices = [
        ('Ring', 'Ring'),
        ('Handbag', 'Handbag'),
        ('Bracelet', 'Bracelet'),
        ('Necklace', 'Necklace'),
    ]

    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    price = models.FloatField()
    product_category = models.CharField(max_length=50, choices=Clotheschoices, default='Accessories')
    size = models.CharField(max_length=5, choices=sizechoices, blank=True, null=True)
    accessory_type = models.CharField(max_length=50, choices=Accessorychoices, blank=True, null=True)
    available = models.BooleanField(default=True)

    def _str_(self):
        return self.product_name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    added_by_admin = models.BooleanField(default=False)
    cart_items = models.JSONField(default=list)

    def _str_(self):
        return f"Cart of {self.user.username}"

    def add_item(self, product, quantity):
        for item in self.cart_items:
            if item['product_id'] == product.id:
                item['quantity'] += quantity
                break
        else:
            self.cart_items.append({'product_id': product.id, 'quantity': quantity})
        self.save()

    def remove_item(self, product):
        self.cart_items = [item for item in self.cart_items if item['product_id'] != product.id]
        self.save()

    def update_item_quantity(self, product, quantity):
        for item in self.cart_items:
            if item['product_id'] == product.id:
                item['quantity'] = quantity
                break
        self.save()

    def total_price(self):
        total = 0
        for item in self.cart_items:
            product = Product.objects.get(id=item['product_id'])
            total += product.price * item['quantity']
        return total


class Payment(models.Model):
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('CARD', 'Card Payment'),
    ]
    CARD_CHOICES = [
        ('CIB', 'CIB'),
        ('QNB', 'QNB'),
        ('MEEZA', 'Meeza'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('SUCCEEDED', 'Succeeded'),
        ('FAILED', 'Failed'),
        ('PENDING', 'Pending'),
    ]

    street_address = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='COD')
    card_type = models.CharField(max_length=5, choices=CARD_CHOICES, blank=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    total_amount = models.FloatField()

    def _str_(self):
        return f"Payment {self.id} - {self.payment_method} - {self.payment_status}"


class Order(models.Model):
    STATUS = [
        ('ordered', 'Ordered Successfully'),
        ('failed', 'Failed to Order'),
    ]

    order_id = models.AutoField(primary_key=True)
    order_date = models.DateField()
    total_price = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='ordered')

    def _str_(self):
        return f"Order {self.order_id} - {self.status}"


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    user_id = models.CharField(max_length=50, unique=True)

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)

    genderchoices = [
        ('Female', 'Female'),
        ('Male', 'Male'),
    ]
    gender = models.CharField(max_length=6, choices=genderchoices)

    age = models.IntegerField()

    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def _str_(self):
        return f'{self.first_name} {self.last_name} ({self.username})'