# Generated by Django 3.2.4 on 2022-10-18 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0003_alter_image_image_related_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_related_post',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='post_image', to='blog_app.post'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image_related_section',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='section_image', to='blog_app.section'),
        ),
    ]
