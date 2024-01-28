# Generated by Django 4.2.6 on 2024-01-28 19:35

import apps.ticket.utils
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
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='بدون عنوان', max_length=128, verbose_name='عنوان')),
                ('type', models.CharField(choices=[('general', 'مشکل عمومی/پیشنهاد'), ('technical', 'مشکل فنی')], default='general', max_length=64, verbose_name='نوع')),
                ('status', models.CharField(choices=[('open', 'باز'), ('close', 'بسته شده')], default='open', max_length=32, verbose_name='وضعیت')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='زمان ویرایش')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tickets', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'تیکت',
                'verbose_name_plural': 'تیکت\u200cها',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=512, verbose_name='متن')),
                ('file', models.FileField(blank=True, null=True, upload_to=apps.ticket.utils.ticket_file_src, verbose_name='فایل مرتبط')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='زمان ویرایش')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='ticket.ticket', verbose_name='تیکت')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ticket_messages', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'پیام تیکت',
                'verbose_name_plural': 'پیام\u200cهای تیکت',
            },
        ),
    ]