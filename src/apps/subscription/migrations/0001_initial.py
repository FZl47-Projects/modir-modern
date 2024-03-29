# Generated by Django 4.2.6 on 2024-02-17 02:56

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
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='زمان ویرایش')),
                ('type', models.SmallIntegerField(choices=[(1, 'یک ماه'), (2, 'دو ماه'), (3, 'سه ماه'), (6, 'شش ماه'), (12, 'دوازده ماه')], unique=True, verbose_name='نوع اشتراک')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='قیمت')),
                ('discount', models.PositiveIntegerField(default=0, verbose_name='تخفیف')),
                ('selling_price', models.PositiveIntegerField(default=0, verbose_name='قیمت فروش')),
                ('promo', models.BooleanField(default=False, verbose_name='ویژه')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
            ],
            options={
                'verbose_name': 'اشتراک',
                'verbose_name_plural': 'اشتراک ها',
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='زمان ویرایش')),
                ('expire_date', models.DateField(blank=True, null=True, verbose_name='تاریخ انقضا')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'مشترک',
                'verbose_name_plural': 'مشترکین',
                'ordering': ('-id',),
            },
        ),
    ]
