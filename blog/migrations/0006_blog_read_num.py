# Generated by Django 2.2 on 2020-05-17 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20200517_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='read_num',
            field=models.IntegerField(default=0),
        ),
    ]