# Generated by Django 4.0.3 on 2022-03-21 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_project_cvss_required_project_pentest_method_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='is_archived',
        ),
    ]
