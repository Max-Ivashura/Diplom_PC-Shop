from django.shortcuts import render, get_object_or_404
from .models import Category, Product

from .filters import ProductFilter


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(in_stock=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    filter = ProductFilter(request.GET, queryset=products)
    products = filter.qs

    return render(request, 'catalog/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'filter': filter
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


def compare_view(request):
    comparison = None
    if request.user.is_authenticated:
        comparison = Comparison.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        comparison = Comparison.objects.filter(session_key=session_key).first()
    return render(request, 'catalog/compare.html', {'comparison': comparison})
