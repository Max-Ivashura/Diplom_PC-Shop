from .models import Category, Product
from django.core.paginator import Paginator
from .filters import ProductFilter
from .models import Product, Comparison
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductForm
from .models import Product, AttributeValue
import logging
logger = logging.getLogger(__name__)


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(in_stock=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    filter = ProductFilter(request.GET, queryset=products)
    products = filter.qs

    paginator = Paginator(products, 6)  # 6 товаров на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalog/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'filter': filter,
        'page_obj': page_obj
    })


def product_detail(request, pk):
    product = get_object_or_404(
        Product.objects.prefetch_related(
            'attributevalue_set__attribute__group'  # Загружаем связанные данные
        ),
        pk=pk
    )
    return render(request, 'catalog/product_detail.html', {'product': product})


def comparison_view(request):
    comparison = None

    if request.user.is_authenticated:
        comparison = Comparison.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        comparison = Comparison.objects.filter(session_key=session_key).first()

    return render(request, 'catalog/compare.html', {'comparison': comparison})


def add_to_comparison(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comparison = None

    if request.user.is_authenticated:
        comparison, created = Comparison.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        comparison, created = Comparison.objects.get_or_create(session_key=session_key)

    if product not in comparison.products.all():
        comparison.products.add(product)

    return redirect('product_detail', pk=product_id)


def remove_from_comparison(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comparison = None

    if request.user.is_authenticated:
        comparison = Comparison.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        comparison = Comparison.objects.filter(session_key=session_key).first()

    if comparison and product in comparison.products.all():
        comparison.products.remove(product)

    return redirect('comparison_view')


def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        logger.debug(f"POST data: {request.POST}")  # <-- Логируем данные
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()

            for attr_value in product.attributevalue_set.all():
                field_name = f'attr_{attr_value.attribute.id}'
                logger.debug(f"Processing {field_name}: {request.POST.get(field_name)}")  # <-- Логируем каждое поле
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()

            # Сохранение атрибутов
            for attr_value in product.attributevalue_set.all():
                field_name = f'attr_{attr_value.attribute.id}'
                if field_name in request.POST:
                    raw_value = request.POST[field_name]
                    attr_type = attr_value.attribute.attribute_type

                    if attr_type == 'boolean':
                        # Checkbox возвращает 'on' или None
                        attr_value.value_boolean = (raw_value == 'on')
                    elif attr_type == 'number':
                        attr_value.value_number = raw_value
                    elif attr_type == 'choice':
                        attr_value.value_choice = raw_value
                    else:
                        attr_value.value_string = raw_value

                    attr_value.save()

            return redirect('product_detail', pk=pk)
    else:
        form = ProductForm(instance=product)

    return render(request, 'admin/catalog/product_edit.html', {
        'form': form,
        'product': product
    })
