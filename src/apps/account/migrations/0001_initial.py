# Generated by Django 4.2.6 on 2024-02-15 18:56

import apps.account.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('phone_number', models.CharField(max_length=11, unique=True, verbose_name='شماره تلفن')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='آدرس الکترونیک')),
                ('first_name', models.CharField(blank=True, max_length=128, null=True, verbose_name='نام')),
                ('last_name', models.CharField(blank=True, max_length=128, null=True, verbose_name='نام خانوادگی')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('is_admin', models.BooleanField(default=False, verbose_name='ادمین')),
                ('is_verified', models.BooleanField(default=False, verbose_name='تایید شده')),
                ('token', models.CharField(blank=True, editable=False, max_length=64, null=True, verbose_name='توکن')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='زمان ویرایش')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربران',
            },
        ),
        migrations.CreateModel(
            name='Access',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('user', 'کاربر'), ('admin', 'ادمین')], default='user', max_length=32, unique=True, verbose_name='عنوان دسترسی')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
            ],
            options={
                'verbose_name': 'دسترسی',
                'verbose_name_plural': 'دسترسی ها',
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='زمان ویرایش')),
                ('melli_code', models.CharField(blank=True, max_length=10, null=True, validators=[apps.account.validators.validate_didit_type], verbose_name='کدملی')),
                ('gender', models.CharField(blank=True, choices=[('m', 'مرد'), ('f', 'زن')], max_length=8, null=True, verbose_name='جنسیت')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')),
                ('place_name', models.CharField(blank=True, max_length=128, null=True, verbose_name='نام مجموعه')),
                ('province', models.CharField(blank=True, max_length=64, null=True, verbose_name='استان')),
                ('city', models.CharField(blank=True, max_length=64, null=True, verbose_name='شهر')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/profiles/', verbose_name='تصویر')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'پروفایل کاربر',
                'verbose_name_plural': 'پروفایل کاربران',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='accesses',
            field=models.ManyToManyField(blank=True, related_name='user', to='account.access', verbose_name='دسترسی ها'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
