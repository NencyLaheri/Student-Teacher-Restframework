# Generated by Django 4.1.1 on 2022-09-12 09:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stportal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationModel',
            fields=[
                ('app_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('uni_name', models.CharField(max_length=200)),
                ('program_name', models.CharField(max_length=200)),
                ('study_mode', models.CharField(choices=[('online', 'online'), ('on-campus', 'on-campus')], max_length=20)),
                ('status', models.CharField(choices=[('none', 'none'), ('accepted', 'accepted'), ('rejected', 'rejected')], default='none', max_length=20)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
