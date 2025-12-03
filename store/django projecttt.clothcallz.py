from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, Order, Address
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Home page
def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

# Add to cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.name} added to cart!")
    return redirect('home')

# View cart
@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})

# Checkout page - choose address & payment
@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    addresses = Address.objects.filter(user=request.user)

    if request.method == "POST":
        address_id = request.POST.get("address")
        payment_method = request.POST.get("payment_method")

        if not address_id or not payment_method:
            messages.error(request, "Please select address and payment method!")
            return redirect("checkout")

        address = get_object_or_404(Address, id=address_id, user=request.user)

        # Create Order
        order = Order.objects.create(
            user=request.user,
            address=address,
            total_price=total_price,
            payment_method=payment_method,
            payment_status=(payment_method == "COD")  # COD is paid at delivery
        )

        # Clear cart
        cart_items.delete()

        # Redirect based on payment method
        if payment_method == "COD":
            messages.success(request, "Order placed successfully with Cash on Delivery!")
            return redirect("order_success", order_id=order.id)
        elif payment_method == "UPI":
            return redirect("upi_payment", order_id=order.id)
        elif payment_method == "RAZORPAY":
            return redirect("razorpay_payment", order_id=order.id)

    return render(request, "store/checkout.html", {
        "cart_items": cart_items,
        "total_price": total_price,
        "addresses": addresses
    })

# Dummy UPI payment page
@login_required
def upi_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == "POST":
        order.payment_status = True
        order.save()
        messages.success(request, "Payment received via UPI!")
        return redirect("order_success", order_id=order.id)
    return render(request, "store/upi_payment.html", {"order": order})

# Dummy Razorpay payment page
@login_required
def razorpay_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == "POST":
        order.payment_status = True
        order.save()
        messages.success(request, "Payment successful via Razorpay!")
        return redirect("order_success", order_id=order.id)
    return render(request, "store/razorpay_payment.html", {"order": order})

# Order success page
@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "store/order_success.html", {"order": order})
