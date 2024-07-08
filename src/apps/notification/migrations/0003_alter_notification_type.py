# Generated by Django 4.2.6 on 2024-07-08 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_alter_notification_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('MOBILE_VERIFICATION_CODE', 'کد تاییدیه موبایل'), ('SUBSCRIPTION_END_WARNING', 'هشدار پایان اشتراک'), ('NEW_COUNSELING_FORM_SUBMITED', 'New counseling form submited')], max_length=128, verbose_name='نوع اعلان'),
        ),
    ]
