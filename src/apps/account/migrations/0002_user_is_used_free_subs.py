# Generated by Django 4.2.6 on 2024-05-21 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_used_free_subs',
            field=models.BooleanField(default=False),
        ),
    ]
