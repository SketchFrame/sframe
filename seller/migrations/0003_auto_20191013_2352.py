# Generated by Django 2.2.4 on 2019-10-13 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0002_auto_20191013_0036'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seller',
            old_name='specialty',
            new_name='speciality',
        ),
    ]