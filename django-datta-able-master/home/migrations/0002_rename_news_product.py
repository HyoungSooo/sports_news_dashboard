# Generated by Django 4.2.3 on 2023-07-12 05:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='News',
            new_name='Product',
        ),
    ]