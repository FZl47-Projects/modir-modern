# Generated by Django 4.2.6 on 2024-03-16 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='file_url',
            field=models.URLField(blank=True, null=True, verbose_name='لینک فایل'),
        ),
    ]
