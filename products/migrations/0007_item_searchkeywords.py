# Generated by Django 2.2.4 on 2019-10-15 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20191013_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='searchKeywords',
            field=models.TextField(blank=True, default='[]', null=True),
        ),
    ]
