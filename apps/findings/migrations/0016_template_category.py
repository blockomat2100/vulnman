# Generated by Django 4.0.4 on 2022-04-15 13:51

from django.db import migrations, models
import django.db.models.deletion


def migrate_categories(apps, schema_editor):
    Template = apps.get_model("findings", "Template")
    for template in Template.objects.all():
        template.category = template.categories.first()
        template.save()


class Migration(migrations.Migration):

    dependencies = [
        ('findings', '0015_vulnerabilitycategory_display_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='templates_set', to='findings.vulnerabilitycategory'),
        ),
        migrations.RunPython(migrate_categories)
    ]
