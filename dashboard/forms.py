import json
from django import forms
from core.models import ContentItem, Partner, PageContent, SiteSetting, ContactMessage, VolunteerApplication, FormationRegistration, ActivityRegistration

def _(text):
    return text


IMAGE_URL_FIELDS = {"image_url", "logo_url", "hero_image_url", "og_image_url"}


FIELD_LABELS = {
    "value_en": _("Valeur anglaise"),     "value_ar": _("Valeur arabe"),     "value_fr": _("Valeur française"),     "content_fr": _("Contenu français"),     "subtitle_fr": _("Sous-titre français"),     "partner_type_fr": _("Type français"),     "keywords_fr": _("Mots-clés français"),     "meta_description_fr": _("Meta description français"),     "meta_title_fr": _("Meta title français"),     "instructor_name_en": _("Formateur anglais"),     "instructor_name_ar": _("Formateur arabe"),     "instructor_name_fr": _("Formateur français"),     "location_en": _("Lieu anglais"),     "location_ar": _("Lieu arabe"),     "location_fr": _("Lieu français"),     "body_fr": _("Contenu détaillé français"),     "summary_fr": _("Description courte française"),     "category_fr": _("Catégorie française"),     "title_fr": _("Titre français"),     "title": _("Titre"), "title_ar": _("Titre arabe"), "title_en": _("Titre anglais"), "slug": _("Slug"), "category": _("Catégorie"), "summary": _("Description courte"), "summary_ar": _("Description courte arabe"), "summary_en": _("Description courte anglaise"),
    "body": _("Contenu détaillé"), "image_url": _("Image principale"), "video_url": _("Vidéo"),
    "facebook_url": _("Lien Facebook"), "instagram_url": _("Lien Instagram"), "youtube_url": _("Lien YouTube"),
    "author": _("Auteur / responsable"), "date": _("Date"), "start_date": _("Date de début"),
    "end_date": _("Date de fin"), "start_time": _("Heure de début"), "end_time": _("Heure de fin"),
    "location": _("Lieu"), "instructor_name": _("Formateur"), "total_seats": _("Nombre de places"),
    "registered_seats": _("Places occupées"), "participants": _("Participants"), "reports_count": _("Rapports"),
    "reading_time": _("Temps / note"), "status": _("Statut"), "order": _("Ordre d'affichage"),
    "featured": _("Mettre à la une"), "meta_title": _("Meta title"), "meta_title_ar": _("Meta title arabe"), "meta_title_en": _("Meta title anglais"), "meta_description": _("Meta description"), "meta_description_ar": _("Meta description arabe"), "meta_description_en": _("Meta description anglais"),
    "keywords": _("Mots-clés"), "canonical_url": _("URL canonique"), "og_image_url": _("Image Open Graph"),
    "name": _("Nom"), "name_ar": _("Nom arabe"), "name_en": _("Nom anglais"), "partner_type": _("Type"), "partner_type_ar": _("Type arabe"), "partner_type_en": _("Type anglais"), "url": _("Lien externe"), "logo_url": _("Logo"),
    "description": _("Description"), "description_ar": _("Description arabe"), "description_en": _("Description anglaise"), "featured_home": _("Afficher sur l'accueil"), "subtitle": _("Sous-titre"), "subtitle_ar": _("Sous-titre arabe"), "subtitle_en": _("Sous-titre anglais"),
    "hero_image_url": _("Image de couverture"), "content": _("Contenu de page"), "content_ar": _("Contenu arabe"), "content_en": _("Contenu anglais"), "key": _("Clé"),
    "value": _("Valeur"), "group": _("Groupe"), "sections": _("Sections avancées à propos (JSON)"),
}


