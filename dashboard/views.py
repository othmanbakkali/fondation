from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.utils import timezone

from core.models import ContentItem, ContactMessage, PageContent, Partner, SiteSetting, VolunteerApplication, FormationRegistration, ActivityRegistration
from .forms import ContentItemForm, PageContentForm, PartnerForm, SiteSettingForm, ContactMessageForm, VolunteerApplicationForm, FormationRegistrationForm, ActivityRegistrationForm
from core.views import ABOUT_TEXT_DEFAULTS, ABOUT_SECTION_DEFAULTS

def _(text):
    return text


def dashboard_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard:home")
    next_url = request.GET.get("next") or request.POST.get("next") or reverse("dashboard:home")
    if request.method == "POST":
        username = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        remember = request.POST.get("remember") == "on"
        user = authenticate(request, username=username, password=password)
        if user is None and "@" in username:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            match = User.objects.filter(email__iexact=username).first()
            if match:
                user = authenticate(request, username=match.get_username(), password=password)
        if user is not None and user.is_active:
            login(request, user)
            request.session.set_expiry(60 * 60 * 24 * 30 if remember else 0)
            return redirect(next_url)
        messages.error(request, _("Email ou mot de passe incorrect."))
    return render(request, "dashboard/login.html", {"next": next_url})


def dashboard_logout(request):
    logout(request)
    messages.success(request, _("Déconnexion effectuée."))
    return redirect("dashboard:login")


MODULES = {
    "program": {"label": _("Programmes"), "singular": _("programme"), "icon": "fa-project-diagram", "url": "program", "columns": [_("Titre"), _("Catégorie"), _("Date"), _("Statut"), _("Ordre")]},
    "activity": {"label": _("Activités"), "singular": _("activité"), "icon": "fa-calendar-alt", "url": "activity", "columns": [_("Titre"), _("Catégorie"), _("Date"), _("Lieu"), _("Statut")]},
    "news": {"label": _("Actualités"), "singular": _("article"), "icon": "fa-newspaper", "url": "news", "columns": [_("Titre"), _("Catégorie"), _("Auteur"), _("Date"), _("Statut")]},
    "formation": {"label": _("Formations"), "singular": _("formation"), "icon": "fa-graduation-cap", "url": "formation", "columns": [_("Titre"), _("Formateur"), _("Date"), _("Places"), _("Statut")]},
    "media": {"label": _("Médias"), "singular": _("média"), "icon": "fa-photo-video", "url": "media", "columns": [_("Titre"), _("Type"), _("Catégorie"), _("Date"), _("Statut")]},
    "volunteer": {"label": _("Bénévolat"), "singular": _("candidature"), "icon": "fa-hands-helping", "url": "volunteer", "columns": [_("Nom"), _("Ville"), _("Compétences"), _("Téléphone"), _("Statut")]},
    "contact": {"label": _("Contact"), "singular": _("message"), "icon": "fa-envelope", "url": "contact", "columns": [_("Nom"), _("Email"), _("Sujet"), _("Date"), _("Statut")]},
    "partner": {"label": _("Partenaires"), "singular": _("partenaire"), "icon": "fa-handshake", "url": "partner", "columns": [_("Nom"), _("Type"), _("Lien"), _("Ordre"), _("Statut")]},
    "team": {"label": _("Équipe"), "singular": _("membre"), "icon": "fa-users", "url": "team", "columns": [_("Nom"), _("Fonction"), _("Email"), _("Ordre"), _("Statut")]},
    "testimonial": {"label": _("Témoignages"), "singular": _("témoignage"), "icon": "fa-quote-right", "url": "testimonial", "columns": [_("Auteur"), _("Profession"), _("Note"), _("Ordre"), _("Statut")]},
    "user": {"label": _("Utilisateurs"), "singular": _("utilisateur"), "icon": "fa-user-shield", "url": "user", "columns": [_("Nom"), _("Rôle"), _("Email"), _("Téléphone"), _("Statut")]},
    "registration": {"label": _("Inscriptions"), "singular": _("inscription"), "icon": "fa-user-check", "url": "registration", "columns": [_("Candidat"), _("Formation"), _("Email"), _("Téléphone"), _("Statut")]},
    "activity_registration": {"label": _("Inscriptions Activités"), "singular": _("inscription activité"), "icon": "fa-calendar-check", "url": "activity_registration", "columns": [_("Candidat"), _("Activité"), _("Email"), _("Téléphone"), _("Statut")]},
}


IMAGE_UPLOAD_FIELDS = ("image_url", "logo_url", "hero_image_url", "og_image_url")


def save_uploaded_dashboard_image(uploaded_file, folder="dashboard"):
    if not uploaded_file:
        return ""
    path = default_storage.save(f"{folder}/{uploaded_file.name}", uploaded_file)
    return default_storage.url(path)


def apply_uploaded_image_fields(instance, files, folder="dashboard"):
    for field_name in IMAGE_UPLOAD_FIELDS:
        if hasattr(instance, field_name):
            uploaded_url = save_uploaded_dashboard_image(files.get(f"{field_name}_upload"), folder)
            if uploaded_url:
                setattr(instance, field_name, uploaded_url)


def save_uploaded_announcement_image(uploaded_file):
    return save_uploaded_dashboard_image(uploaded_file, "announcements")


CONTENT_ITEM_TEXT_FIELDS = (
    "title", "title_fr", "title_ar", "title_en", "slug", "category", "category_fr", "category_ar", "category_en", "summary", "summary_fr", "summary_ar", "summary_en", "body", "body_fr", "body_ar", "body_en", "image_url", "video_url",
    "facebook_url", "instagram_url", "youtube_url", "linkedin_url", "twitter_url", "tiktok_url", "author", "location",
    "instructor_name", "instructor_name_fr", "instructor_name_ar", "instructor_name_en", "location_fr", "location_ar", "location_en", "meta_title", "meta_title_fr", "meta_title_ar", "meta_title_en", "meta_description", "meta_description_fr", "meta_description_ar", "meta_description_en", "keywords", "keywords_fr", "keywords_ar", "keywords_en",
    "canonical_url", "og_image_url",
)
CONTENT_ITEM_INT_FIELDS = (
    "total_seats", "registered_seats", "participants", "reports_count",
    "reading_time", "order",
)
CONTENT_ITEM_DATE_FIELDS = ("date", "start_date", "end_date")
CONTENT_ITEM_TIME_FIELDS = ("start_time", "end_time")


def assign_content_item_from_request(item, request, module_key):
    for field_name in CONTENT_ITEM_TEXT_FIELDS:
        if field_name in request.POST:
            setattr(item, field_name, request.POST.get(field_name, ""))
    for field_name in CONTENT_ITEM_INT_FIELDS:
        value = request.POST.get(field_name)
        setattr(item, field_name, int(value) if value not in (None, "") else 0)
    for field_name in CONTENT_ITEM_DATE_FIELDS + CONTENT_ITEM_TIME_FIELDS:
        value = request.POST.get(field_name)
        setattr(item, field_name, value or None)
    if "status" in request.POST:
        item.status = request.POST.get("status") or item.status
    item.featured = request.POST.get("featured") == "on"
    item.module = module_key
    apply_uploaded_image_fields(item, request.FILES, module_key)
    return item


def common_context(title):
    return {"page_title": title}


