# Generated by Django 4.2 on 2024-05-23 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_alter_search_month_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='search',
            name='date_to_search',
            field=models.DateTimeField(verbose_name='Date'),
        ),
    ]