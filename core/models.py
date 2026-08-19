from django.db import models
from django.utils.text import slugify

STATUS_CHOICES = [
    ("publie", "Publié"),
    ("brouillon", "Brouillon"),
    ("programme", "Programmé"),
    ("archive", "Archivé"),
    ("actif", "Actif"),
    ("inactif", "Inactif"),
    ("en_attente", "En attente"),
    ("accepte", "Accepté"),
    ("refuse", "Refusé"),
]

MODULE_CHOICES = [
    ("program", "Programmes"),
    ("activity", "Activités"),
    ("news", "Actualités"),
    ("formation", "Formations"),
    ("media", "Médias"),
    ("team", "Équipe"),
    ("testimonial", "Témoignages"),
    ("user", "Utilisateurs"),
]


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SiteSetting(TimeStampedModel):
    key = models.CharField(max_length=120, unique=True)
    value = models.TextField(blank=True)
    value_fr = models.TextField(blank=True, null=True)
    value_ar = models.TextField(blank=True, null=True)
    value_en = models.TextField(blank=True, null=True)
    group = models.CharField(max_length=80, default="general")

    class Meta:
        verbose_name = "Paramètre du site"
        verbose_name_plural = "Paramètres du site"

    def __str__(self):
        return self.key


class PageContent(TimeStampedModel):
    slug = models.SlugField(max_length=80, unique=True)
    title = models.CharField(max_length=180)
    title_fr = models.CharField(max_length=180, null=True)
    title_ar = models.CharField(max_length=180, null=True)
    title_en = models.CharField(max_length=180, null=True)
    subtitle = models.TextField(blank=True)
    subtitle_fr = models.TextField(blank=True, null=True)
    subtitle_ar = models.TextField(blank=True, null=True)
    subtitle_en = models.TextField(blank=True, null=True)
    hero_image_url = models.URLField(blank=True)
    content = models.TextField(blank=True)
    content_fr = models.TextField(blank=True, null=True)
    content_ar = models.TextField(blank=True, null=True)
    content_en = models.TextField(blank=True, null=True)
    sections = models.JSONField(default=list, blank=True)
    meta_title = models.CharField(max_length=180, blank=True)
    meta_title_fr = models.CharField(max_length=180, blank=True, null=True)
    meta_title_ar = models.CharField(max_length=180, blank=True, null=True)
    meta_title_en = models.CharField(max_length=180, blank=True, null=True)
    meta_description = models.TextField(blank=True)
    meta_description_fr = models.TextField(blank=True, null=True)
    meta_description_ar = models.TextField(blank=True, null=True)
    meta_description_en = models.TextField(blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True)
    keywords_fr = models.CharField(max_length=255, blank=True, null=True)
    keywords_ar = models.CharField(max_length=255, blank=True, null=True)
    keywords_en = models.CharField(max_length=255, blank=True, null=True)
    canonical_url = models.URLField(blank=True)
    og_image_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="publie")

    class Meta:
        ordering = ["slug"]
        verbose_name = "Contenu de page"
        verbose_name_plural = "Contenus de pages"


    def __str__(self):
        return self.title


