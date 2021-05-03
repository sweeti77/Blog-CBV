# Generated by Django 3.1.1 on 2021-05-03 06:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('date_time', models.DateTimeField(default=datetime.datetime(2021, 5, 3, 6, 53, 16, 326543, tzinfo=utc))),
            ],
        ),
    ]