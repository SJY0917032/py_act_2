# Generated by Django 3.2.10 on 2021-12-25 15:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('instagram', '0003_auto_20211225_2349'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like_user_set',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_post_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
