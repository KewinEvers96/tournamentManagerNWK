# Generated by Django 3.2.5 on 2021-08-07 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0002_auto_20210806_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]
