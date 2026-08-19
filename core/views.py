from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST

from .models import ContactMessage, ContentItem, PageContent, Partner, SiteSetting, VolunteerApplication, FormationRegistration
from .i18n import get_language_code, localize_object, localize_queryset, localized_value, clean_display_text


FAKE_PUBLIC_TOKENS = ("images.unsplash.com", "placehold.co", "example", "dQw4w9WgXcQ", "ui-avatars.com", "Ahmed El Mansouri", "Fatima Zahra Bennani")

DISPLAY_TEXT_REPLACEMENTS = {
    "M?tropole": "Métropole",
    "Métropole": "Métropole",
    "Actualités": "Actualités",
    "Activités": "Activités",
    "Médias": "Médias",
    "Bénévolat": "Bénévolat",
    "é": "é",
    "è": "è",
    "ê": "ê",
    "Ã ": "à",
    "v?rifi?": "vérifié",
}


def clean_display_text(value):
    if not isinstance(value, str):
        return value
    result = value
    for old, new in DISPLAY_TEXT_REPLACEMENTS.items():
        result = result.replace(old, new)
    return result


def public_value(value):
    value = value or ""
    return "" if any(token in value for token in FAKE_PUBLIC_TOKENS) else value


def public_media_url(value):
    return public_value(value)


def page(slug, lang=None):
    return localize_object(PageContent.objects.filter(slug=slug, status="publie").first(), ["title", "subtitle", "content", "meta_title", "meta_description", "keywords"], lang)


def published(module):
    return ContentItem.objects.filter(module=module).exclude(status__in=["brouillon", "archive", "inactif"]).order_by("order", "-date", "-created_at")


def media_json(items, lang=None):
    lang = lang or get_language_code()
    data = []
    for item in items:
        category_lower = (item.category or "").lower()
        if "video" in category_lower or "youtube" in category_lower or item.video_url:
            media_type = "video"
        elif "pdf" in category_lower or "doc" in category_lower:
            media_type = "pdf"
        else:
            media_type = "photo"
            
        video_url = item.video_url or item.youtube_url or ""
        platform = "YouTube"
        if "vimeo" in video_url.lower():
            platform = "Vimeo"
            
        data.append({
            "id": item.id,
            "type": media_type,
            "title": localized_value(item, "title", lang),
            "description": localized_value(item, "summary", lang) or localized_value(item, "body", lang),
            "category": localized_value(item, "category", lang),
            "date": (item.date or item.created_at.date()).isoformat(),
            "thumbnail": public_media_url(item.image_url),
            "source": public_value(item.video_url or item.image_url),
            "album": item.slug or item.category,
            
            # Video specific
            "videoUrl": public_value(video_url),
            "videoPlatform": platform,
            "duration": f"{item.reading_time} min" if item.reading_time else "3:45",
            
            # PDF specific
            "pages": item.reading_time or 12,
            "fileSize": item.location or "1.5 MB",
            "language": "Français" if lang == "fr" else ("العربية" if lang == "ar" else "English"),
            "fileUrl": public_value(item.video_url or item.image_url),
        })
    return data


def volunteer_photos_json(items, lang=None):
    lang = lang or get_language_code()
    data = []
    for item in items:
        data.append({
            "src": public_media_url(item.image_url),
            "title": localized_value(item, "title", lang),
            "legend": localized_value(item, "summary", lang) or localized_value(item, "body", lang),
            "date": (item.date or item.created_at.date()).isoformat(),
        })
    return data


def volunteer_videos_json(items, lang=None):
    lang = lang or get_language_code()
    data = []
    for item in items:
        video_url = item.video_url or item.youtube_url or ""
        platform = "youtube" if "youtube" in video_url.lower() else "vimeo"
        data.append({
            "url": public_value(video_url),
            "platform": platform,
            "thumb": public_media_url(item.image_url),
            "title": localized_value(item, "title", lang),
            "desc": localized_value(item, "summary", lang) or localized_value(item, "body", lang),
        })
    return data


def testimonials_json(items, lang=None):
    lang = lang or get_language_code()
    data = []
    for item in items:
        data.append({
            "photo": public_media_url(item.image_url),
            "quote": localized_value(item, "body", lang) or localized_value(item, "summary", lang),
            "name": localized_value(item, "title", lang),
            "role": localized_value(item, "category", lang),
        })
    return data


