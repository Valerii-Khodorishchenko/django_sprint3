# Generated by Django 3.2.16 on 2024-04-11 10:03

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20240410_2254'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='post',
            managers=[
                ('posts', django.db.models.manager.Manager()),
            ],
        ),
    ]
