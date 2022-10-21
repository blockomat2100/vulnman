# Generated by Django 4.1.2 on 2022-10-19 05:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0015_projectcontributor_invite_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetTechnology',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('asset_type', models.CharField(choices=[('webapplication', 'Web Application'), ('host', 'Host'), ('service', 'Service')], default='webapplication', max_length=64)),
                ('object_id', models.UUIDField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
            options={
                'ordering': ['-date_updated'],
            },
        ),
        migrations.CreateModel(
            name='Technology',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
                ('programming_language', models.CharField(blank=True, max_length=128, null=True)),
                ('homepage', models.URLField(blank=True, null=True)),
                ('version', models.CharField(blank=True, max_length=16, null=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Technology',
                'verbose_name_plural': 'Technologies',
                'ordering': ['-date_updated'],
                'unique_together': {('name', 'version')},
            },
        ),
        migrations.CreateModel(
            name='ChecklistTask',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('task_id', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
                'ordering': ['-date_updated'],
                'abstract': False,
                'unique_together': {('task_id',)},
            },
        ),
    ]
