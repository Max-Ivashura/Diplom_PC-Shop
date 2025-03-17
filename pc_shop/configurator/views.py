from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PCBuild, BuildComponent
from catalog.models import Category, Product
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import check_compatibility_logic

@login_required
def configurator_view(request):
    categories = Category.objects.all()
    build = PCBuild.objects.filter(user=request.user, is_saved=False).first()
    if not build:
        build = PCBuild.objects.create(user=request.user, title="Новая сборка")

    # Подготовка данных для шаблона
    component_data = []
    for category in categories:
        component = build.components.filter(category=category).first()
        component_data.append({
            'category': category,
            'component': component,
            'image': component.productimage_set.first().image.url if component else None
        })

    return render(request, 'configurator/configurator.html', {
        'categories': categories,
        'build': build,
        'component_data': component_data
    })


@csrf_exempt
def check_compatibility_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        component_ids = data.get('components', [])
        components = Product.objects.filter(id__in=component_ids)
        errors, compatibility_status = check_compatibility_logic(components)
        return JsonResponse({
            'errors': errors,
            'compatibility_status': compatibility_status
        })
    return JsonResponse({'errors': [], 'compatibility_status': []})


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