def item_rows(module_key, items):
    rows = []
    for item in items:
        if module_key == "formation":
            rows.append([item.title, item.instructor_name or item.author, item.start_date or item.date or "-", f"{item.registered_seats}/{item.total_seats}", item.status])
        elif module_key == "activity":
            rows.append([item.title, item.category, item.date or "-", item.location, item.status])
        elif module_key == "news":
            rows.append([item.title, item.category, item.author, item.date or "-", item.status])
        elif module_key in ("team", "user"):
            rows.append([item.title, item.category, item.author or item.location, item.order, item.status])
        elif module_key == "testimonial":
            rows.append([item.title, item.category, f"{item.reading_time}/5", item.order, item.status])
        else:
            rows.append([item.title, item.category, item.date or "-", item.status, item.order])
    return rows


def dashboard(request):
    from django.db.models import Count
    from django.utils import timezone
    
    # Calculate real registrations stats
    pending_regs = FormationRegistration.objects.filter(status="en_attente").count() + ActivityRegistration.objects.filter(status="en_attente").count()
    total_regs = FormationRegistration.objects.count() + ActivityRegistration.objects.count()
    
    stats = [
        {"label": _("Activités"), "value": ContentItem.objects.filter(module="activity").count(), "icon": "fa-calendar-alt", "color": "#3B82F6", "change": _("dans la base")},
        {"label": _("Actualités"), "value": ContentItem.objects.filter(module="news").count(), "icon": "fa-newspaper", "color": "#10B981", "change": _("publiées")},
        {"label": _("Formations"), "value": ContentItem.objects.filter(module="formation").count(), "icon": "fa-graduation-cap", "color": "#7C3AED", "change": _("sessions")},
        {"label": _("Bénévoles"), "value": VolunteerApplication.objects.count(), "icon": "fa-hands-helping", "color": "#D9A441", "change": _("candidatures")},
        {"label": _("Partenaires"), "value": Partner.objects.count(), "icon": "fa-handshake", "color": "#14B8A6", "change": _("partenaires")},
        {"label": _("Messages"), "value": ContactMessage.objects.count(), "icon": "fa-comments", "color": "#EF4444", "change": _("messages reçus")},
        {"label": _("Inscriptions"), "value": total_regs, "icon": "fa-clipboard-list", "color": "#0B5EA8", "change": _("%(count)s en attente") % {"count": pending_regs}},
        {"label": _("Médias"), "value": ContentItem.objects.filter(module="media").count(), "icon": "fa-photo-video", "color": "#6366F1", "change": _("dans la galerie")},
    ]
    
    # Monthly activity counts for current year (real database records across all tables)
    current_year = timezone.now().year
    monthly_counts = []
    for month_num in range(1, 13):
        item_cnt = ContentItem.objects.filter(created_at__year=current_year, created_at__month=month_num).count()
        reg_cnt = FormationRegistration.objects.filter(created_at__year=current_year, created_at__month=month_num).count() + ActivityRegistration.objects.filter(created_at__year=current_year, created_at__month=month_num).count()
        msg_cnt = ContactMessage.objects.filter(created_at__year=current_year, created_at__month=month_num).count()
        vol_cnt = VolunteerApplication.objects.filter(created_at__year=current_year, created_at__month=month_num).count()
        partner_cnt = Partner.objects.filter(created_at__year=current_year, created_at__month=month_num).count()
        monthly_counts.append(item_cnt + reg_cnt + msg_cnt + vol_cnt + partner_cnt)
        
    months_labels = [_("Jan"), _("Fév"), _("Mar"), _("Avr"), _("Mai"), _("Juin"), _("Juil"), _("Août"), _("Sep"), _("Oct"), _("Nov"), _("Déc")]
    monthly_activity = []
    max_count = max(monthly_counts) or 1
    for i in range(12):
        raw_val = monthly_counts[i]
        percentage_val = int(round(raw_val / max_count * 90)) if raw_val > 0 else 0
        monthly_activity.append({
            "month": months_labels[i],
            "value": raw_val,
            "height": percentage_val
        })
        
    # Categories statistics (using both activity and program items to have real initial values from the database!)
    total_activities = ContentItem.objects.filter(module__in=["activity", "program"]).count()
    categories_stats = {
        "education": ContentItem.objects.filter(module__in=["activity", "program"], category__icontains="educ").count() + ContentItem.objects.filter(module__in=["activity", "program"], category__icontains="éduc").count(),
        "social": ContentItem.objects.filter(module__in=["activity", "program"], category__icontains="social").count(),
        "culture": ContentItem.objects.filter(module__in=["activity", "program"], category__icontains="cult").count(),
        "sport": ContentItem.objects.filter(module__in=["activity", "program"], category__icontains="sport").count(),
    }
    if total_activities > 0:
        pct_edu = int(round(categories_stats["education"] / total_activities * 100))
        pct_soc = int(round(categories_stats["social"] / total_activities * 100))
        pct_cul = int(round(categories_stats["culture"] / total_activities * 100))
        pct_spo = max(0, 100 - (pct_edu + pct_soc + pct_cul))
    else:
        pct_edu, pct_soc, pct_cul, pct_spo = 25, 25, 25, 25
        
    seg1 = pct_edu
    seg2 = seg1 + pct_soc
    seg3 = seg2 + pct_cul
    donut_gradient = f"conic-gradient(#3B82F6 0% {seg1}%, #10B981 {seg1}% {seg2}%, #D9A441 {seg2}% {seg3}%, #EF4444 {seg3}% 100%)"
    
    pending = ContentItem.objects.exclude(status="publie")[:6]
    context = common_context(_("Tableau de bord"))
    context.update({
        "stats": stats,
        "monthly_activity": monthly_activity,
        "categories_percentages": {"education": pct_edu, "social": pct_soc, "culture": pct_cul, "sport": pct_spo},
        "donut_gradient": donut_gradient,
        "quick_actions": [
            {"label": _("Ajouter activité"), "icon": "fa-calendar-plus", "url": reverse("dashboard:activity_add")},
            {"label": _("Publier actualité"), "icon": "fa-newspaper", "url": reverse("dashboard:news_add")},
            {"label": _("Créer formation"), "icon": "fa-graduation-cap", "url": reverse("dashboard:formation_add")},
            {"label": _("Voir messages"), "icon": "fa-envelope", "url": reverse("dashboard:contact_messages")},
        ],
        "volunteers": [[v.name, v.city, v.skills, v.phone, v.status] for v in VolunteerApplication.objects.all()[:5]],
        "messages": [[m.name, m.email, m.subject, m.created_at.strftime("%d/%m/%Y"), m.status] for m in ContactMessage.objects.all()[:5]],
        "pending_columns": [_("Titre"), _("Module"), _("Date"), _("Statut")],
        "pending": [[p.title, p.get_module_display(), p.updated_at.strftime("%d/%m/%Y"), p.status] for p in pending],
    })
    return render(request, "dashboard/dashboard.html", context)


