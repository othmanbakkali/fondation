import re
from django.utils.translation import get_language

SUPPORTED_LANGUAGES = ("fr", "ar", "en")

DISPLAY_TEXT_REPLACEMENTS = {
    # Match literal question marks resulting from encoding corruptions
    "M?tropole": "Métropole",
    "Mtropole": "Métropole",
    "Mtropole": "Métropole",
    "v?rifi?": "vérifié",
    "vrifi": "vérifié",
    "vrifi": "vérifié",
    "v?rifi": "vérifié",
    
    # Match incorrect double UTF-8 / latin-1 conversions
    "Ã©": "é",
    "Ã¨": "è",
    "Ã ": "à",
    "Ã¢": "â",
    "Ãª": "ê",
    "Ã´": "ô",
    "Ã¹": "ù",
    "Ã»": "û",
    "Ã§": "ç",
    "Ã": "à",
    "Ã‰": "É",
    "Ãˆ": "È",
    "Ã€": "À",
    "Ã‚": "Â",
    "Ã": "Ê",
    "Ã": "Ä",
    "Ã": "Ö",
    "Ã": "Ü",
    
    # Common words in page content titles and subtitles
    "Ã€ propos": "À propos",
    "Ã  propos": "à propos",
    "DÃ©couvrez": "Découvrez",
    "dÃ©couvrez": "découvrez",
    "dÃ©couvrir": "découvrir",
    "DÃ©couvrir": "Découvrir",
    "dÃ©filement": "défilement",
    "DÃ©filer": "Défiler",
    "dÃ©filer": "défiler",
    "bÃ©nÃ©vole": "bénévole",
    "BÃ©nÃ©vole": "bénévole",
    "BÃ©nÃ©volat": "bénévolat",
    "bÃ©nÃ©volat": "bénévolat",
    "actualitÃ©s": "actualités",
    "ActualitÃ©s": "Actualités",
    "activitÃ©s": "activités",
    "ActivitÃ©s": "Activités",
    "mÃ©dias": "médias",
    "MÃ©dias": "Médias",
    "partenaires": "partenaires",
    "Partenaires": "Partenaires",
    "prÃ©sent": "présent",
    "PrÃ©sent": "Présent",
    "rÃ©alisation": "réalisation",
    "RÃ©alisation": "Réalisation",
    "dÃ©veloppement": "développement",
    "DÃ©veloppement": "Développement",
    "Ã©quipe": "équipe",
    "Ãquipe": "Équipe",
    "dÃ©cision": "décision",
    "DÃ©cision": "Décision",
    "intÃ©gration": "intégration",
    "IntÃ©gration": "Intégration",
    "citoyennetÃ©": "citoyenneté",
    "CitoyennetÃ©": "Citoyenneté",
    "solidaritÃ©": "solidarité",
    "SolidaritÃ©": "Solidarité",
    "activitÃ©": "activité",
    "ActivitÃ©": "Activité",
    "nouveau": "nouveau",
    "Nouveau": "Nouveau",
    "annonces": "annonces",
    "Annonces": "Annonces",
    "bÃ©nÃ©ficiaires": "bénéficiaires",
    "BÃ©nÃ©ficiaires": "Bénéficiaires",
    "publiÃ©s": "publiés",
    "PubliÃ©s": "Publiés",
    "publiÃ©es": "publiées",
    "PubliÃ©es": "Publiées",
    "annÃ©es": "années",
    "AnnÃ©es": "Années",
    "expÃ©rience": "expérience",
    "ExpÃ©rience": "Expérience",
    "domaines": "domaines",
    "Domaines": "Domaines",
    "intervention": "intervention",
    "Intervention": "Intervention",
    "rejoignez": "rejoignez",
    "Rejoignez": "Rejoignez",
    "inscrire": "inscrire",
    "Inscrire": "Inscrire",
    "envoyer": "envoyer",
    "Envoyer": "Envoyer",
}


def clean_display_text(value):
    if not isinstance(value, str):
        return value
    result = value
    for old, new in DISPLAY_TEXT_REPLACEMENTS.items():
        result = result.replace(old, new)
    return result


def get_language_code(request=None):
    lang = get_language()
    if lang:
        lang = lang.split("-")[0]
        if lang in SUPPORTED_LANGUAGES:
            return lang
    if request:
        session_lang = request.session.get("django_language")
        if session_lang in SUPPORTED_LANGUAGES:
            return session_lang
        cookie_lang = request.COOKIES.get("django_language")
        if cookie_lang in SUPPORTED_LANGUAGES:
            return cookie_lang
    return "fr"


def get_ui(lang=None, request=None):
    return {
        "about": "About",
        "programme": "Programme",
        "activities": "Activités",
        "news": "Actualités",
        "formations": "Formations",
        "media": "Médias",
        "volunteering": "Bénévolat",
        "contact": "Contact",
        "join_us": "Rejoignez-nous",
    }


def localized_value(obj, field, lang=None):
    if obj is None:
        return ""
    
    attrs = []
    if lang:
        attrs.append(f"{field}_{lang}")
    attrs.extend([f"{field}_fr", field])
    
    for attr in attrs:
        if hasattr(obj, attr):
            value = getattr(obj, attr)
            if value not in (None, "", [], {}):
                return clean_display_text(value)
    return ""


def localize_object(obj, fields, lang=None):
    if obj is None:
        return obj
    for field in fields:
        val = localized_value(obj, field, lang)
        setattr(obj, field, val)
        setattr(obj, f"{field}_localized", val)
    return obj


def localize_queryset(items, fields, lang=None):
    return [localize_object(item, fields, lang) for item in items]
