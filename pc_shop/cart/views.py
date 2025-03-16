from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.backends.db import SessionStore
from .models import Cart, CartItem
from catalog.models import Product
from django.shortcuts import render
from .models import Cart
from django.http import JsonResponse

def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'message': 'Товар добавлен в корзину',
            'total_items': cart.cartitem_set.count(),
        })
    return redirect('cart')

def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart')


def cart_view(request):
    cart = get_cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})