# Generated by Django 4.2.6 on 2024-01-26 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='فعال'),
        ),
    ]