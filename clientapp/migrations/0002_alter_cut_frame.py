# Generated by Django 4.2.4 on 2023-09-22 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cut',
            name='frame',
            field=models.CharField(default='black', max_length=5),
        ),
    ]
