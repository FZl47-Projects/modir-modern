# Generated by Django 4.2.6 on 2024-02-09 21:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0014_alter_recipematerial_prepared_material'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipematerial',
            name='raw_material',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipe_materials', to='restaurant.rawmaterial', verbose_name='ماده اولیه'),
        ),
    ]