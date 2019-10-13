# Generated by Django 2.2.4 on 2019-10-12 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('bids', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='assignedTo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.UserExtended'),
        ),
        migrations.AddField(
            model_name='project',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_by', to='users.UserExtended'),
        ),
        migrations.AlterField(
            model_name='bids',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bid_by', to='seller.Seller'),
        ),
    ]