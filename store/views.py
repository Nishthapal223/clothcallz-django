from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, Order, Address
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import razorpay

# ==============================
# Home page
# ==============================
def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

# ==============================
# Add to cart
# ==============================
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.name} added to cart!")
    return redirect('home')

# ==============================
# View cart
# ==============================
@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})

# ==============================
# Buy Now (Direct purchase of a single product)
# ==============================
@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        address_id = request.POST.get("address")

        if not address_id or not payment_method:
            messages.error(request, "Please select address and payment method!")
            return redirect("buy_now", product_id=product.id)

        address = get_object_or_404(Address, id=address_id, user=request.user)

        # Create order
        order = Order.objects.create(
            user=request.user,
            address=address,
            total_price=product.price,
            payment_method=payment_method,
            payment_status=(payment_method == "COD")
        )

        if payment_method == "COD":
            messages.success(request, "Order placed successfully with Cash on Delivery!")
            return redirect("order_success", order_id=order.id)
        elif payment_method == "UPI":
            return redirect("upi_payment", order_id=order.id)
        elif payment_method == "RAZORPAY":
            return redirect("razorpay_payment", order_id=order.id)

    addresses = Address.objects.filter(user=request.user)
    return render(request, "store/buy_now.html", {"product": product, "addresses": addresses})

# ==============================
# Checkout - Select Address & Payment Method
# ==============================
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

        # Create order
        order = Order.objects.create(
            user=request.user,
            address=address,
            total_price=total_price,
            payment_method=payment_method,
            payment_status=(payment_method == "COD")
        )

        if payment_method == "COD":
            cart_items.delete()
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

# ==============================
# UPI Payment Page
# ==============================
@login_required
def upi_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    upi_id = "palaknishtha@upi"  # 🔹 Replace with your actual UPI ID

    if request.method == "POST":
        order.payment_status = True
        order.save()
        Cart.objects.filter(user=request.user).delete()  # Clear cart after payment
        messages.success(request, "Payment received via UPI!")
        return redirect("order_success", order_id=order.id)

    return render(request, "store/upi_payment.html", {"order": order, "upi_id": upi_id})

# ==============================
# Razorpay Payment Page
# ==============================
@login_required
def razorpay_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Create a Razorpay order
    razorpay_order = client.order.create({
        "amount": int(order.total_price * 100),  # amount in paise
        "currency": "INR",
        "payment_capture": 1
    })

    if request.method == "POST":
        # Payment success webhook can be handled here or via JS callback
        order.payment_status = True
        order.save()
        Cart.objects.filter(user=request.user).delete()  # Cl
# ==============================
# Order Success Page
# ==============================
@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_success.html', {'order': order})
