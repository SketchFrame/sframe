# Generated by Django 2.2.4 on 2019-10-13 10:31

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20191013_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(blank=True, choices=[('Pencil work', 'Pencil work'), ('Pastel colours', 'Pastel colours'), ('Water colours', 'Water colours'), ('Acrylic colours', 'Acrylic colours'), ('Fabric colours', 'Fabric colours'), ('Oil colours', 'Oil colours'), ('Mix media', 'Mix Media')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='height',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='originalPrice',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='shortDescription',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='weight',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='width',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
