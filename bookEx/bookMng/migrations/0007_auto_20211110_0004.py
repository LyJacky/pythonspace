# Generated by Django 3.2.9 on 2021-11-10 00:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookMng', '0006_auto_20211109_2356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='username',
        ),
        migrations.AddField(
            model_name='book',
            name='username',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