def dashboard_notification_counts(request):
    unread_messages = ContactMessage.objects.filter(status="non_lu").count()
    pending_volunteers = VolunteerApplication.objects.filter(status="en_attente").count()
    pending_content = ContentItem.objects.filter(status__in=["brouillon", "programme", "en_attente"]).count()
    pending_formations_regs = FormationRegistration.objects.filter(status="en_attente").count()
    pending_activities_regs = ActivityRegistration.objects.filter(status="en_attente").count()
    return JsonResponse({
        "total": (
            unread_messages 
            + pending_volunteers 
            + pending_content 
            + pending_formations_regs 
            + pending_activities_regs
        ),
        "messages": unread_messages,
        "volunteers": pending_volunteers,
        "content": pending_content,
        "formations_registrations": pending_formations_regs,
        "activities_registrations": pending_activities_regs,
    })


def home_page_management(request):
    from core.views import HOME_TEXT_DEFAULTS
    from django.db.models import Sum
    
    home_page = PageContent.objects.filter(slug="accueil").first()
    
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "update_hero":
            home_page.title_fr = request.POST.get("title", home_page.title_fr or home_page.title)
            home_page.title = home_page.title_fr
            home_page.title_ar = request.POST.get("title_ar", home_page.title_ar)
            home_page.title_en = request.POST.get("title_en", home_page.title_en)
            
            home_page.subtitle_fr = request.POST.get("subtitle", home_page.subtitle_fr or home_page.subtitle)
            home_page.subtitle = home_page.subtitle_fr
            home_page.subtitle_ar = request.POST.get("subtitle_ar", home_page.subtitle_ar)
            home_page.subtitle_en = request.POST.get("subtitle_en", home_page.subtitle_en)
            
            # Handle sections texts (buttons, scroll)
            sections = dict(home_page.sections or {})
            if "texts" not in sections or not isinstance(sections["texts"], dict):
                sections["texts"] = {}
            texts = sections["texts"]
            
            for key in ["hero_btn1", "hero_btn2", "hero_scroll", "hero_btn1_ar", "hero_btn2_ar", "hero_scroll_ar", "hero_btn1_en", "hero_btn2_en", "hero_scroll_en"]:
                if key in request.POST:
                    texts[key] = request.POST.get(key)
            home_page.sections = sections
            
            # Handle image
            hero_image_upload = save_uploaded_dashboard_image(request.FILES.get("hero_image_upload"), "pages")
            if hero_image_upload:
                home_page.hero_image_url = hero_image_upload
            elif "hero_image_url" in request.POST:
                home_page.hero_image_url = request.POST.get("hero_image_url")
                
            home_page.save()
            messages.success(request, _("Hero section mise à jour."))
            
        elif action == "update_stats":
            years = request.POST.get("stats_annees")
            if years is not None:
                SiteSetting.objects.update_or_create(key="stats_annees", defaults={"value": str(years)})
            messages.success(request, _("Statistiques mises à jour."))
            
        elif action == "update_seo":
            home_page.meta_title = request.POST.get("meta_title", home_page.meta_title)
            home_page.meta_title_fr = request.POST.get("meta_title_fr", home_page.meta_title_fr)
            home_page.meta_title_ar = request.POST.get("meta_title_ar", home_page.meta_title_ar)
            home_page.meta_title_en = request.POST.get("meta_title_en", home_page.meta_title_en)
            home_page.meta_description = request.POST.get("meta_description", home_page.meta_description)
            home_page.meta_description_fr = request.POST.get("meta_description_fr", home_page.meta_description_fr)
            home_page.meta_description_ar = request.POST.get("meta_description_ar", home_page.meta_description_ar)
            home_page.meta_description_en = request.POST.get("meta_description_en", home_page.meta_description_en)
            home_page.keywords = request.POST.get("keywords", home_page.keywords)
            home_page.keywords_fr = request.POST.get("keywords_fr", home_page.keywords_fr)
            home_page.keywords_ar = request.POST.get("keywords_ar", home_page.keywords_ar)
            home_page.keywords_en = request.POST.get("keywords_en", home_page.keywords_en)
            home_page.canonical_url = request.POST.get("canonical_url", home_page.canonical_url)
            
            og_image_upload = save_uploaded_dashboard_image(request.FILES.get("og_image_url_upload"), "pages")
            if og_image_upload:
                home_page.og_image_url = og_image_upload
            elif "og_image_url" in request.POST:
                home_page.og_image_url = request.POST.get("og_image_url")
                
            home_page.save()
            messages.success(request, _("Paramètres SEO mis à jour."))
            
        return redirect("dashboard:home_page")

    announcements = ContentItem.objects.filter(module="news").order_by("order", "-date")[:8]
    partners = Partner.objects.all()[:12]
    
    # Load all texts from sections['texts']
    sections_dict = getattr(home_page, "sections", None) or {}
    texts_dict = sections_dict.get("texts", {}) if isinstance(sections_dict, dict) else {}
    home_texts = {}
    for key in HOME_TEXT_DEFAULTS:
        home_texts[key] = texts_dict.get(key) or HOME_TEXT_DEFAULTS.get(key, "")
        home_texts[f"{key}_ar"] = texts_dict.get(f"{key}_ar") or ""
        home_texts[f"{key}_en"] = texts_dict.get(f"{key}_en") or ""
        
    # Calculate real-time stats
    beneficiaries_count = ContentItem.objects.filter(module="activity", status="publie").aggregate(total=Sum("participants"))["total"] or 0
    volunteers_count = VolunteerApplication.objects.filter(status__in=["accepte", "actif"]).count()
    years_count = SiteSetting.objects.filter(key="stats_annees").values_list("value", flat=True).first() or 0
    
    context = common_context(_("Gestion de la page d'accueil"))
    context.update({
        "home_page": home_page,
        "home_texts": home_texts,
        "home_announcements": announcements,
        "home_partners": partners,
        "beneficiaries_count": beneficiaries_count,
        "programs_count": ContentItem.objects.filter(module="program").exclude(status__in=["brouillon", "archive", "inactif"]).count(),
        "formations_count": ContentItem.objects.filter(module="formation").exclude(status__in=["brouillon", "archive", "inactif"]).count(),
        "partners_count": Partner.objects.filter(status="actif").count(),
        "volunteers_count": volunteers_count,
        "years_count": years_count,
        "home_domains": ContentItem.objects.filter(module="program")[:4],
        "activity_columns": MODULES["activity"]["columns"],
    })
    
    # Prepare activity table items
    activities_qs = ContentItem.objects.filter(module="activity")[:6]
    activity_table_items = []
    for obj in activities_qs:
        row = [obj.title, obj.category, obj.date or "-", obj.location, obj.status]
        activity_table_items.append({
            "object": obj,
            "cells": row,
            "detail_url": reverse("dashboard:activity_detail", args=[obj.pk]),
            "edit_url": reverse("dashboard:activity_edit", args=[obj.pk]),
            "duplicate_url": reverse("dashboard:module_duplicate", args=["activity", obj.pk]),
            "delete_url": reverse("dashboard:module_delete", args=["activity", obj.pk]),
            "image": obj.image_url or "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=120&h=80&fit=crop&auto=format",
            "read_only": False,
            "is_registration": False,
        })
    context["activity_table_items"] = activity_table_items
    return render(request, "dashboard/pages/home_page.html", context)



