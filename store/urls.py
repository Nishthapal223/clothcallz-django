from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Cart
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),

    # Buy Now
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),

    # Checkout
    path('checkout/', views.checkout, name='checkout'),

    # Payments
    path('payment/upi/<int:order_id>/', views.upi_payment, name='upi_payment'),
    path('payment/razorpay/<int:order_id>/', views.razorpay_payment, name='razorpay_payment'),

    # Order success
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),

    # Authentication
    path('accounts/login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