def volunteer_actions_json(items, lang=None):
    lang = lang or get_language_code()
    data = []
    for item in items:
        data.append({
            "image": public_media_url(item.image_url),
            "title": localized_value(item, "title", lang),
            "description": localized_value(item, "summary", lang) or localized_value(item, "body", lang),
            "date": (item.date or item.created_at.date()).isoformat(),
            "location": localized_value(item, "location", lang) or "Tanger",
            "volunteers": item.participants,
        })
    return data


def volunteer_faq_json(lang=None):
    lang = lang or get_language_code()
    from core.models import PageContent
    try:
        page = PageContent.objects.get(slug="benevolat")
        if page.sections and isinstance(page.sections, list):
            faqs = []
            for f in page.sections:
                if lang == "ar":
                    q = f.get("q_ar") or f.get("q")
                    r = f.get("r_ar") or f.get("r")
                elif lang == "en":
                    q = f.get("q_en") or f.get("q")
                    r = f.get("r_en") or f.get("r")
                else:
                    q = f.get("q")
                    r = f.get("r")
                faqs.append({"q": q, "r": r})
            return faqs
    except Exception:
        pass

    if lang == "ar":
        return [
            {"q": "كيف يمكنني أن أصبح متطوعًا؟", "r": "للقيام بذلك، ما عليك سوى ملء استمارة التقديم على هذه الصفحة. سيتصل بك فريقنا بمجرد توفر مهمة تناسب مؤهلاتك."},
            {"q": "ما هي شروط التطوع؟", "r": "لا توجد شروط خاصة. يمكن للجميع المشاركة والمساهمة وفقًا لمهاراتهم واهتماماتهم وأوقات فارغهم."},
            {"q": "كم من الوقت يجب أن أخصصه للتطوع؟", "r": "الالتزام مرن للغاية. يمكنك اختيار الفترات التي تناسب جدولك الزمني (خلال الأسبوع، في عطلة نهاية الأسبوع، أو بشكل دوري)."}
        ]
    elif lang == "en":
        return [
            {"q": "How can I become a volunteer?", "r": "To become a volunteer, simply fill out the application form on this page. Our team will contact you as soon as a mission corresponding to your profile is available."},
            {"q": "What are the conditions to be a volunteer?", "r": "There are no special conditions. Everyone can get involved according to their skills, interests, and availability."},
            {"q": "How much time do I need to devote to volunteering?", "r": "Commitment is flexible. You can choose your slots according to your schedule (weekdays, weekends, occasionally, or regularly)."}
        ]
    else:  # Default to French
        return [
            {"q": "Comment puis-je devenir bénévole ?", "r": "Pour devenir bénévole, il vous suffit de remplir le formulaire de candidature sur cette page. Notre équipe vous contactera dès qu'une mission correspondant à votre profil sera disponible."},
            {"q": "Quelles sont les conditions pour être bénévole ?", "r": "Il n'y a pas de conditions particulières. Tout le monde peut s'engager selon ses compétences, ses centres d'intérêt et ses disponibilités."},
            {"q": "Combien de temps dois-je consacrer au bénévolat ?", "r": "L'engagement est flexible. Vous pouvez choisir vos créneaux en fonction de votre emploi du temps (en semaine, le week-end, ponctuellement ou régulièrement)."}
        ]


