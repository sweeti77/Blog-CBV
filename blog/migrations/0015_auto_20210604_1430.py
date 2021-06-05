# Generated by Django 3.1.1 on 2021-06-04 14:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20210603_1059'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, default='Literature', max_length=35)),
                ('slug', models.SlugField(max_length=35, unique=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ('title',),
            },
        ),
        migrations.AlterField(
            model_name='blog',
            name='posted_date',
            field=models.DateField(default=datetime.datetime(2021, 6, 4, 14, 30, 24, 965831, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='blog',
            name='category',
            field=models.ManyToManyField(to='blog.Category'),
        ),
    ]