class ContentItem(TimeStampedModel):
    module = models.CharField(max_length=30, choices=MODULE_CHOICES)
    title = models.CharField(max_length=220)
    title_fr = models.CharField(max_length=220, null=True)
    title_ar = models.CharField(max_length=220, null=True)
    title_en = models.CharField(max_length=220, null=True)
    slug = models.SlugField(max_length=240, blank=True)
    category = models.CharField(max_length=80, blank=True)
    category_fr = models.CharField(max_length=80, blank=True, null=True)
    category_ar = models.CharField(max_length=80, blank=True, null=True)
    category_en = models.CharField(max_length=80, blank=True, null=True)
    summary = models.TextField(blank=True)
    summary_fr = models.TextField(blank=True, null=True)
    summary_ar = models.TextField(blank=True, null=True)
    summary_en = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True)
    body_fr = models.TextField(blank=True, null=True)
    body_ar = models.TextField(blank=True, null=True)
    body_en = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True)
    gallery = models.JSONField(default=list, blank=True)
    video_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)
    author = models.CharField(max_length=120, blank=True)
    date = models.DateField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=180, blank=True)
    location_fr = models.CharField(max_length=180, blank=True, null=True)
    location_ar = models.CharField(max_length=180, blank=True, null=True)
    location_en = models.CharField(max_length=180, blank=True, null=True)
    instructor_name = models.CharField(max_length=120, blank=True)
    instructor_name_fr = models.CharField(max_length=120, blank=True, null=True)
    instructor_name_ar = models.CharField(max_length=120, blank=True, null=True)
    instructor_name_en = models.CharField(max_length=120, blank=True, null=True)
    total_seats = models.PositiveIntegerField(default=0)
    registered_seats = models.PositiveIntegerField(default=0)
    participants = models.PositiveIntegerField(default=0)
    reports_count = models.PositiveIntegerField(default=0)
    reading_time = models.PositiveIntegerField(default=3)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="publie")
    order = models.PositiveIntegerField(default=1)
    featured = models.BooleanField(default=False)
    meta_title = models.CharField(max_length=180, blank=True)
    meta_title_fr = models.CharField(max_length=180, blank=True, null=True)
    meta_title_ar = models.CharField(max_length=180, blank=True, null=True)
    meta_title_en = models.CharField(max_length=180, blank=True, null=True)
    meta_description = models.TextField(blank=True)
    meta_description_fr = models.TextField(blank=True, null=True)
    meta_description_ar = models.TextField(blank=True, null=True)
    meta_description_en = models.TextField(blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True)
    keywords_fr = models.CharField(max_length=255, blank=True, null=True)
    keywords_ar = models.CharField(max_length=255, blank=True, null=True)
    keywords_en = models.CharField(max_length=255, blank=True, null=True)
    canonical_url = models.URLField(blank=True)
    og_image_url = models.URLField(blank=True)

    class Meta:
        ordering = ["order", "-date", "-created_at"]
        verbose_name = "Élément de contenu"
        verbose_name_plural = "Éléments de contenu"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Partner(TimeStampedModel):
    name = models.CharField(max_length=180)
    name_fr = models.CharField(max_length=180, null=True)
    name_ar = models.CharField(max_length=180, null=True)
    name_en = models.CharField(max_length=180, null=True)
    partner_type = models.CharField(max_length=100, blank=True)
    partner_type_fr = models.CharField(max_length=100, blank=True, null=True)
    partner_type_ar = models.CharField(max_length=100, blank=True, null=True)
    partner_type_en = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(blank=True)
    logo_url = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    description_fr = models.TextField(blank=True, null=True)
    description_ar = models.TextField(blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="actif")
    featured_home = models.BooleanField(default=True)
    start_date = models.DateField(null=True, blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Partenaire"
        verbose_name_plural = "Partenaires"

    @property
    def initials(self):
        return "".join(word[:1] for word in self.name.split()[:3]).upper()

    def __str__(self):
        return self.name


class ContactMessage(TimeStampedModel):
    name = models.CharField(max_length=160)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=100, blank=True, default="")
    subject = models.CharField(max_length=180, blank=True)
    message = models.TextField()
    attachment_url = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=20, default="non_lu")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"

    def __str__(self):
        return f"{self.name} - {self.subject or 'Message'}"


class VolunteerApplication(TimeStampedModel):
    name = models.CharField(max_length=160)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=100, blank=True)
    skills = models.CharField(max_length=255, blank=True)
    skills_description = models.TextField(blank=True, default="")
    cv_url = models.CharField(max_length=255, blank=True, default="")
    availability = models.CharField(max_length=255, blank=True, default="")
    desired_fields = models.CharField(max_length=255, blank=True, default="")
    motivation = models.TextField(blank=True)
    experience = models.TextField(blank=True, default="")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="en_attente")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Candidature bénévole"
        verbose_name_plural = "Candidatures bénévoles"

    def __str__(self):
        return self.name


class FormationRegistration(TimeStampedModel):
    formation = models.ForeignKey(ContentItem, on_delete=models.CASCADE, related_name="registrations")
    name = models.CharField(max_length=160)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="en_attente")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Inscription formation"
        verbose_name_plural = "Inscriptions formations"

    def __str__(self):
        return f"{self.name} - {self.formation.title}"


class ActivityRegistration(TimeStampedModel):
    activity = models.ForeignKey(ContentItem, on_delete=models.CASCADE, related_name="activity_registrations")
    name = models.CharField(max_length=160)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="en_attente")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Inscription activité"
        verbose_name_plural = "Inscriptions activités"

    def __str__(self):
        return f"{self.name} - {self.activity.title}"


from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
