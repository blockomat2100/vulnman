# Generated by Django 3.2.9 on 2021-12-20 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0002_alter_reportsharetoken_share_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportsharetoken',
            name='report',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='reporting.report'),
        ),
    ]
