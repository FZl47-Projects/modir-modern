# Generated by Django 4.2.6 on 2024-02-04 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_alter_rawmaterial_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawmaterial',
            name='use_price',
            field=models.PositiveIntegerField(default=0, help_text='Per unit', verbose_name='Use price'),
        ),
    ]
