# Generated by Django 4.2 on 2024-05-28 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cv', models.FileField(upload_to='cv')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
