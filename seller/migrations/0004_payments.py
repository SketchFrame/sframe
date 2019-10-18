# Generated by Django 2.2.4 on 2019-10-17 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0003_auto_20191013_2352'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accountNumber', models.CharField(blank=True, max_length=20, null=True)),
                ('cif', models.CharField(blank=True, max_length=20, null=True)),
                ('fullName', models.CharField(blank=True, max_length=40, null=True)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.Seller')),
            ],
        ),
    ]