def content_json(items, module, lang=None):
    lang = lang or get_language_code()
    data = []
    for item in items:
        base = {
            "id": item.id,
            "title": localized_value(item, "title", lang),
            "slug": item.slug,
            "category": item.category,
            "description": localized_value(item, "summary", lang),
            "excerpt": localized_value(item, "summary", lang),
            "content": localized_value(item, "body", lang),
            "image": public_media_url(item.image_url),
            "img": public_media_url(item.image_url),
            "cat": item.category,
            "titre": localized_value(item, "title", lang),
            "desc": localized_value(item, "summary", lang),
            "date": (item.date or item.start_date or item.created_at.date()).isoformat(),
            "location": localized_value(item, "location", lang),
            "youtubeUrl": public_value(item.youtube_url or item.video_url),
            "videoUrl": public_value(item.video_url),
            "instagramUrl": public_value(item.instagram_url),
            "facebookUrl": public_value(item.facebook_url),
            "author": clean_display_text(item.author),
            "readingTime": item.reading_time,
            "featured": item.featured,
            "participants": (item.participants or 0) + item.activity_registrations.filter(status="accepte").count(),
            "reports": item.reports_count,
            "url": f"/الأنشطة/#activity-{item.id}" if lang == "ar" else f"/activites/#activity-{item.id}",
            "readMoreText": "اقرأ المزيد" if lang == "ar" else ("Read more" if lang == "en" else "Lire la suite"),
        }
        if module == "formation":
            accepted_count = item.registrations.filter(status="accepte").count()
            total_reg = (item.registered_seats or 0) + accepted_count
            base.update({
                "fullDescription": localized_value(item, "body", lang),
                "startDate": (item.start_date or item.date).isoformat() if (item.start_date or item.date) else "",
                "endDate": (item.end_date or item.start_date or item.date).isoformat() if (item.end_date or item.start_date or item.date) else "",
                "startTime": item.start_time.strftime("%H:%M") if item.start_time else "",
                "endTime": item.end_time.strftime("%H:%M") if item.end_time else "",
                "instructor": {"name": localized_value(item, "instructor_name", lang) or clean_display_text(public_value(item.author)), "role": "", "photo": public_media_url(item.image_url)},
                "totalSeats": item.total_seats,
                "registeredSeats": total_reg,
                "registrationDeadline": (item.date or item.start_date).isoformat() if (item.date or item.start_date) else "",
                "status": "open" if item.status in ["publie", "actif"] else item.status,
            })
        data.append(base)
    return data


def site_settings(lang=None):
    return {s.key: localized_value(s, "value", lang) for s in SiteSetting.objects.all()}


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


def home_text(page_content, key, lang=None):
    lang = lang or get_language_code()
    sections = getattr(page_content, "sections", None) or {}
    default = HOME_TEXT_DEFAULTS.get(key, "")
    if isinstance(sections, dict):
        texts = sections.get("texts")
        if isinstance(texts, dict):
            if lang != "fr" and texts.get(f"{key}_{lang}"):
                return clean_display_text(texts.get(f"{key}_{lang}"))
            if texts.get(key) not in (None, ""):
                return clean_display_text(texts.get(key))
        if lang != "fr" and sections.get(f"{key}_{lang}"):
            return clean_display_text(sections.get(f"{key}_{lang}"))
        if sections.get(key) not in (None, ""):
            return clean_display_text(sections.get(key))
    return clean_display_text(default)


def home(request):
    from django.db.models import Sum
    lang = get_language_code(request)
    page_content = page("accueil", lang)
    context = {
        "page_content": page_content,
        "home_texts": {key: home_text(page_content, key, lang) for key in HOME_TEXT_DEFAULTS},
        "announcements": localize_queryset(published("news")[:6], ["title", "category", "summary", "body"], lang),
        "activities": content_json(published("activity").order_by("-date", "-created_at")[:6], "activity", lang),
        "partners": localize_queryset([p for p in Partner.objects.filter(status="actif", featured_home=True)[:12] if public_media_url(p.logo_url) or p.name], ["name", "partner_type", "description"], lang),
        "programs": localize_queryset(published("program")[:4], ["title", "category", "summary", "body"], lang),
        "settings": site_settings(lang),
        "beneficiaries_count": ContentItem.objects.filter(module="activity", status="publie").aggregate(total=Sum("participants"))["total"] or 0,
        "programs_count": ContentItem.objects.filter(module="program").exclude(status__in=["brouillon", "archive", "inactif"]).count(),
        "formations_count": ContentItem.objects.filter(module="formation").exclude(status__in=["brouillon", "archive", "inactif"]).count(),
        "partners_count": Partner.objects.filter(status="actif").count(),
        "volunteers_count": VolunteerApplication.objects.filter(status__in=["accepte", "actif"]).count(),
        "years_count": SiteSetting.objects.filter(key="stats_annees").values_list("value", flat=True).first() or 0,
    }
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get("nom", ""),
            email=request.POST.get("email", ""),
            message=request.POST.get("message", ""),
            subject="Contact accueil",
        )
        return redirect("core:home")
    return render(request, "pages/index.html", context)



