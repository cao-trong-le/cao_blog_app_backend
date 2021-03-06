# Generated by Django 3.2.4 on 2022-05-20 10:00

import blog_app.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comment_code', models.CharField(default=blog_app.models._comment_code, max_length=15, unique=True, verbose_name='Comment Code')),
                ('comment_content', models.TextField(default='', max_length=5000, null=True, verbose_name='Comment Content')),
                ('comment_time', models.DateTimeField(auto_now_add=True, verbose_name='Comment Time')),
                ('comment_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('post_code', models.CharField(default=blog_app.models._post_code, max_length=15, unique=True, verbose_name='Post Code')),
                ('post_title', models.CharField(max_length=255, unique=True, verbose_name='Post Title')),
                ('post_summary', models.TextField(default='', max_length=500, null=True, verbose_name='Post Summary')),
                ('post_public', models.BooleanField(default=True, verbose_name='Post Public')),
                ('post_likes', models.IntegerField(default=0, max_length=10, verbose_name='Post Likes')),
                ('post_views', models.IntegerField(default=0, max_length=10, verbose_name='Post Views')),
                ('post_edited', models.BooleanField(default=False, verbose_name='Post Editted')),
                ('post_date', models.DateTimeField(auto_now_add=True, verbose_name='Post Date')),
                ('post_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('section_code', models.CharField(default=blog_app.models._post_code, max_length=15, unique=True, verbose_name='Section Code')),
                ('section_title', models.CharField(default='', max_length=255, null=True, verbose_name='Section Title')),
                ('section_content', models.TextField(default='', max_length=10000, null=True, verbose_name='Section Content')),
                ('section_public', models.BooleanField(default=True, verbose_name='Section Public')),
                ('section_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='section_user', to=settings.AUTH_USER_MODEL)),
                ('section_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='section_post', to='blog_app.post')),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('reply_code', models.CharField(default=blog_app.models._comment_code, max_length=15, unique=True, verbose_name='Reply Code')),
                ('reply_content', models.TextField(default='', max_length=5000, null=True, verbose_name='Reply Content')),
                ('reply_time', models.DateTimeField(auto_now_add=True, verbose_name='reply Time')),
                ('reply_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_user', to=settings.AUTH_USER_MODEL)),
                ('reply_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_comment', to='blog_app.comment')),
                ('reply_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_post', to='blog_app.post')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image_code', models.CharField(default=blog_app.models._image_code, max_length=15, unique=True, verbose_name='Image Code')),
                ('image_content', models.ImageField(default=blog_app.models.default_image, null=True, upload_to=blog_app.models.get_image_filepath, verbose_name='Image Content')),
                ('image_related_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_image', to='blog_app.post')),
                ('image_related_section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='section_image', to='blog_app.section')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_post', to='blog_app.post'),
        ),
    ]
