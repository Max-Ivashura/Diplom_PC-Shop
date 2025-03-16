# configurator/models.py
from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product

class PCBuild(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    components = models.ManyToManyField(Product, through='BuildComponent')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_saved = models.BooleanField(default=False)  # Черновик или готовая сборка
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total_price(self):
        self.total_price = sum(component.product.price for component in self.buildcomponent_set.all())
        self.save()

    def __str__(self):
        return self.title

class BuildComponent(models.Model):
    build = models.ForeignKey(PCBuild, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} in {self.build.title}"

