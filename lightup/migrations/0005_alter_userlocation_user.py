# Generated by Django 3.2.5 on 2021-08-10 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lightup', '0004_auto_20210811_0206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlocation',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='lightup.userinfo'),
        ),
    ]
