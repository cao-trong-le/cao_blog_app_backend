# Generated by Django 3.2.4 on 2022-10-11 08:13

from django.db import migrations, models
import user_management.models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0004_alter_newuser_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='code',
            field=models.CharField(default=user_management.models._user_code, max_length=255, null=True, unique=True, verbose_name='User Code'),
        ),
    ]