ABOUT_SECTIONS_PLACEHOLDER = """{
  "texts": {
    "presentation_title": "À propos de la Fondation Tanger Métropole",
    "mission_label": "Notre raison d'être",
    "mission_title": "Notre mission",
    "mission_button_text": "Découvrir nos programmes",
    "objectives_title": "Nos objectifs",
    "values_title": "Nos valeurs",
    "bureau_title": "Notre bureau dirigeant",
    "bureau_intro": "Une équipe engagée qui œuvre pour la réalisation des objectifs de la Fondation.",
    "members_title": "Liste des membres du bureau dirigeant",
    "members_intro": "Consultez la liste complète des membres de notre bureau dirigeant.",
    "zone_title": "Notre zone d'intervention",
    "zone_name": "Grand Tanger",
    "zone_text": "La Fondation Tanger Métropole intervient principalement dans le Grand Tanger et ses environs.",
    "cta_title": "Construisons ensemble l'avenir du Grand Tanger",
    "cta_text": "Rejoignez nos programmes, devenez bénévole ou contactez-nous.",
    "cta_primary_text": "Devenir bénévole",
    "cta_secondary_text": "Nous contacter"
  },
  "presentation_cards": [
    {"icon": "fa-calendar-alt", "title": "Date de création", "text": "27 mars 2017"},
    {"icon": "fa-eye", "title": "Vision", "text": "Votre texte ici"}
  ],
  "mission_features": ["Formation professionnelle", "Insertion sociale"],
  "objectives": [
    {"icon": "fa-hand-holding-heart", "title": "Solidarité sociale", "text": "Votre texte ici"}
  ],
  "values": [
    {"icon": "fa-flag", "title": "Citoyenneté"}
  ],
  "zone_stats": [
    {"icon": "fa-city", "title": "Tanger Ville"}
  ]
}"""

ABOUT_SECTIONS_HELP = _(
    "Pour la page À propos, ce JSON contrôle les titres de sections, cartes de présentation, "
    "mission, objectifs, valeurs, zone d'intervention et CTA. Les membres du bureau viennent "
    "de la rubrique Équipe."
)


def allow_local_image_paths(form):
    for name in IMAGE_URL_FIELDS:
        if name in form.fields:
            form.fields[name] = forms.CharField(
                label=FIELD_LABELS.get(name, form.fields[name].label),
                required=False,
                widget=forms.TextInput(attrs={
                    "class": "admin-field",
                    "placeholder": "https://... ou /media/...",
                }),
            )


def polish_fields(form):
    allow_local_image_paths(form)
    for name, field in form.fields.items():
        field.label = FIELD_LABELS.get(name, field.label)
        css = "admin-field"
        if isinstance(field.widget, forms.Textarea):
            css += " admin-textarea"
        field.widget.attrs.setdefault("class", css)
        if name.endswith("_url") or name in {"url", "image_url", "logo_url"}:
            field.widget.attrs.setdefault("placeholder", "https://...")
        if name in {"summary", "description", "meta_description"}:
            field.widget.attrs.setdefault("placeholder", _("Texte court et clair pour l'affichage public."))