def home_announcement_update(request, pk):
    item = get_object_or_404(ContentItem, pk=pk, module="news")
    if request.method == "POST":
        item.title = request.POST.get("title", item.title)
        item.category = request.POST.get("category", item.category)
        item.summary = request.POST.get("summary", item.summary)
        item.body = request.POST.get("body", item.body or item.summary)
        uploaded_image_url = save_uploaded_announcement_image(request.FILES.get("image_upload") or request.FILES.get("image_url_upload"))
        item.image_url = uploaded_image_url or request.POST.get("image_url", item.image_url)
        item.status = request.POST.get("status", item.status)
        item.order = request.POST.get("order") or item.order
        if request.POST.get("date"):
            item.date = request.POST.get("date")
        item.save()
        messages.success(request, _("Annonce modifiée avec succès."))
    return redirect("dashboard:home_page")


def site_content(request):
    pages = PageContent.objects.all()
    context = common_context(_("Contenu du site"))
    context["managed_pages"] = pages
    return render(request, "dashboard/pages/site_content.html", context)



ABOUT_TEXT_FIELD_LABELS = {
    "presentation_title": "Titre de la section présentation",
    "mission_label": "Petit label mission",
    "mission_title": "Titre mission",
    "mission_button_text": "Texte bouton mission",
    "objectives_title": "Titre objectifs",
    "values_title": "Titre valeurs",
    "bureau_title": "Titre bureau dirigeant",
    "bureau_intro": "Introduction bureau dirigeant",
    "members_title": "Titre liste des membres",
    "members_intro": "Introduction liste des membres",
    "members_search_placeholder": "Placeholder recherche membres",
    "members_filter_all": "Texte filtre toutes les fonctions",
    "members_export": "Texte bouton export",
    "members_empty_title": "Titre aucun résultat",
    "members_empty_text": "Texte aucun résultat",
    "zone_title": "Titre zone d'intervention",
    "zone_name": "Nom de la zone",
    "zone_text": "Texte zone d'intervention",
    "cta_title": "Titre appel à l'action",
    "cta_text": "Texte appel à l'action",
    "cta_primary_text": "Texte bouton bénévolat",
    "cta_secondary_text": "Texte bouton contact",
}


def about_section_for_dashboard(sections, key):
    if isinstance(sections, dict):
        value = sections.get(key)
        if value not in (None, "", []):
            return value
    if isinstance(sections, list):
        for section in sections:
            if isinstance(section, dict) and section.get("key") == key:
                value = section.get("items", section.get("value", section.get("text")))
                if value not in (None, "", []):
                    return value
    return ABOUT_SECTION_DEFAULTS.get(key, [])


def about_text_for_dashboard(sections, key):
    default = ABOUT_TEXT_DEFAULTS.get(key, "")
    if isinstance(sections, dict):
        texts = sections.get("texts")
        if isinstance(texts, dict) and texts.get(key) not in (None, ""):
            return texts.get(key)
        if sections.get(key) not in (None, ""):
            return sections.get(key)
    if isinstance(sections, list):
        for section in sections:
            if isinstance(section, dict) and section.get("key") == "texts":
                value = section.get("items", section.get("value", {}))
                if isinstance(value, dict) and value.get(key) not in (None, ""):
                    return value.get(key)
    return default


def about_items_from_post(post, prefix, fields):
    values = {field: post.getlist(f"{prefix}_{field}") for field in fields}
    length = max([len(items) for items in values.values()] or [0])
    rows = []
    for index in range(length):
        row = {}
        has_content = False
        for field in fields:
            value = values[field][index].strip() if index < len(values[field]) else ""
            row[field] = value
            if field != "icon" and value:
                has_content = True
        if has_content:
            rows.append(row)
    return rows


def about_simple_list_from_post(post, name):
    return [value.strip() for value in post.getlist(name) if value.strip()]


def about_editor_context(page):
    from core.views import ABOUT_TEXT_DEFAULTS
    sections = page.sections or {}
    texts = sections.get("texts") if isinstance(sections, dict) else {}
    if not isinstance(texts, dict):
        texts = {}

    text_fields = []
    for key in ABOUT_TEXT_DEFAULTS:
        label = ABOUT_TEXT_FIELD_LABELS.get(key, key)
        val_fr = texts.get(key, about_text_for_dashboard(sections, key))
        val_ar = texts.get(f"{key}_ar", "")
        val_en = texts.get(f"{key}_en", "")
        text_fields.append({
            "key": key,
            "label": label,
            "value": val_fr,
            "value_ar": val_ar,
            "value_en": val_en,
        })

    features_raw = about_section_for_dashboard(sections, "mission_features")
    features_list = []
    for item in features_raw:
        if isinstance(item, dict):
            features_list.append(item)
        elif isinstance(item, str):
            features_list.append({"feature": item, "feature_ar": "", "feature_en": ""})

    return {
        "about_text_fields": text_fields,
        "about_presentation_cards": about_section_for_dashboard(sections, "presentation_cards"),
        "about_mission_features": features_list,
        "about_objectives": about_section_for_dashboard(sections, "objectives"),
        "about_values": about_section_for_dashboard(sections, "values"),
        "about_zone_stats": about_section_for_dashboard(sections, "zone_stats"),
    }


def about_sections_from_request(post):
    texts = {}
    for key, value in post.items():
        if key.startswith("about_text_"):
            clean_key = key.replace("about_text_", "", 1)
            texts[clean_key] = value.strip()
    return {
        "texts": texts,
        "presentation_cards": about_items_from_post(post, "about_card", ("icon", "title", "title_ar", "title_en", "text", "text_ar", "text_en")),
        "mission_features": about_items_from_post(post, "about_mission", ("feature", "feature_ar", "feature_en")),
        "objectives": about_items_from_post(post, "about_objective", ("icon", "title", "title_ar", "title_en", "text", "text_ar", "text_en")),
        "values": about_items_from_post(post, "about_value", ("icon", "title", "title_ar", "title_en")),
        "zone_stats": about_items_from_post(post, "about_zone_stat", ("icon", "title", "title_ar", "title_en")),
    }


HOME_TEXT_FIELD_LABELS = {
    "hero_btn1": "Bouton 1 du Hero (Découvrir la Fondation)",
    "hero_btn2": "Bouton 2 du Hero (Devenir Bénévole)",
    "hero_scroll": "Texte indicateur de défilement (Défiler)",
    "annonces_title": "Titre section Actualités & Annonces",
    "stats_beneficiaries_label": "Titre Statistique 1 (Bénéficiaires)",
    "stats_beneficiaries_sub": "Sous-titre Statistique 1 (directs et indirects)",
    "stats_programs_label": "Titre Statistique 2 (Programmes)",
    "stats_programs_sub": "Sous-titre Statistique 2 (publiés)",
    "stats_formations_label": "Titre Statistique 3 (Formations)",
    "stats_formations_sub": "Sous-titre Statistique 3 (publiées)",
    "stats_partners_label": "Titre Statistique 4 (Partenaires)",
    "stats_partners_sub": "Sous-titre Statistique 4 (actifs)",
    "stats_volunteers_label": "Titre Statistique 5 (Bénévoles)",
    "stats_volunteers_sub": "Sous-titre Statistique 5 (candidatures)",
    "stats_years_label": "Titre Statistique 6 (Années)",
    "stats_years_sub": "Sous-titre Statistique 6 (d'expérience)",
    "domains_title": "Titre section Nos Domaines d'Intervention",
    "domains_btn": "Bouton carte domaine (Découvrir)",
    "activities_title": "Titre section Activités de la Fondation",
    "activities_btn": "Bouton voir toutes les activités",
    "partners_title": "Titre section Nos Partenaires",
    "benevolat_title": "Titre section Devenir Bénévole",
    "benevolat_text": "Texte introduction bénévolat",
    "benevolat_point1": "Point 1 bénévolat",
    "benevolat_point2": "Point 2 bénévolat",
    "benevolat_point3": "Point 3 bénévolat",
    "benevolat_btn": "Bouton S'inscrire maintenant",
    "contact_title": "Titre section Contactez-nous",
    "contact_name_ph": "Placeholder Nom complet",
    "contact_email_ph": "Placeholder Email",
    "contact_msg_ph": "Placeholder Votre message",
    "contact_btn": "Bouton Envoyer message",
}

