# Generated by Django 3.2.4 on 2022-10-19 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0004_auto_20221018_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_title',
            field=models.CharField(max_length=255, verbose_name='Post Title'),
        ),
    ]
