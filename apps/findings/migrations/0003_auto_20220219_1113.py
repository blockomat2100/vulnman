# Generated by Django 3.2.12 on 2022-02-19 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('findings', '0002_alter_vulnerabilitycategory_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vulnerability',
            name='method',
        ),
        migrations.RemoveField(
            model_name='vulnerability',
            name='parameter',
        ),
        migrations.RemoveField(
            model_name='vulnerability',
            name='parameters',
        ),
        migrations.RemoveField(
            model_name='vulnerability',
            name='path',
        ),
        migrations.RemoveField(
            model_name='vulnerability',
            name='query_parameters',
        ),
        migrations.RemoveField(
            model_name='vulnerability',
            name='site',
        ),
    ]