HOME_TEXT_DEFAULTS = {
    "hero_btn1": "Découvrir la Fondation",
    "hero_btn2": "Devenir Bénévole",
    "hero_scroll": "Défiler",
    "annonces_title": "Actualités & Annonces",
    "stats_beneficiaries_label": "Bénéficiaires",
    "stats_beneficiaries_sub": "directs et indirects",
    "stats_programs_label": "Programmes",
    "stats_programs_sub": "publiés",
    "stats_formations_label": "Formations",
    "stats_formations_sub": "publiées",
    "stats_partners_label": "Partenaires",
    "stats_partners_sub": "actifs",
    "stats_volunteers_label": "Bénévoles",
    "stats_volunteers_sub": "candidatures",
    "stats_years_label": "Années",
    "stats_years_sub": "d'expérience",
    "domains_title": "Nos Domaines d'Intervention",
    "domains_btn": "Découvrir",
    "activities_title": "Activités de la Fondation",
    "activities_btn": "Voir toutes les activités",
    "partners_title": "Nos Partenaires",
    "benevolat_title": "Devenir Bénévole",
    "benevolat_text": "Rejoignez une communauté dynamique qui transforme Tanger. Chaque geste compte pour construire un avenir meilleur.",
    "benevolat_point1": "Missions flexibles adaptées à votre disponibilité",
    "benevolat_point2": "Formations offertes pour développer vos compétences",
    "benevolat_point3": "Impact mesurable sur la communauté",
    "benevolat_btn": "S'inscrire maintenant",
    "contact_title": "Contactez-nous",
    "contact_name_ph": "Nom complet",
    "contact_email_ph": "Email",
    "contact_msg_ph": "Votre message",
    "contact_btn": "Envoyer",
}


def home_editor_context(page):
    sections = page.sections or {}
    texts = sections.get("texts") if isinstance(sections, dict) else {}
    if not isinstance(texts, dict):
        texts = {}

    text_fields = []
    for key in HOME_TEXT_DEFAULTS:
        label = HOME_TEXT_FIELD_LABELS.get(key, key)
        val_fr = texts.get(key, HOME_TEXT_DEFAULTS.get(key, ""))
        val_ar = texts.get(f"{key}_ar", "")
        val_en = texts.get(f"{key}_en", "")
        text_fields.append({
            "key": key,
            "label": label,
            "value": val_fr,
            "value_ar": val_ar,
            "value_en": val_en,
        })
    return {"home_text_fields": text_fields}


def home_sections_from_request(post):
    texts = {}
    for key, value in post.items():
        if key.startswith("home_text_"):
            clean_key = key.replace("home_text_", "", 1)
            texts[clean_key] = value.strip()
    return {"texts": texts}


def page_edit(request, slug):
    page = get_object_or_404(PageContent, slug=slug)

    if request.method == "POST" and slug in ("a-propos", "accueil", "benevolat"):
        page_fields = [
            "title", "title_fr", "title_ar", "title_en",
            "subtitle", "subtitle_fr", "subtitle_ar", "subtitle_en",
            "content", "content_fr", "content_ar", "content_en",
            "meta_title", "meta_title_fr", "meta_title_ar", "meta_title_en",
            "meta_description", "meta_description_fr", "meta_description_ar", "meta_description_en",
            "keywords", "keywords_fr", "keywords_ar", "keywords_en",
            "canonical_url", "og_image_url", "status",
        ]
        for field_name in page_fields:
            if field_name in request.POST:
                setattr(page, field_name, request.POST.get(field_name, ""))

        if slug == "a-propos":
            page.sections = about_sections_from_request(request.POST)
            mission_image_link = request.POST.get("about_mission_image_url", "").strip()
            mission_image_upload = save_uploaded_dashboard_image(request.FILES.get("about_mission_image_upload"), "pages")
            if mission_image_upload or mission_image_link:
                page.hero_image_url = mission_image_upload or mission_image_link
        elif slug == "accueil":
            page.sections = home_sections_from_request(request.POST)
        elif slug == "benevolat":
            faqs = []
            for i in range(3):
                faqs.append({
                    "q": request.POST.get(f"faq_q_{i}", "").strip(),
                    "r": request.POST.get(f"faq_r_{i}", "").strip(),
                    "q_ar": request.POST.get(f"faq_q_{i}_ar", "").strip(),
                    "r_ar": request.POST.get(f"faq_r_{i}_ar", "").strip(),
                    "q_en": request.POST.get(f"faq_q_{i}_en", "").strip(),
                    "r_en": request.POST.get(f"faq_r_{i}_en", "").strip(),
                })
            page.sections = faqs

        og_image_upload = save_uploaded_dashboard_image(request.FILES.get("og_image_url_upload"), "pages")
        if og_image_upload:
            page.og_image_url = og_image_upload

        page.save()
        messages.success(request, _("Page modifiée avec succès."))
        return redirect("dashboard:page_edit", slug=slug)

    form = PageContentForm(request.POST or None, request.FILES or None, instance=page)
    if request.method == "POST" and form.is_valid():
        saved = form.save(commit=False)
        apply_uploaded_image_fields(saved, request.FILES, "pages")
        saved.save()
        messages.success(request, _("Page modifiée avec succès."))
        return redirect("dashboard:site_content")

    context = {
        "page_title": _("Modifier %(title)s") % {"title": page.title},
        "form": form,
        "page": page,
        "about_mission_image_url": page.hero_image_url if slug == "a-propos" else "",
    }
    if slug == "a-propos":
        context.update(about_editor_context(page))
    elif slug == "accueil":
        context.update(home_editor_context(page))
    elif slug == "benevolat":
        faqs = page.sections
        if not faqs or not isinstance(faqs, list):
            faqs = [
                {
                    "q": "Comment puis-je devenir bénévole ?",
                    "r": "Pour devenir bénévole, il vous suffit de remplir le formulaire de candidature sur cette page. Notre équipe vous contactera dès qu'une mission correspondant à votre profil sera disponible.",
                    "q_ar": "كيف يمكنني أن أصبح متطوعًا؟",
                    "r_ar": "للقيام بذلك، ما عليك سوى ملء استمارة التقديم على هذه الصفحة. سيتصل بك فريقنا بمجرد توفر مهمة تناسب مؤهلاتك.",
                    "q_en": "How can I become a volunteer?",
                    "r_en": "To become a volunteer, simply fill out the application form on this page. Our team will contact you as soon as a mission corresponding to your profile is available."
                },
                {
                    "q": "Quelles sont les conditions pour être bénévole ?",
                    "r": "Il n'y a pas de conditions particulières. Tout le monde peut s'engager selon ses compétences, ses centres d'intérêt et ses disponibilités.",
                    "q_ar": "ما هي شروط التطوع؟",
                    "r_ar": "لا توجد شروط خاصة. يمكن للجميع المشاركة والمساهمة وفقًا لمهاراتهم واهتماماتهم وأوقات فارغهم.",
                    "q_en": "What are the conditions to be a volunteer?",
                    "r_en": "There are no special conditions. Everyone can get involved according to their skills, interests, and availability."
                },
                {
                    "q": "Combien de temps dois-je consacrer au bénévolat ?",
                    "r": "L'engagement est flexible. Vous pouvez choisir vos créneaux en fonction de votre emploi du temps (en semaine, le week-end, ponctuellement ou régulièrement).",
                    "q_ar": "كم من الوقت يجب أن أخصصه للتطوع؟",
                    "r_ar": "الالتزام مرن للغاية. يمكنك اختيار الفترات التي تناسب جدولك الزمني (خلال الأسبوع، في عطلة نهاية الأسبوع، أو بشكل دوري).",
                    "q_en": "How much time do I need to devote to volunteering?",
                    "r_en": "Commitment is flexible. You can choose your slots according to your schedule (weekdays, weekends, occasionally, or regularly)."
                }
            ]
        context["benevolat_faq_fields"] = faqs
    return render(request, "dashboard/pages/page_form.html", context)


