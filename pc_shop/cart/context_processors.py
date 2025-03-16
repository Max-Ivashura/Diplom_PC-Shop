from .models import Cart

def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart = Cart.objects.filter(session_key=request.session.session_key).first()
    return {'cart': cart or Cart()}