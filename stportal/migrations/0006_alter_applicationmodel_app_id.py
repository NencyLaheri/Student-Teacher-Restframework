# Generated by Django 4.1.1 on 2022-09-15 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stportal', '0005_alter_applicationmodel_app_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationmodel',
            name='app_id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]
