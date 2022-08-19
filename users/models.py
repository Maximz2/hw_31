from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from users.validators import AgeCheckValidator, CheckEmail

MIN_AGE = 9

class Location(models.Model):
    name = models.CharField(max_length=200, unique=True)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    ing = models.DecimalField(max_digits=8, decimal_places=6, null=True)

    class Meta:
        verbose_name = "Mecтo"
        verbose_name_plural = "Mecтa"

    def __str__(self):
        return self.name


class User(AbstractUser):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

    ROLES = [
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    ]

    role = models.CharField(max_length=50, choices=ROLES, default=USER)
    age = models.PositiveSmallIntegerField(null=True)
    locations = models.ManyToManyField(Location)
    birth_date = models.DateField(null=True, validators=[AgeCheckValidator])
    email = models.EmailField(unique=True, null=True, validators=[CheckEmail])

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    def __str__(self):
        return self.username