def about_list(request):
    from django.db.models import Sum
    page_content = PageContent.objects.filter(slug="a-propos").first()
    
    # Extract presentation title and description
    sections = page_content.sections if page_content else {}
    presentation_title = about_text_for_dashboard(sections, "presentation_title") or _("Présentation de la Fondation")
    presentation_text = page_content.content if page_content else _("La Fondation Tanger Métropole accompagne les jeunes, les femmes et les acteurs associatifs du Grand Tanger...")
    
    # Extract values
    raw_values = about_section_for_dashboard(sections, "values")
    values_list = []
    for item in raw_values:
        if isinstance(item, dict) and item.get("title"):
            values_list.append(item.get("title"))
        elif isinstance(item, str):
            values_list.append(item)
            
    # Calculate real key figures
    beneficiaries_count = ContentItem.objects.filter(module="activity", status="publie").aggregate(total=Sum("participants"))["total"] or 0
    partners_count = Partner.objects.filter(status="actif").count()
    
    # Prepare team table items
    team_items = ContentItem.objects.filter(module="team").order_by("order", "created_at")
    team_table_items = []
    for obj in team_items:
        row = [obj.title, obj.category, obj.author or obj.location, obj.order, obj.status]
        team_table_items.append({
            "object": obj,
            "cells": row,
            "detail_url": reverse("dashboard:team_detail", args=[obj.pk]),
            "edit_url": reverse("dashboard:team_edit", args=[obj.pk]),
            "duplicate_url": reverse("dashboard:module_duplicate", args=["team", obj.pk]),
            "delete_url": reverse("dashboard:module_delete", args=["team", obj.pk]),
            "image": obj.image_url or "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=120&h=80&fit=crop&auto=format",
            "read_only": False,
            "is_registration": False,
        })
        
    context = common_context(_("À propos"))
    context.update({
        "page_content": page_content,
        "presentation_title": presentation_title,
        "presentation_text": presentation_text,
        "values": values_list,
        "beneficiaries_count": beneficiaries_count,
        "partners_count": partners_count,
        "team_columns": MODULES["team"]["columns"],
        "team_table_items": team_table_items,
    })
    return render(request, "dashboard/pages/about.html", context)


def about_edit(request):
    return page_edit(request, "a-propos")


def module_list(request, key):
    module = MODULES[key]
    qs = ContentItem.objects.filter(module=key)
    if key == "team":
        qs = qs.order_by("order", "created_at")
    rows = item_rows(key, qs)
    objects = list(qs)
    if key == "partner":
        objects = list(Partner.objects.all())
        rows = [[p.name, p.partner_type, p.url, p.order, p.status] for p in objects]
    elif key == "contact":
        objects = list(ContactMessage.objects.all())
        rows = [[m.name, m.email, m.subject, m.created_at.strftime("%d/%m/%Y"), m.status] for m in objects]
    elif key == "volunteer":
        objects = list(VolunteerApplication.objects.all())
        rows = [[v.name, v.city, v.skills, v.phone, v.status] for v in objects]
    elif key == "registration":
        objects = list(FormationRegistration.objects.all())
        rows = [[r.name, r.formation.title if r.formation else "-", r.email, r.phone, r.status] for r in objects]
    elif key == "activity_registration":
        objects = list(ActivityRegistration.objects.all())
        rows = [[r.name, r.activity.title if r.activity else "-", r.email, r.phone, r.status] for r in objects]
    elif key == "user":
        from django.contrib.auth.models import User
        objects = list(User.objects.all().order_by("-id"))
        rows = []
        for u in objects:
            role = _("Administrateur") if u.is_staff or u.is_superuser else _("Utilisateur")
            phone = u.profile.phone if hasattr(u, "profile") else "-"
            status = _("Actif") if u.is_active else _("Inactif")
            name = f"{u.last_name} {u.first_name}".strip() or u.username
            rows.append([name, role, u.email or "-", phone, status])
    table_items = []
    for obj, row in zip(objects, rows):
        table_items.append({
            "object": obj,
            "cells": row,
            "detail_url": reverse(f"dashboard:{module['url']}_detail", args=[obj.pk]),
            "edit_url": reverse(f"dashboard:{module['url']}_edit", args=[obj.pk]),
            "duplicate_url": "" if key == "user" else reverse("dashboard:module_duplicate", args=[key, obj.pk]),
            "delete_url": reverse("dashboard:module_delete", args=[key, obj.pk]),
            "image": (
                f"https://ui-avatars.com/api/?name={getattr(obj, 'last_name', '')}+{getattr(obj, 'first_name', '') or getattr(obj, 'username', 'User')}&background=0D8ABC&color=fff" if key == "user"
                else (getattr(obj, "image_url", "") 
                or getattr(obj, "logo_url", "") 
                or (obj.formation.image_url if hasattr(obj, "formation") and obj.formation else "")
                or (obj.activity.image_url if hasattr(obj, "activity") and obj.activity else "")
                or "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=120&h=80&fit=crop&auto=format")
            ),
            "read_only": key == "contact",
            "is_registration": key in ("registration", "activity_registration", "volunteer"),
        })
    context = common_context(module["label"])
    context.update({
        "module": module, "columns": module["columns"], "rows": rows, "objects": objects, "table_items": table_items,
        "intro": _("Liste, filtres, statuts, actions, pagination et exports pour %(label)s.") % {"label": module["label"].lower()},
        "is_contact_module": key == "contact",
        "add_url": reverse(f"dashboard:{module['url']}_add"),
        "detail_url": reverse(f"dashboard:{module['url']}_detail", args=[objects[0].pk]) if objects else reverse(f"dashboard:{module['url']}_add"),
    })
    return render(request, "dashboard/pages/module_list.html", context)


def list_route_name(key):
    if key == "contact":
        return "dashboard:contact_messages"
    return f"dashboard:{MODULES[key]['url']}_list"