ABOUT_SECTION_DEFAULTS = {
    "presentation_cards": [
        {"icon": "fa-calendar-alt", "title": "Date de création", "text": "27 mars 2017"},
        {"icon": "fa-eye", "title": "Vision", "text": "Devenir une référence dans l'accompagnement et la qualification des jeunes et des femmes, ainsi qu'un modèle de travail associatif structuré, innovant et engagé dans le développement humain et territorial."},
        {"icon": "fa-rocket", "title": "Mission", "text": "Autonomiser les jeunes et les femmes du Grand Tanger à travers des programmes de formation, d'accompagnement et d'encadrement."},
        {"icon": "fa-map-marker-alt", "title": "Zone d'intervention", "text": "Le Grand Tanger et ses environs"},
        {"icon": "fa-users", "title": "Publics ciblés", "text": "Les jeunes, les femmes, les porteurs de projets, les associations locales et les acteurs de la société civile."},
    ],
    "mission_features": [
        "Formation professionnelle",
        "Insertion sociale",
        "Citoyenneté active",
        "Autonomisation",
    ],
    "objectives": [
        {"icon": "fa-hand-holding-heart", "title": "Solidarité sociale", "text": "Créer un cadre permettant de renforcer et d'enraciner les valeurs de solidarité et d'entraide sociale."},
        {"icon": "fa-handshake", "title": "Partenariats", "text": "Développer des partenariats durables avec des organismes, institutions et acteurs nationaux et internationaux."},
        {"icon": "fa-globe-africa", "title": "Diplomatie parallèle", "text": "Jouer un rôle dans la diplomatie parallèle et favoriser l'échange d'expériences."},
        {"icon": "fa-palette", "title": "Industrie culturelle", "text": "Promouvoir le concept d'industrie culturelle à travers des projets, événements et initiatives artistiques."},
        {"icon": "fa-lightbulb", "title": "Créativité et innovation", "text": "Encourager la créativité, l'innovation et la participation active des jeunes et des femmes."},
        {"icon": "fa-chalkboard-teacher", "title": "Formation et accompagnement", "text": "Organiser des programmes de formation, d'encadrement et d'accompagnement adaptés."},
    ],
    "values": [
        {"icon": "fa-flag", "title": "Citoyenneté"},
        {"icon": "fa-heart", "title": "Solidarité"},
        {"icon": "fa-fist-raised", "title": "Engagement"},
        {"icon": "fa-people-arrows", "title": "Inclusion"},
        {"icon": "fa-lightbulb", "title": "Innovation"},
        {"icon": "fa-balance-scale", "title": "Responsabilité"},
    ],
    "zone_stats": [
        {"icon": "fa-city", "title": "Tanger Ville"},
        {"icon": "fa-map", "title": "Tanger-Med"},
        {"icon": "fa-building", "title": "Zones industrielles"},
    ],
}


ABOUT_TEXT_DEFAULTS = {
    "presentation_title": "À propos de la Fondation Tanger Métropole",
    "mission_label": "Notre raison d'être",
    "mission_title": "Notre mission",
    "mission_button_text": "Découvrir nos programmes",
    "objectives_title": "Nos objectifs",
    "values_title": "Nos valeurs",
    "bureau_title": "Notre bureau dirigeant",
    "bureau_intro": "Une équipe engagée qui œuvre pour la réalisation des objectifs de la Fondation et le développement de ses actions.",
    "members_title": "Liste des membres du bureau dirigeant",
    "members_intro": "Consultez la liste complète des membres de notre bureau dirigeant avec leurs fonctions et statuts.",
    "members_search_placeholder": "Rechercher un membre par nom ou fonction...",
    "members_filter_all": "Toutes les fonctions",
    "members_export": "Exporter",
    "members_empty_title": "Aucun membre trouvé",
    "members_empty_text": "Essayez de modifier vos critères de recherche.",
    "zone_title": "Notre zone d'intervention",
    "zone_name": "Grand Tanger",
    "zone_text": "La Fondation Tanger Métropole intervient principalement dans le Grand Tanger et ses environs, en développant des projets sociaux, éducatifs, culturels, professionnels et citoyens.",
    "cta_title": "Construisons ensemble l'avenir du Grand Tanger",
    "cta_text": "Rejoignez nos programmes, devenez bénévole ou contactez-nous pour proposer une initiative au service de la communauté.",
    "cta_primary_text": "Devenir bénévole",
    "cta_secondary_text": "Nous contacter",
}


