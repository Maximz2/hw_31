# Generated by Django 4.1 on 2022-08-19 19:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(10)])),
                ('price', models.IntegerField(default=0, validators=[django.core.validators.MinLengthValidator(0)])),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('is_published', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='ads/')),
            ],
            options={
                'verbose_name': 'Объявление',
                'verbose_name_plural': 'Объявления',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=10, unique=True, validators=[django.core.validators.MinLengthValidator(5)])),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Selection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('items', models.ManyToManyField(to='ads.ad')),
            ],
            options={
                'verbose_name': 'Подборка',
                'verbose_name_plural': 'Подборки',
            },
        ),
    ]