def module_form(request, key, pk=None, edit=False, custom_title=None):
    if key == "contact":
        messages.info(request, _("Les messages de contact sont en lecture seule. Ouvrez le détail pour les consulter."))
        if pk:
            return redirect("dashboard:contact_detail", pk=pk)
        return redirect("dashboard:contact_messages")
    module = MODULES[key]
    
    if key == "user":
        from django.contrib.auth.models import User
        from core.models import UserProfile
        obj = get_object_or_404(User, pk=pk) if pk else None
        
        if request.method == "POST":
            first_name = request.POST.get("first_name", "").strip()
            last_name = request.POST.get("last_name", "").strip()
            email = request.POST.get("email", "").strip()
            phone = request.POST.get("phone", "").strip()
            password = request.POST.get("password", "")
            is_active = request.POST.get("status") == "actif"
            
            if not email:
                messages.error(request, _("L'adresse email est requise."))
            else:
                dup = User.objects.filter(email__iexact=email).exclude(pk=obj.pk if obj else None).first()
                if dup:
                    messages.error(request, _("Cet email est déjà utilisé par un autre utilisateur."))
                else:
                    if obj is None:
                        obj = User.objects.create_user(username=email, email=email, password=password)
                    else:
                        obj.email = email
                        obj.username = email
                        if password:
                            obj.set_password(password)
                    obj.first_name = first_name
                    obj.last_name = last_name
                    obj.is_staff = True
                    obj.is_active = is_active
                    obj.save()
                    
                    profile, created = UserProfile.objects.get_or_create(user=obj)
                    profile.phone = phone
                    profile.save()
                    
                    messages.success(request, _("Utilisateur enregistré avec succès."))
                    return redirect("dashboard:user_list")
                    
        action = _("Modifier") if edit or pk else _("Ajouter")
        context = common_context(custom_title or f"{action} {module['singular']}")
        context.update({
            "module": module,
            "object": obj,
            "phone": obj.profile.phone if obj and hasattr(obj, "profile") else "",
            "list_url": reverse(list_route_name(key)),
            "detail_url": reverse("dashboard:user_detail", args=[obj.pk]) if obj else "",
        })
        return render(request, "dashboard/pages/user_form.html", context)
    if key == "partner":
        obj = get_object_or_404(Partner, pk=pk) if pk else None
        form = PartnerForm(request.POST or None, request.FILES or None, instance=obj)
    elif key == "contact":
        obj = get_object_or_404(ContactMessage, pk=pk) if pk else None
        form = ContactMessageForm(request.POST or None, instance=obj)
    elif key == "volunteer":
        obj = get_object_or_404(VolunteerApplication, pk=pk) if pk else None
        form = VolunteerApplicationForm(request.POST or None, instance=obj)
    elif key == "registration":
        obj = get_object_or_404(FormationRegistration, pk=pk) if pk else None
        form = FormationRegistrationForm(request.POST or None, instance=obj)
    elif key == "activity_registration":
        obj = get_object_or_404(ActivityRegistration, pk=pk) if pk else None
        form = ActivityRegistrationForm(request.POST or None, instance=obj)
    else:
        obj = get_object_or_404(ContentItem, pk=pk, module=key) if pk else None
        form = ContentItemForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and key not in ("partner", "contact", "volunteer", "registration", "activity_registration"):
        if obj is None:
            obj = ContentItem(module=key, title=request.POST.get("title") or module["singular"])
        assign_content_item_from_request(obj, request, key)
        obj.save()
        messages.success(request, _("Contenu enregistré avec succès."))
        return redirect(f"dashboard:{module['url']}_edit", pk=obj.pk)
    if request.method == "POST" and form.is_valid():
        saved = form.save(commit=False)
        if isinstance(saved, ContentItem):
            saved.module = key
        apply_uploaded_image_fields(saved, request.FILES, key)
        saved.save()
        messages.success(request, _("Contenu enregistré avec succès."))
        return redirect(list_route_name(key))
    action = _("Modifier") if edit or pk else _("Ajouter")
    context = common_context(custom_title or f"{action} {module['singular']}")
    context.update({
        "module": module,
        "form": form,
        "object": obj,
        "list_url": reverse(list_route_name(key)),
        "detail_url": reverse(f"dashboard:{module['url']}_detail", args=[obj.pk]) if obj else "",
    })
    if key == "news":
        return render(request, "dashboard/pages/news_form.html", context)
    if key == "partner":
        return render(request, "dashboard/pages/partner_form.html", context)
    return render(request, "dashboard/pages/module_form.html", context)


def module_detail(request, key, pk=1):
    module = MODULES[key]
    if key == "partner":
        obj = get_object_or_404(Partner, pk=pk)
    elif key == "contact":
        obj = get_object_or_404(ContactMessage, pk=pk)
    elif key == "volunteer":
        obj = get_object_or_404(VolunteerApplication, pk=pk)
    elif key == "registration":
        obj = get_object_or_404(FormationRegistration, pk=pk)
    elif key == "activity_registration":
        obj = get_object_or_404(ActivityRegistration, pk=pk)
    elif key == "user":
        from django.contrib.auth.models import User
        obj = get_object_or_404(User, pk=pk)
        obj.created_at = obj.date_joined
        obj.updated_at = obj.date_joined
    else:
        obj = get_object_or_404(ContentItem, pk=pk, module=key)
    context = common_context(_("Détails %(singular)s") % {"singular": module["singular"]})
    if key == "registration" and obj.formation:
        detail_image = obj.formation.image_url
        detail_title = obj.formation.title
        detail_summary = obj.formation.summary
        detail_body = obj.formation.body
    elif key == "activity_registration" and obj.activity:
        detail_image = obj.activity.image_url
        detail_title = obj.activity.title
        detail_summary = obj.activity.summary
        detail_body = obj.activity.body
    elif key == "user":
        detail_image = f"https://ui-avatars.com/api/?name={getattr(obj, 'last_name', '')}+{getattr(obj, 'first_name', '') or getattr(obj, 'username', 'User')}&background=0D8ABC&color=fff"
        detail_title = f"{obj.first_name} {obj.last_name}".strip() or obj.username
        detail_summary = obj.email
        phone = obj.profile.phone if hasattr(obj, "profile") else "-"
        role = _("Super-administrateur") if obj.is_superuser else (_("Administrateur") if obj.is_staff else _("Utilisateur"))
        status = _("Actif") if obj.is_active else _("Inactif")
        detail_body = f"Rôle : {role} <br> Téléphone : {phone} <br> Statut : {status} <br> Dernière connexion : {obj.last_login.strftime('%d/%m/%Y %H:%M') if obj.last_login else '-'}"
    else:
        detail_image = getattr(obj, "image_url", "") or getattr(obj, "logo_url", "")
        detail_title = getattr(obj, "title", "") or getattr(obj, "name", "")
        detail_summary = getattr(obj, "summary", "") or getattr(obj, "description", "") or getattr(obj, "message", "")
        detail_body = getattr(obj, "body", "") or getattr(obj, "content", "") or getattr(obj, "message", "")

    if key == "contact" and getattr(obj, "status", "") == "non_lu":
        obj.status = "lu"
        obj.save(update_fields=["status", "updated_at"])
    context.update({
        "module": module,
        "object": obj,
        "is_contact_detail": key == "contact",
        "is_registration": key in ("registration", "activity_registration", "volunteer"),
        "detail_image": detail_image,
        "detail_title": detail_title,
        "detail_summary": detail_summary,
        "detail_body": detail_body,
        "detail_category": getattr(obj, "category", "") or getattr(obj, "partner_type", ""),
        "detail_date": getattr(obj, "date", None) or getattr(obj, "created_at", None),
        "detail_location": getattr(obj, "location", ""),
        "list_url": reverse(f"dashboard:{module['url']}_list") if key != "contact" else reverse("dashboard:contact_messages"),
        "edit_url": reverse(f"dashboard:{module['url']}_edit", args=[pk]) if key != "contact" else reverse("dashboard:contact_edit", args=[pk]),
    })
    return render(request, "dashboard/pages/module_detail.html", context)


