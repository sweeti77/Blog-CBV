# Generated by Django 3.1.1 on 2021-05-20 18:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210520_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='posted_date',
            field=models.DateField(default=datetime.datetime(2021, 5, 20, 18, 22, 52, 64337, tzinfo=utc)),
        ),
    ]