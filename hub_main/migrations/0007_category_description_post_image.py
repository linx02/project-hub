# Generated by Django 4.2.4 on 2023-09-08 13:17

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub_main', '0006_alter_comment_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, default='default_image.jpg', max_length=255, null=True),
            preserve_default=False,
        ),
    ]
