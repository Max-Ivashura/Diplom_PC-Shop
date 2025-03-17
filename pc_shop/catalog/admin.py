from django.db.models import Prefetch

from .models import Category, AttributeGroup, Attribute, AttributeValue
from django.utils.html import format_html
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import admin
from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from .models import ProductImage
from django import forms
from django.urls import path
from django.template.response import TemplateResponse
from .models import Attribute, Product


class ProductImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = ProductImage
    extra = 0
    fields = ('image', 'is_main', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return format_html('<img src="{}" style="max-height: 100px;" />', obj.image.url)

    image_preview.short_description = 'Миниатюра'


class AttributeValueForm(forms.ModelForm):
    class Meta:
        model = AttributeValue
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance']:
            self.fields['attribute'].queryset = Attribute.objects.filter(
                group__category=kwargs['instance'].product.category
            ).order_by('group__order', 'order')


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    form = AttributeValueForm
    extra = 0

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('attribute__group').order_by(
            'attribute__group__order',
            'attribute__order'
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "attribute":
            kwargs["queryset"] = Attribute.objects.order_by('group__order', 'order')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Product)
class ProductAdmin(SortableAdminBase, admin.ModelAdmin):  # Добавлено наследование
    list_display = ('preview_and_name', 'category', 'price', 'in_stock', 'image_management_link')
    list_filter = ('category', 'in_stock')
    search_fields = ('name',)
    inlines = [ProductImageInline, AttributeValueInline]

    class Media:
        css = {
            'all': (
                'admin/css/product_admin.css',  # Стили для админки продукта
                'admin/css/attribute_groups.css',  # Стили для групп атрибутов
                'admin/css/custom_admin.css',
            )
        }
        js = (
            'admin/js/product_admin.js',
            'admin/js/product_attribute.js',
            'admin/js/attribute_filter.js',
        )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        product = self.get_object(request, object_id)
        extra_context['attribute_values_dict'] = {
            str(av.attribute_id): av  # Используем строки для ключей
            for av in product.attributevalue_set.select_related('attribute').all()
        }
        return super().change_view(request, object_id, form_url, extra_context)

    def preview_and_name(self, obj):
        main_image = obj.productimage_set.filter(is_main=True).first()
        image_url = main_image.image.url if main_image else '/static/admin/img/icon-no.svg'
        return format_html(
            '<a href="{}" class="product-link" style="display: flex; align-items: center; text-decoration: none;">'
            '<img src="{}" style="max-height: 40px; margin-right: 10px;" />'
            '<span>{}</span>'
            '</a>',
            reverse('admin:catalog_product_change', args=[obj.pk]),
            image_url,
            obj.name
        )

    preview_and_name.short_description = 'Товар'
    preview_and_name.allow_tags = True

    def thumbnail_preview(self, obj):
        images = obj.productimage_set.all()
        if images:
            main_image = images.filter(is_main=True).first() or images.first()
            return format_html(
                '<a href="{}"><img src="{}" style="max-height: 50px;" /></a>',
                reverse('admin:catalog_product_change', args=[obj.pk]),
                main_image.image.url
            )
        return '-'

    thumbnail_preview.short_description = 'Превью'

    def manage_images(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        return redirect(f'/admin/catalog/product/{product_id}/change/#productimage_set-group')

    def image_management_link(self, obj):
        return format_html(
            '<a href="{}" class="button">Изображения</a>',
            reverse('admin:manage_product_images', args=[obj.pk])
        )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('get_attributes/', self.admin_site.admin_view(self.get_attributes_view),
                 name='get_attributes'),
        ]
        return custom_urls + urls

    def get_attributes_view(self, request):
        category_id = request.GET.get('category_id')
        category = get_object_or_404(Category, id=category_id)

        attribute_groups = category.attributegroup_set.prefetch_related(
            Prefetch('attribute_set', queryset=Attribute.objects.order_by('order'))
        ).order_by('order')

        return TemplateResponse(request, 'admin/catalog/product/attribute_groups.html', {
            'attribute_groups': attribute_groups,
            'original': self.get_object(request, request.GET.get('product_id')),
        })

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        attributes_data = request.POST.get('attributes', {})
        # Обработка сохранения атрибутов

    image_management_link.short_description = 'Действия'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class AttributeInline(admin.TabularInline):
    model = Attribute
    extra = 0
    fields = ('name', 'unit', 'attribute_type', 'order', 'required')
    ordering = ('order',)


@admin.register(AttributeGroup)
class AttributeGroupAdmin(admin.ModelAdmin):
    inlines = [AttributeInline]
    list_display = ('name', 'category', 'order')
    list_filter = ('category',)
    ordering = ('category', 'order')


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': (
                'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
                'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css',
                'admin/css/admin.css'  # Пользовательские стили
            )
        }
        js = ('https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',)

    list_display = ('name', 'group_category', 'group_name', 'order', 'attribute_type')
    list_filter = ('group__category', 'group')
    ordering = ('group__category__name', 'group__order', 'order')

    def group_category(self, obj):
        return obj.group.category.name

    group_category.short_description = 'Категория'

    def group_name(self, obj):
        return obj.group.name

    group_name.short_description = 'Группа'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['categories'] = Category.objects.prefetch_related('attributegroup_set__attribute_set').all()
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(AttributeValue)
