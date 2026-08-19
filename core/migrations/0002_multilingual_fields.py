from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField("pagecontent", "title_ar", models.CharField(blank=True, max_length=180)),
        migrations.AddField("pagecontent", "title_en", models.CharField(blank=True, max_length=180)),
        migrations.AddField("pagecontent", "subtitle_ar", models.TextField(blank=True)),
        migrations.AddField("pagecontent", "subtitle_en", models.TextField(blank=True)),
        migrations.AddField("pagecontent", "content_ar", models.TextField(blank=True)),
        migrations.AddField("pagecontent", "content_en", models.TextField(blank=True)),
        migrations.AddField("pagecontent", "meta_title_ar", models.CharField(blank=True, max_length=180)),
        migrations.AddField("pagecontent", "meta_title_en", models.CharField(blank=True, max_length=180)),
        migrations.AddField("pagecontent", "meta_description_ar", models.TextField(blank=True)),
        migrations.AddField("pagecontent", "meta_description_en", models.TextField(blank=True)),
        migrations.AddField("pagecontent", "keywords_ar", models.CharField(blank=True, max_length=255)),
        migrations.AddField("pagecontent", "keywords_en", models.CharField(blank=True, max_length=255)),
        migrations.AddField("contentitem", "title_ar", models.CharField(blank=True, max_length=220)),
        migrations.AddField("contentitem", "title_en", models.CharField(blank=True, max_length=220)),
        migrations.AddField("contentitem", "category_ar", models.CharField(blank=True, max_length=80)),
        migrations.AddField("contentitem", "category_en", models.CharField(blank=True, max_length=80)),
        migrations.AddField("contentitem", "summary_ar", models.TextField(blank=True)),
        migrations.AddField("contentitem", "summary_en", models.TextField(blank=True)),
        migrations.AddField("contentitem", "body_ar", models.TextField(blank=True)),
        migrations.AddField("contentitem", "body_en", models.TextField(blank=True)),
        migrations.AddField("contentitem", "meta_title_ar", models.CharField(blank=True, max_length=180)),
        migrations.AddField("contentitem", "meta_title_en", models.CharField(blank=True, max_length=180)),
        migrations.AddField("contentitem", "meta_description_ar", models.TextField(blank=True)),
        migrations.AddField("contentitem", "meta_description_en", models.TextField(blank=True)),
        migrations.AddField("contentitem", "keywords_ar", models.CharField(blank=True, max_length=255)),
        migrations.AddField("contentitem", "keywords_en", models.CharField(blank=True, max_length=255)),
        migrations.AddField("partner", "name_ar", models.CharField(blank=True, max_length=180)),
        migrations.AddField("partner", "name_en", models.CharField(blank=True, max_length=180)),
        migrations.AddField("partner", "partner_type_ar", models.CharField(blank=True, max_length=100)),
        migrations.AddField("partner", "partner_type_en", models.CharField(blank=True, max_length=100)),
        migrations.AddField("partner", "description_ar", models.TextField(blank=True)),
        migrations.AddField("partner", "description_en", models.TextField(blank=True)),
    ]
