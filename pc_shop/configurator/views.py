from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PCBuild, BuildComponent
from catalog.models import Category, Product
from .utils import check_compatibility

@login_required
def configurator_view(request):
    categories = Category.objects.all()
    build = PCBuild.objects.filter(user=request.user, is_saved=False).first()
    if not build:
        build = PCBuild.objects.create(user=request.user, title="Новая сборка")

    if request.method == "POST":
        product_id = request.POST.get('product_id')
        category_id = request.POST.get('category_id')
        product = get_object_or_404(Product, id=product_id)
        category = get_object_or_404(Category, id=category_id)

        compatibility_errors = check_compatibility(build.components.all())
        if compatibility_errors:
            for error in compatibility_errors:
                messages.error(request, error)
        else:
            BuildComponent.objects.update_or_create(...)
            build.calculate_total_price()
        return redirect('configurator')

    return render(request, 'configurator/configurator.html', {
        'categories': categories,
        'build': build
    })


@login_required
def save_build(request):
    if request.method == "POST":
        build_id = request.POST.get('build_id')
        build = get_object_or_404(PCBuild, id=build_id, user=request.user)
        build.title = request.POST.get('title')
        build.description = request.POST.get('description')
        build.is_saved = True
        build.save()
        messages.success(request, "Сборка сохранена!")
        return redirect('configurator')
    return redirect('configurator')

def build_detail(request, pk):
    build = get_object_or_404(PCBuild, pk=pk)
    return render(request, 'configurator/build_detail.html', {'build': build})