# Generated by Django 3.2.12 on 2022-12-01 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_auto_20221201_0617'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='lesson',
            field=models.TextField(blank=True, null=True),
        ),
    ]