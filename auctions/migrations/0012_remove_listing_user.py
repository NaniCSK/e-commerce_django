# Generated by Django 4.2.6 on 2024-03-26 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_listing_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='user',
        ),
    ]
