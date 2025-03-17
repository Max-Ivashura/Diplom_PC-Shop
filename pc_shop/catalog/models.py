from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from .utils import generate_image_filename  # Теперь безопасно


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class AttributeGroup(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class Attribute(models.Model):
    ATTRIBUTE_TYPES = (
        ('string', 'Строка'),
        ('number', 'Число'),
        ('boolean', 'Да/Нет'),
        ('choice', 'Выбор')
    )

    group = models.ForeignKey(AttributeGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20, blank=True)  # Единица измерения (например, ГГц)
    attribute_type = models.CharField(max_length=20, choices=ATTRIBUTE_TYPES)
    order = models.IntegerField(default=0)
    required = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.group.category.name} → {self.group.name} → {self.name} (порядок: {self.order})"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def attributes_dict(self):
        if not hasattr(self, '_attributes_cache'):
            self._attributes_cache = {
                av.attribute: av
                for av in self.attributevalue_set.select_related('attribute').all()
            }
        return self._attributes_cache

    def get_attribute_value(self, attribute):
        return self.attributes_dict.get(attribute)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            # Создаем все атрибуты для категории
            for attr in Attribute.objects.filter(group__category=self.category):
                AttributeValue.objects.get_or_create(product=self, attribute=attr)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)  # Используйте строковый импорт
    image = models.ImageField(upload_to=generate_image_filename)
    is_main = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)  # Для сортировки

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.product.name}"


class AttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value_string = models.CharField(max_length=255, blank=True, null=True)
    value_number = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    value_boolean = models.BooleanField(null=True)
    value_choice = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        unique_together = ('product', 'attribute')

    def get_value_for_attribute(self, attribute_id):
        try:
            return self.attributevalue.objects.get(
                product=self.product,
                attribute_id=attribute_id
            ).get_value()
        except AttributeValue.DoesNotExist:
            return None

    def get_value(self):
        if self.attribute.attribute_type == 'string':
            return self.value_string
        elif self.attribute.attribute_type == 'number':
            return self.value_number
        elif self.attribute.attribute_type == 'boolean':
            return self.value_boolean
        elif self.attribute.attribute_type == 'choice':
            return self.value_choice
        return None


class Comparison(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)  # Для неавторизованных пользователей
    products = models.ManyToManyField('Product', blank=True)

    def __str__(self):
        return f"Сравнение {self.id}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
