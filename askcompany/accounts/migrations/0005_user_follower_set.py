# Generated by Django 3.2.10 on 2021-12-25 09:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='follower_set',
            field=models.ManyToManyField(blank=True, related_name='following_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
