# Generated by Django 4.2.6 on 2024-05-14 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0002_alter_subscription_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='type',
            field=models.CharField(choices=[(0, 'One week'), (1, 'یک ماه'), (2, 'دو ماه'), (3, 'سه ماه'), (6, 'شش ماه'), (12, 'دوازده ماه')], max_length=6, unique=True, verbose_name='نوع اشتراک'),
        ),
    ]