def about_text(page_content, key, lang=None):
    lang = lang or get_language_code()
    sections = getattr(page_content, "sections", None) or {}
    default = ABOUT_TEXT_DEFAULTS.get(key, "")
    if isinstance(sections, dict):
        texts = sections.get("texts")
        if isinstance(texts, dict):
            if lang != "fr" and texts.get(f"{key}_{lang}"):
                return clean_display_text(texts.get(f"{key}_{lang}"))
            if texts.get(key) not in (None, ""):
                return clean_display_text(texts.get(key))
        if lang != "fr" and sections.get(f"{key}_{lang}"):
            return clean_display_text(sections.get(f"{key}_{lang}"))
        if sections.get(key) not in (None, ""):
            return clean_display_text(sections.get(key))
    return clean_display_text(default)


def about_section(page_content, key, lang=None):
    lang = lang or get_language_code()
    sections = getattr(page_content, "sections", None) or []
    raw_items = []
    if isinstance(sections, dict):
        raw_items = sections.get(key) or []
    elif isinstance(sections, list):
        for section in sections:
            if isinstance(section, dict) and section.get("key") == key:
                raw_items = section.get("items", section.get("value", section.get("text"))) or []
                break
    if not raw_items:
        raw_items = ABOUT_SECTION_DEFAULTS.get(key, [])

    if not isinstance(raw_items, list):
        return raw_items

    localized_items = []
    for item in raw_items:
        if isinstance(item, dict):
            item_copy = dict(item)
            if lang != "fr":
                for field in ("title", "text", "feature"):
                    if item_copy.get(f"{field}_{lang}"):
                        item_copy[field] = item_copy[f"{field}_{lang}"]
            for field in ("title", "text", "feature"):
                if field in item_copy:
                    item_copy[field] = clean_display_text(item_copy.get(field, ""))
            localized_items.append(item_copy)
        elif isinstance(item, str):
            localized_items.append(clean_display_text(item))
        else:
            localized_items.append(item)
    return localized_items


def member_image(member):
    if public_media_url(member.image_url):
        return member.image_url
    name = (localized_value(member, "title") or "Membre FTM").replace(" ", "+")
    return f"https://ui-avatars.com/api/?name={name}&size=400&background=062B4F&color=fff&bold=true"


def about_team_members(items, lang=None):
    members = []
    for item in items:
        members.append({
            "id": item.id,
            "name": localized_value(item, "title", lang),
            "role": localized_value(item, "category", lang),
            "bio": localized_value(item, "body", lang) or localized_value(item, "summary", lang),
            "summary": localized_value(item, "summary", lang),
            "image": member_image(item),
            "email": item.author or "",
            "status": item.status,
            "facebook": item.facebook_url or "",
            "instagram": item.instagram_url or "",
            "youtube": item.youtube_url or "",
            "linkedin": item.linkedin_url or "",
            "twitter": item.twitter_url or "",
            "tiktok": item.tiktok_url or "",
        })
    return members


def about(request):
    lang = get_language_code(request)
    page_content = page("a-propos", lang)
    team_items = localize_queryset(published("team").order_by("order", "created_at"), ["title", "category", "summary", "body"], lang)
    context = {
        "page_content": page_content,
        "about_texts": {key: about_text(page_content, key, lang) for key in ABOUT_TEXT_DEFAULTS},
        "settings": site_settings(lang),
        "programs": localize_queryset(published("program"), ["title", "category", "summary", "body"], lang),
        "presentation_cards": about_section(page_content, "presentation_cards", lang),
        "mission_features": about_section(page_content, "mission_features", lang),
        "objectives": about_section(page_content, "objectives", lang),
        "values": about_section(page_content, "values", lang),
        "zone_stats": about_section(page_content, "zone_stats", lang),
        "team_members": about_team_members(team_items, lang),
    }
    return render(request, "pages/about.html", context)


def activites(request):
    lang = get_language_code(request)
    return render(request, "pages/activites.html", {"page_content": page("activites", lang), "activities_json": content_json(published("activity"), "activity", lang), "settings": site_settings(lang)})


def actualites(request):
    lang = get_language_code(request)
    return render(request, "pages/actualites.html", {"page_content": page("actualites", lang), "news_json": content_json(published("news"), "news", lang), "settings": site_settings(lang)})


