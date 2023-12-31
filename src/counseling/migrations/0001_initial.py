# Generated by Django 4.1.3 on 2023-09-24 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='counseling',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_created=True)),
                ('condition', models.CharField(choices=[('ph', 'byphone'), ('ip', 'inperson')], max_length=3)),
                ('topic', models.CharField(max_length=20)),
                ('job', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=10, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
    ]
