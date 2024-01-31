# Generated by Django 4.2.6 on 2024-01-31 14:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='زمان ویرایش')),
                ('title', models.CharField(default='بدون عنوان', max_length=128, verbose_name='عنوان')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurants', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'Restaurant',
                'verbose_name_plural': 'Restaurants',
            },
        ),
        migrations.CreateModel(
            name='RawMaterialCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='زمان ویرایش')),
                ('title', models.CharField(default='Test category', max_length=128, verbose_name='عنوان')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='raw_material_categories', to='restaurant.restaurant', verbose_name='Restaurant')),
            ],
            options={
                'verbose_name': 'Raw materials category',
                'verbose_name_plural': 'Raw materials categories',
            },
        ),
    ]