def formations(request):
    lang = get_language_code(request)
    all_formations = published("formation")
    
    total_count = all_formations.count()
    open_count = 0
    total_seats = 0
    total_registered = 0
    
    from django.utils import timezone
    now = timezone.now()
    
    for f in all_formations:
        accepted_count = f.registrations.filter(status="accepte").count()
        reg = (f.registered_seats or 0) + accepted_count
        tot = f.total_seats or 0
        rem = max(0, tot - reg)
        
        total_registered += reg
        total_seats += rem
        
        # Determine status matching JS logic
        is_finished = False
        if f.end_date and f.end_time:
            from datetime import datetime
            try:
                end_dt = datetime.combine(f.end_date, f.end_time)
                # Handle timezone awareness
                if timezone.is_aware(end_dt):
                    if now > end_dt:
                        is_finished = True
                else:
                    if timezone.make_naive(now) > end_dt:
                        is_finished = True
            except Exception:
                pass
                
        is_closed = False
        if f.start_date and now.date() > f.start_date:
            is_closed = True
            
        if not is_finished and not is_closed and rem > 0:
            open_count += 1
            
    stats = {
        "total": total_count,
        "open": open_count,
        "seats": total_seats,
        "registered": total_registered,
    }
    
    return render(request, "pages/formations.html", {
        "page_content": page("formations", lang),
        "formations_json": content_json(all_formations, "formation", lang),
        "settings": site_settings(lang),
        "stats": stats,
    })


def medias(request):
    lang = get_language_code(request)
    return render(request, "pages/medias.html", {"page_content": page("medias", lang), "media_items": published("media"), "media_json": media_json(published("media"), lang), "settings": site_settings(lang)})


def benevolat(request):
    lang = get_language_code(request)
    if request.method == "POST":
        import json
        name = request.POST.get("nom") or request.POST.get("name")
        email = request.POST.get("email", "")
        phone = request.POST.get("telephone") or request.POST.get("phone", "")
        city = request.POST.get("ville") or request.POST.get("city", "")
        skills = request.POST.get("competences") or request.POST.get("skills", "")
        motivation = request.POST.get("motivation") or request.POST.get("message", "")
        
        skills_description = request.POST.get("skills_description", "")
        availability = request.POST.get("availability", "")
        desired_fields = request.POST.get("desired_fields", "")
        experience = request.POST.get("experience", "")
        
        # Parse JSON payload for AJAX calls
        if not name and request.body:
            try:
                data = json.loads(request.body)
                name = data.get("nom") or data.get("name")
                email = data.get("email", "")
                phone = data.get("telephone") or data.get("phone", "")
                city = data.get("ville") or data.get("city", "")
                skills = data.get("competences") or data.get("skills", "")
                skills_description = data.get("skills_description", "")
                availability = data.get("availability", "")
                desired_fields = data.get("desired_fields", "")
                motivation = data.get("motivation") or data.get("message", "")
                experience = data.get("experience", "")
            except Exception:
                pass

        cv_file = request.FILES.get("cv")
        cv_url = ""
        if cv_file:
            from django.core.files.storage import default_storage
            path = default_storage.save(f"volunteers/{cv_file.name}", cv_file)
            cv_url = default_storage.url(path)

        app = VolunteerApplication.objects.create(
            name=name or "",
            email=email or "",
            phone=phone or "",
            city=city or "",
            skills=skills or "",
            skills_description=skills_description,
            cv_url=cv_url,
            availability=availability,
            desired_fields=desired_fields,
            motivation=motivation or "",
            experience=experience,
        )
        
        # Check if AJAX request
        if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.content_type == "application/json":
            return JsonResponse({"status": "success", "reference": f"FTM-BNV-{app.id}"})
            
        return redirect("core:benevolat")
    from django.db.models import Sum
    active_volunteers_count = VolunteerApplication.objects.filter(status__in=["accepte", "actif"]).count()
    total_volunteers = active_volunteers_count
    
    total_activities = ContentItem.objects.filter(module="activity", status="publie").count()
    activities_stat = total_activities
    hours_stat = active_volunteers_count * 15
    
    # Calculate sum of participants configured in all published activities
    beneficiaries_stat = ContentItem.objects.filter(module="activity", status="publie").aggregate(total=Sum("participants"))["total"] or 0
    missions_stat = total_activities
    
    stats = {
        "volunteers": total_volunteers,
        "hours": hours_stat,
        "activities": activities_stat,
        "beneficiaries": beneficiaries_stat,
        "missions": missions_stat,
    }
    
    all_media = published("media")
    photos = all_media.exclude(category__icontains="video").exclude(category__icontains="pdf")
    videos = all_media.filter(category__icontains="video")
    
    return render(request, "pages/benevolat.html", {
        "page_content": page("benevolat", lang),
        "testimonials": localize_queryset(published("testimonial"), ["title", "category", "summary", "body"], lang),
        "volunteer_actions": volunteer_actions_json(published("activity"), lang),
        "volunteer_photos": volunteer_photos_json(photos, lang),
        "volunteer_videos": volunteer_videos_json(videos, lang),
        "testimonials_json": testimonials_json(published("testimonial"), lang),
        "faq_json": volunteer_faq_json(lang),
        "stats": stats,
        "settings": site_settings(lang)
    })