def settings_page(request):
    settings_qs = SiteSetting.objects.all().order_by("group", "key")
    form = SiteSettingForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        instance = form.save(commit=False)
        if request.FILES.get("value_upload"):
            uploaded_url = save_uploaded_dashboard_image(request.FILES["value_upload"], "settings")
            instance.value = uploaded_url
            instance.value_fr = uploaded_url
        instance.save()
        messages.success(request, _("Paramètre enregistré."))
        return redirect("dashboard:settings")
    context = common_context(_("Paramètres"))
    context.update({"settings": settings_qs, "form": form})
    return render(request, "dashboard/pages/settings.html", context)


def setting_edit(request, pk):
    setting = get_object_or_404(SiteSetting, pk=pk)
    form = SiteSettingForm(request.POST or None, instance=setting)
    if request.method == "POST" and form.is_valid():
        instance = form.save(commit=False)
        if request.FILES.get("value_upload"):
            uploaded_url = save_uploaded_dashboard_image(request.FILES["value_upload"], "settings")
            instance.value = uploaded_url
            instance.value_fr = uploaded_url
        instance.save()
        messages.success(request, _("Paramètre enregistré."))
        return redirect("dashboard:settings")
        
    context = common_context(_("Modifier le paramètre"))
    context.update({"setting": setting, "form": form})
    return render(request, "dashboard/pages/setting_form.html", context)


def setting_delete(request, pk):
    setting = get_object_or_404(SiteSetting, pk=pk)
    if request.method == "POST":
        setting.delete()
        messages.success(request, _("Paramètre supprimé avec succès."))
    return redirect("dashboard:settings")


def profile(request):
    context = common_context(_("Profil administrateur"))
    context.update({"history_columns": [_("Action"), _("Module"), _("Date"), _("Statut")], "history_rows": [[_("Connexion"), _("Compte"), timezone.now().strftime("%d/%m/%Y %H:%M"), _("actif")], [_("Modification contenu"), _("Accueil"), _("Base MySQL"), _("publié")], [_("Export"), _("Bénévolat"), _("Dashboard"), _("archive")]]})
    return render(request, "dashboard/pages/profile.html", context)



def module_delete(request, key, pk):
    module = MODULES[key]
    if request.method != "POST":
        messages.error(request, _("Action non autorisée."))
        return redirect(list_route_name(key))
    if key == "partner":
        obj = get_object_or_404(Partner, pk=pk)
    elif key == "contact":
        obj = get_object_or_404(ContactMessage, pk=pk)
    elif key == "volunteer":
        obj = get_object_or_404(VolunteerApplication, pk=pk)
    elif key == "registration":
        obj = get_object_or_404(FormationRegistration, pk=pk)
    elif key == "activity_registration":
        obj = get_object_or_404(ActivityRegistration, pk=pk)
    elif key == "user":
        from django.contrib.auth.models import User
        obj = get_object_or_404(User, pk=pk)
        if request.user.pk == obj.pk:
            messages.error(request, _("Vous ne pouvez pas supprimer votre propre compte."))
            return redirect(list_route_name(key))
    else:
        obj = get_object_or_404(ContentItem, pk=pk, module=key)
    obj.delete()
    messages.success(request, _("Élément supprimé avec succès."))
    return redirect(list_route_name(key))


def module_duplicate(request, key, pk):
    if key in ("user", "contact", "registration", "activity_registration", "volunteer"):
        messages.error(request, _("Cette action n'est pas autorisée pour ce module."))
        return redirect(list_route_name(key))
    if key == "partner":
        orig = get_object_or_404(Partner, pk=pk)
    elif key == "contact":
        orig = get_object_or_404(ContactMessage, pk=pk)
    elif key == "volunteer":
        orig = get_object_or_404(VolunteerApplication, pk=pk)
    elif key == "registration":
        orig = get_object_or_404(FormationRegistration, pk=pk)
    elif key == "activity_registration":
        orig = get_object_or_404(ActivityRegistration, pk=pk)
    else:
        orig = get_object_or_404(ContentItem, pk=pk, module=key)
        
    orig.pk = None
    orig.id = None
    if hasattr(orig, "title") and orig.title:
        orig.title = f"{orig.title} (Copie)"
    elif hasattr(orig, "name") and orig.name:
        orig.name = f"{orig.name} (Copie)"
    orig.save()
    
    messages.success(request, _("Élément dupliqué avec succès."))
    return redirect(list_route_name(key))


@require_POST
def update_registration_status(request, key, pk):
    if key == "registration":
        obj = get_object_or_404(FormationRegistration, pk=pk)
        success_url = reverse("dashboard:registration_detail", args=[pk])
    elif key == "activity_registration":
        obj = get_object_or_404(ActivityRegistration, pk=pk)
        success_url = reverse("dashboard:activity_registration_detail", args=[pk])
    elif key == "volunteer":
        obj = get_object_or_404(VolunteerApplication, pk=pk)
        success_url = reverse("dashboard:volunteer_detail", args=[pk])
    else:
        return redirect("dashboard:home")
        
    status = request.POST.get("status")
    if status in ("accepte", "refuse", "en_attente"):
        obj.status = status
        obj.save(update_fields=["status", "updated_at"])
        messages.success(request, _("Le statut de l'inscription a été mis à jour."))
        
    return redirect(success_url)


def translate_api_view(request):
    text = request.GET.get("text", "").strip()
    if not text:
        return JsonResponse({"ar": "", "en": ""})
        
    import urllib.request, urllib.parse, json
    
    def translate_helper(txt, lang):
        # 1. Try Chrome Extension Google Translate API (reliable, bypasses 429)
        try:
            url = "https://clients5.google.com/translate_a/t?client=dict-chrome-ex&sl=fr&tl=" + lang + "&q=" + urllib.parse.quote(txt)
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req, timeout=5)
            data = json.loads(res.read().decode('utf-8'))
            if isinstance(data, list) and len(data) > 0:
                return data[0]
        except Exception:
            pass
            
        # 2. Fallback to gtx endpoint
        try:
            url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=fr&tl=" + lang + "&dt=t&q=" + urllib.parse.quote(txt)
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req, timeout=5)
            data = json.loads(res.read().decode('utf-8'))
            return "".join([part[0] for part in data[0] if part[0]])
        except Exception:
            return ""
            
    ar_trans = translate_helper(text, "ar")
    en_trans = translate_helper(text, "en")
    
    return JsonResponse({"ar": ar_trans, "en": en_trans})

