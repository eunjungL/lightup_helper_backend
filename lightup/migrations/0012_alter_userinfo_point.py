# Generated by Django 3.2.5 on 2021-08-14 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lightup', '0011_donationcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='point',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
