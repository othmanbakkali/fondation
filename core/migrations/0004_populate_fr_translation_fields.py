from django.db import migrations


MODEL_FIELDS = {
    "PageContent": ("title", "subtitle", "content", "meta_title", "meta_description", "keywords"),
    "ContentItem": ("title", "category", "summary", "body", "meta_title", "meta_description", "keywords", "location", "instructor_name"),
    "Partner": ("name", "partner_type", "description"),
    "SiteSetting": ("value",),
}


def populate_fr(apps, schema_editor):
    for model_name, fields in MODEL_FIELDS.items():
        model = apps.get_model("core", model_name)
        for obj in model.objects.all():
            changed = []
            for field in fields:
                fr_field = f"{field}_fr"
                if hasattr(obj, fr_field) and not getattr(obj, fr_field, None):
                    setattr(obj, fr_field, getattr(obj, field, ""))
                    changed.append(fr_field)
            if changed:
                obj.save(update_fields=changed)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_alter_contactmessage_options_and_more"),
    ]

    operations = [
        migrations.RunPython(populate_fr, noop_reverse),
    ]
