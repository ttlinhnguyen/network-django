# Generated by Django 3.2.5 on 2021-08-02 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]
