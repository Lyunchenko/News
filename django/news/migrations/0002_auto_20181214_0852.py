# Generated by Django 2.1.4 on 2018-12-14 03:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='News',
            new_name='NewsData',
        ),
    ]
