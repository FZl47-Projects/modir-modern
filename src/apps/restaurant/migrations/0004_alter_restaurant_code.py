# Generated by Django 4.2.6 on 2024-07-04 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_alter_preparedmaterialcategory_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='code',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='کد'),
        ),
    ]
