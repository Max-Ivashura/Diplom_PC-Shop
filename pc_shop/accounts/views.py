from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from orders.models import Order
from configurator.models import PCBuild
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import FormView


@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user)
    builds = PCBuild.objects.filter(user=request.user)
    return render(request, 'accounts/profile.html', {
        'orders': orders,
        'builds': builds
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    profile = request.user.profile
    if profile.favorite_products.filter(id=product.id).exists():
        profile.favorite_products.remove(product)
    else:
        profile.favorite_products.add(product)
    return redirect('product_detail', pk=product_id)


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

class RegisterView(FormView):
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

def logout_view(request):
    logout(request)
    return redirect('product_list')
