# Generated by Django 4.1.2 on 2022-10-07 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_alter_projectcontact_unique_together_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProjectContact',
        ),
    ]