def contact(request):
    lang = get_language_code(request)
    if request.method == "POST":
        import json
        name = request.POST.get("nom") or request.POST.get("name")
        email = request.POST.get("email", "")
        phone = request.POST.get("telephone") or request.POST.get("phone", "")
        city = request.POST.get("ville") or request.POST.get("city", "")
        if city == "autre" or request.POST.get("autreVille"):
            city = request.POST.get("autreVille") or city
            
        objet = request.POST.get("objet", "")
        if objet == "autre" or request.POST.get("autreObjet"):
            objet = request.POST.get("autreObjet") or objet
            
        sujet = request.POST.get("sujet") or request.POST.get("subject", "Contact")
        message = request.POST.get("message", "")
        
        # Parse JSON payload for AJAX calls
        if not name and request.body:
            try:
                data = json.loads(request.body)
                name = data.get("nom") or data.get("name")
                email = data.get("email", "")
                phone = data.get("telephone") or data.get("phone", "")
                city = data.get("ville") or data.get("city", "")
                if city == "autre" or data.get("autreVille"):
                    city = data.get("autreVille") or city
                objet = data.get("objet", "")
                if objet == "autre" or data.get("autreObjet"):
                    objet = data.get("autreObjet") or objet
                sujet = data.get("sujet") or data.get("subject", "Contact")
                message = data.get("message", "")
            except Exception:
                pass
                
        # Handle attachment upload
        pj_file = request.FILES.get("pj")
        attachment_url = ""
        if pj_file:
            from django.core.files.storage import default_storage
            path = default_storage.save(f"contact_attachments/{pj_file.name}", pj_file)
            attachment_url = default_storage.url(path)
                
        # Build nice subject line
        final_subject = f"[{objet}] {sujet}" if objet else sujet
        
        msg = ContactMessage.objects.create(
            name=name or "",
            email=email or "",
            phone=phone or "",
            city=city or "",
            subject=final_subject,
            message=message or "",
            attachment_url=attachment_url,
        )
        
        # Check if AJAX request
        if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.content_type == "application/json":
            return JsonResponse({"status": "success", "reference": f"FTM-MSG-{msg.id}"})
            
        return redirect("core:contact")
    return render(request, "pages/contact.html", {"page_content": page("contact", lang), "settings": site_settings(lang)})


def programme(request):
    return activites(request)


@require_POST
def register_formation(request, formation_id):
    formation = get_object_or_404(ContentItem, id=formation_id, module="formation")
    
    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    phone = request.POST.get("phone", "").strip()
    city = request.POST.get("city", "").strip()
    
    if not name or not email or not phone or not city:
        return JsonResponse({"success": False, "error": "Veuillez remplir tous les champs obligatoires."}, status=400)
        
    registration = FormationRegistration.objects.create(
        formation=formation,
        name=name,
        email=email,
        phone=phone,
        city=city,
        status="en_attente"
    )
    
    return JsonResponse({"success": True, "registration_id": registration.id})


@require_POST
def register_activity(request, activity_id):
    activity = get_object_or_404(ContentItem, id=activity_id, module="activity")
    
    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    phone = request.POST.get("phone", "").strip()
    city = request.POST.get("city", "").strip()
    
    if not name or not email or not phone or not city:
        return JsonResponse({"success": False, "error": "Veuillez remplir tous les champs obligatoires."}, status=400)
        
    registration = ActivityRegistration.objects.create(
        activity=activity,
        name=name,
        email=email,
        phone=phone,
        city=city,
        status="en_attente"
    )
    
    return JsonResponse({"success": True, "registration_id": registration.id})

