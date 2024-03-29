# Generated by Django 4.2.6 on 2024-02-17 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IndexVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='زمان ویرایش')),
                ('title', models.CharField(default='بدون عنوان', max_length=255, verbose_name='عنوان')),
                ('description', models.TextField(blank=True, max_length=512, null=True, verbose_name='توضیحات')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='images/index/', verbose_name='کاور ویدیو')),
                ('video', models.FileField(blank=True, null=True, upload_to='images/index/', verbose_name='فایل ویدیو')),
                ('video_url', models.URLField(default='', verbose_name='لینک ویدیو')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
            ],
            options={
                'verbose_name': 'ویدیو صفحه اصلی',
                'verbose_name_plural': 'ویدیوهای صفحه اصلی',
            },
        ),
        migrations.CreateModel(
            name='TopBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='زمان ویرایش')),
                ('title', models.CharField(blank=True, max_length=128, null=True, verbose_name='عنوان')),
                ('link', models.URLField(blank=True, null=True, verbose_name='لینک مرتبط')),
                ('image', models.ImageField(upload_to='images/banners/', verbose_name='تصویر کاور')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
            ],
            options={
                'verbose_name': 'بنر',
                'verbose_name_plural': 'بنرهای صفحه اصلی',
                'ordering': ('-id',),
            },
        ),
    ]
