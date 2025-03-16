from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from cart.models import Cart
from .models import Order, OrderItem
from .forms import OrderForm
from django.shortcuts import get_object_or_404

@login_required
def checkout_view(request):
    cart = request.user.cart
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = sum(item.total_price() for item in cart.cartitem_set.all())
            order.save()

            # Создаем элементы заказа
            for cart_item in cart.cartitem_set.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )

            # Очищаем корзину
            cart.cartitem_set.all().delete()

            # Отправляем email-уведомления
            send_order_confirmation(request, order)
            send_order_notification_to_admin(request, order)

            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm()

    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart': cart
    })

def send_order_confirmation(request, order):
    subject = f"Подтверждение заказа #{order.id}"
    message = render_to_string('orders/email_confirmation.html', {
        'order': order,
        'request': request
    })
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.user.email])

def send_order_notification_to_admin(request, order):
    subject = f"Новый заказ #{order.id}"
    message = f"Пользователь {order.user.username} оформил заказ на сумму {order.total_price} руб."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})