# Generated by Django 4.2.4 on 2023-08-24 16:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hub_main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='github_repo_link',
            field=models.URLField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='live_link',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('github_profile_link', models.URLField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
