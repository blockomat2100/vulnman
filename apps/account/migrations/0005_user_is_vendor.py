# Generated by Django 4.0.5 on 2022-06-16 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_pentesterprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_vendor',
            field=models.BooleanField(default=False),
        ),
    ]
