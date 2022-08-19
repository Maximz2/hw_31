from django.core.validators import MinLengthValidator
from django.db import models

from users.models import User


class Category(models.Model):
    slug = models.CharField(max_length=10, unique=True, validators=[MinLengthValidator(5)])
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Ad(models.Model):
    name = models.CharField(max_length=100, validators=[MinLengthValidator(10)])
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.IntegerField(default=0, validators=[MinLengthValidator(0)])
    description = models.CharField(max_length=1000, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to="ads/", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.name


class Selection(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Ad)

    class Meta:
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'
