
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Product, Cart, Payment, Order
from django.contrib.auth.decorators import login_required



def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


#
@login_required
def view_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        return HttpResponse("Cart is empty", status=404)

    total = cart.total_price()  # Calculate total price
    return render(request, 'cart_view.html', {'cart': cart, 'total': total})



@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.add_item(product, 1)
    return redirect('view_cart')



@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart.remove_item(product)
    return redirect('view_cart')



@login_required
def update_item_quantity(request, product_id, quantity):
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart.update_item_quantity(product, quantity)
    return redirect('view_cart')



@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or cart.total_price() == 0:
        return HttpResponse("Cart is empty", status=400)


    payment = Payment.objects.create(
        street_address="123 Test Street",
        country="CountryName",
        phone_number="123456789",
        payment_method="COD",  # Default Cash on Delivery
        total_amount=cart.total_price(),
    )


    order = Order.objects.create(
        order_date=request.POST.get('order_date', '2024-01-01'),
        total_price=cart.total_price(),
        status="ordered",  # This is a placeholder as it could be dynamic
    )


    cart.cart_items.clear()
    cart.save()

    return render(request, 'checkout_success.html', {'payment': payment, 'order': order})




