# Generated by Django 3.2.6 on 2021-11-10 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookMng', '0011_rename_total_rating_book_avg_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=200)),
            ],
        ),
    ]
