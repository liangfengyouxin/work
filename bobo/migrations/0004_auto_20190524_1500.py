# Generated by Django 2.2.1 on 2019-05-24 15:00

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bobo', '0003_guanzhu11'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Guanzhu11',
            new_name='Guanzhu',
        ),
    ]
