# Generated by Django 3.2.12 on 2022-12-04 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20221203_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='field',
            field=models.CharField(blank=True, default='General', max_length=200, null=True),
        ),
    ]