class ContentItemForm(forms.ModelForm):
    optional_fields = {
        "total_seats", "registered_seats", "participants", "reports_count",
        "reading_time", "order", "date", "start_date", "end_date",
        "start_time", "end_time",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.optional_fields:
            if name in self.fields:
                self.fields[name].required = False
        polish_fields(self)

    class Meta:
        model = ContentItem
        fields = [
            "title", "title_fr", "title_ar", "title_en", "slug", "category", "category_fr", "category_ar", "category_en", "summary", "summary_fr", "summary_ar", "summary_en", "body", "body_fr", "body_ar", "body_en", "image_url", "video_url",
            "facebook_url", "instagram_url", "youtube_url", "author", "date",
            "start_date", "end_date", "start_time", "end_time", "location", "location_fr", "location_ar", "location_en",
            "instructor_name", "instructor_name_fr", "instructor_name_ar", "instructor_name_en", "total_seats", "registered_seats", "participants",
            "reports_count", "reading_time", "status", "order", "featured",
            "meta_title", "meta_title_fr", "meta_title_ar", "meta_title_en", "meta_description", "meta_description_fr", "meta_description_ar", "meta_description_en", "keywords", "keywords_fr", "keywords_ar", "keywords_en", "canonical_url", "og_image_url",
        ]
        widgets = {
            "content_fr": forms.Textarea(attrs={"rows": 3}),
            "subtitle_fr": forms.Textarea(attrs={"rows": 3}),
            "description_fr": forms.Textarea(attrs={"rows": 3}),
            "meta_description_fr": forms.Textarea(attrs={"rows": 3}),
            "body_fr": forms.Textarea(attrs={"rows": 3}),
            "summary_fr": forms.Textarea(attrs={"rows": 3}),
            "date": forms.DateInput(attrs={"type": "date"}),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
            "summary": forms.Textarea(attrs={"rows": 3}),
            "summary_ar": forms.Textarea(attrs={"rows": 3, "dir": "rtl"}),
            "summary_en": forms.Textarea(attrs={"rows": 3}),
            "body": forms.Textarea(attrs={"rows": 8, "data-rich-source": "body"}),
            "body_ar": forms.Textarea(attrs={"rows": 8, "dir": "rtl"}),
            "body_en": forms.Textarea(attrs={"rows": 8}),
            "meta_description": forms.Textarea(attrs={"rows": 3}),
            "meta_description_ar": forms.Textarea(attrs={"rows": 3, "dir": "rtl"}),
            "meta_description_en": forms.Textarea(attrs={"rows": 3}),
        }


class PartnerForm(forms.ModelForm):
    logo_url = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "admin-field"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        polish_fields(self)
        for field_name in self.fields:
            if field_name.endswith(("_fr", "_ar", "_en")):
                self.fields[field_name].required = False

    class Meta:
        model = Partner
        fields = ["name", "name_fr", "name_ar", "name_en", "partner_type", "partner_type_fr", "partner_type_ar", "partner_type_en", "url", "logo_url", "description", "description_fr", "description_ar", "description_en", "order", "status", "featured_home", "start_date", "facebook_url", "instagram_url", "youtube_url", "linkedin_url", "twitter_url", "tiktok_url"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "start_date": forms.DateInput(attrs={"type": "date", "class": "admin-field"}),
        }


class PageContentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        polish_fields(self)
        for field_name in self.fields:
            if field_name.endswith(("_fr", "_ar", "_en")):
                self.fields[field_name].required = False
        if "sections" in self.fields and getattr(self.instance, "slug", "") == "a-propos":
            self.fields["sections"].help_text = ABOUT_SECTIONS_HELP
            self.fields["sections"].widget.attrs["placeholder"] = ABOUT_SECTIONS_PLACEHOLDER
            self.fields["sections"].widget.attrs["spellcheck"] = "false"
            if not self.instance.sections:
                self.initial["sections"] = json.loads(ABOUT_SECTIONS_PLACEHOLDER)

    class Meta:
        model = PageContent
        fields = [
            "title", "title_fr", "title_ar", "title_en", "subtitle", "subtitle_fr", "subtitle_ar", "subtitle_en", "hero_image_url", "content", "content_fr", "content_ar", "content_en", "meta_title", "meta_title_fr", "meta_title_ar", "meta_title_en",
            "meta_description", "meta_description_fr", "meta_description_ar", "meta_description_en", "keywords", "keywords_fr", "keywords_ar", "keywords_en", "canonical_url", "og_image_url", "sections", "status",
        ]
        widgets = {
            "subtitle": forms.Textarea(attrs={"rows": 3}),
            "subtitle_ar": forms.Textarea(attrs={"rows": 3, "dir": "rtl"}),
            "subtitle_en": forms.Textarea(attrs={"rows": 3}),
            "content": forms.Textarea(attrs={"rows": 8}),
            "sections": forms.Textarea(attrs={"rows": 14, "placeholder": '{"presentation_cards": [{"icon": "fa-eye", "title": "Vision", "text": "..."}]}' }),
            "content_ar": forms.Textarea(attrs={"rows": 8, "dir": "rtl"}),
            "content_en": forms.Textarea(attrs={"rows": 8}),
            "meta_description": forms.Textarea(attrs={"rows": 3}),
            "meta_description_ar": forms.Textarea(attrs={"rows": 3, "dir": "rtl"}),
            "meta_description_en": forms.Textarea(attrs={"rows": 3}),
        }


class SiteSettingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        polish_fields(self)

    class Meta:
        model = SiteSetting
        fields = ["key", "value", "value_fr", "value_ar", "value_en", "group"]
        widgets = {"value": forms.Textarea(attrs={"rows": 3})}



class ContactMessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        polish_fields(self)

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message", "status"]
        widgets = {"message": forms.Textarea(attrs={"rows": 6})}


class VolunteerApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        polish_fields(self)

    class Meta:
        model = VolunteerApplication
        fields = ["name", "email", "phone", "city", "skills", "motivation", "status"]
        widgets = {"motivation": forms.Textarea(attrs={"rows": 6})}


class FormationRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        polish_fields(self)

    class Meta:
        model = FormationRegistration
        fields = ["name", "email", "phone", "city", "formation", "status"]


class ActivityRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        polish_fields(self)

    class Meta:
        model = ActivityRegistration
        fields = ["name", "email", "phone", "city", "activity", "status"]

