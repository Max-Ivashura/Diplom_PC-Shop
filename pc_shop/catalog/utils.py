# catalog/utils.py
import os
from django.utils.text import slugify
from transliterate import translit


def generate_image_filename(instance, filename):
    # Используем instance.product вместо импорта модели
    product = instance.product
    product_name = product.name
    transliterated = translit(product_name, 'ru', reversed=True)
    slug = slugify(transliterated).replace('-', '_').lower()

    # Определяем расширение
    ext = filename.split('.')[-1].lower()
    if ext not in ['jpg', 'jpeg', 'png', 'webp']:
        ext = 'jpg'

    # Определяем номер файла через QuerySet
    # Используем строковый импорт, чтобы избежать цикла
    ProductImage = instance.__class__
    existing_images = ProductImage.objects.filter(product=product).exclude(pk=instance.pk)
    max_num = existing_images.count()

    # Генерируем имя
    filename = f"{slug}_{max_num}.{ext}"
    return os.path.join('products', filename)