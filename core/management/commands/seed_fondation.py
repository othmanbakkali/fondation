
from datetime import date, time
from django.core.management.base import BaseCommand
from core.models import ContentItem, PageContent, Partner, SiteSetting, VolunteerApplication, ContactMessage


class Command(BaseCommand):
    help = "Seed realistic Fondation Tanger Métropole content in MySQL."

    def handle(self, *args, **options):
        pages = {
            "accueil": ("Fondation Tanger Métropole", "Bâtir des ponts entre les talents, la culture et l'avenir de Tanger."),
            "a-propos": ("À propos", "Une fondation engagée pour l'éducation, la culture, le social et le sport dans le Grand Tanger."),
            "activites": ("Activités", "Toutes les actions terrain portées par la Fondation Tanger Métropole."),
            "actualites": ("Actualités", "Dernières nouvelles, communiqués, formations et concours."),
            "formations": ("Nos formations", "Développez vos compétences grâce aux formations proposées par la Fondation."),
            "medias": ("Médias", "Photos, vidéos, albums et documents de la Fondation."),
            "benevolat": ("Bénévolat", "Rejoignez les bénévoles qui transforment Tanger par l'action."),
            "contact": ("Contact", "Contactez la Fondation Tanger Métropole."),
        }
        for slug, (title, subtitle) in pages.items():
            PageContent.objects.update_or_create(slug=slug, defaults={"title": title, "subtitle": subtitle, "content": subtitle, "status": "publie"})

        for key, value in {"stats_beneficiaires": "12500", "site_phone": "+212 5 39 00 00 00", "site_email": "contact@tangermetropole.ma"}.items():
            SiteSetting.objects.update_or_create(key=key, defaults={"value": value, "group": "general"})

        for i, (name, ptype, url) in enumerate([
            ("Commune de Tanger", "Institutionnel", "https://www.tanger.ma"),
            ("Université Abdelmalek Essaâdi", "Académique", "https://www.uae.ac.ma"),
            ("Centre culturel de Tanger", "Culture", "https://culture.example.ma"),
            ("Association Médina", "Associatif", "https://medina.example.ma"),
        ], 1):
            Partner.objects.update_or_create(name=name, defaults={"partner_type": ptype, "url": url, "order": i, "status": "actif", "featured_home": True})

        def item(module, title, **kw):
            defaults = {
                "category": kw.get("category", ""),
                "summary": kw.get("summary", ""),
                "body": kw.get("body", kw.get("summary", "")),
                "image_url": kw.get("image_url", "https://placehold.co/700x450/062B4F/FFFFFF?text=Fondation"),
                "date": kw.get("date"),
                "status": kw.get("status", "publie"),
                "order": kw.get("order", 1),
                "featured": kw.get("featured", False),
                "author": kw.get("author", "Fondation Tanger Métropole"),
                "location": kw.get("location", "Tanger"),
                "participants": kw.get("participants", 0),
                "reports_count": kw.get("reports_count", 0),
                "video_url": kw.get("video_url", ""),
                "facebook_url": kw.get("facebook_url", ""),
                "instagram_url": kw.get("instagram_url", ""),
                "youtube_url": kw.get("youtube_url", ""),
                "instructor_name": kw.get("instructor_name", ""),
                "start_date": kw.get("start_date"),
                "end_date": kw.get("end_date"),
                "start_time": kw.get("start_time"),
                "end_time": kw.get("end_time"),
                "total_seats": kw.get("total_seats", 0),
                "registered_seats": kw.get("registered_seats", 0),
                "reading_time": kw.get("reading_time", 3),
            }
            ContentItem.objects.update_or_create(module=module, title=title, defaults=defaults)

        item("news", "Lancement du programme Tanger Lit", category="formations", summary="Ateliers de lecture dans les écoles de la médina pour 500 enfants.", image_url="https://images.unsplash.com/photo-1590073242678-70ee3fc28f8e?w=800&h=500&fit=crop", date=date(2026, 8, 15), featured=True, order=1)
        item("news", "Exposition Mémoires du Détroit", category="actualites", summary="Vernissage au Palais Moulay Hafid avec des artistes locaux.", image_url="https://images.unsplash.com/photo-1519999482648-25049ddd37b1?w=800&h=500&fit=crop", date=date(2026, 8, 22), order=2)
        item("news", "Concours des jeunes talents 2026", category="concours", summary="Un concours pour valoriser la créativité des jeunes du Grand Tanger.", image_url="https://images.unsplash.com/photo-1531913764164-f85c3e01f9a2?w=800&h=500&fit=crop", date=date(2026, 7, 15), order=3)
        item("activity", "Tournoi sportif des jeunes", category="sport", summary="Une activité sportive destinée aux jeunes du Grand Tanger.", image_url="https://images.unsplash.com/photo-1461896836934-bd45ba22e0a4?w=600", date=date(2026, 7, 25), location="Complexe sportif Ibn Battouta", participants=150, reports_count=3, order=1)
        item("activity", "Atelier d'initiation au numérique", category="education", summary="Formation aux outils numériques pour les jeunes.", image_url="https://images.unsplash.com/photo-1531482615713-2afd69097998?w=600", date=date(2026, 6, 15), location="Centre culturel de Tanger", participants=80, reports_count=2, order=2)
        item("activity", "Campagne de solidarité sociale", category="social", summary="Distribution de kits alimentaires aux familles nécessiteuses.", image_url="https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=600", date=date(2026, 4, 20), location="Beni Makada", participants=500, reports_count=4, order=3)
        item("formation", "Initiation au développement web", category="numerique", summary="Une formation pratique pour découvrir HTML, CSS et JavaScript.", image_url="https://images.unsplash.com/photo-1531482615713-2afd69097998?w=600", start_date=date(2026, 8, 12), end_date=date(2026, 8, 14), start_time=time(10, 0), end_time=time(13, 0), instructor_name="Ahmed El Mansouri", location="Centre de rencontre des jeunes - Hay Kasbah", total_seats=30, registered_seats=22, order=1)
        item("formation", "Entrepreneuriat social", category="entrepreneuriat", summary="Apprenez à créer et gérer une entreprise à impact social.", image_url="https://images.unsplash.com/photo-1552664730-d307ca884978?w=600", start_date=date(2026, 8, 20), end_date=date(2026, 8, 22), start_time=time(9, 0), end_time=time(12, 0), instructor_name="Fatima Zahra Bennani", location="Chambre de commerce de Tanger", total_seats=25, registered_seats=23, order=2)
        item("program", "Éducation et réussite", category="Éducation", summary="Soutien scolaire, bourses et orientation pour les jeunes.", order=1)
        item("program", "Culture et patrimoine", category="Culture", summary="Valorisation du patrimoine tangérois et soutien aux artistes.", order=2)
        item("program", "Solidarité sociale", category="Social", summary="Actions de proximité pour les familles et quartiers prioritaires.", order=3)
        item("program", "Sport pour tous", category="Sport", summary="Événements et encadrement sportif pour les jeunes.", order=4)
        item("team", "Abdelouahed Boulaich", category="Président", summary="Président de la Fondation Tanger Métropole.", order=1)
        item("testimonial", "Meryem Chafik", category="Bénéficiaire", summary="La Fondation m'a aidée à retrouver confiance et à intégrer une formation utile.", reading_time=5, order=1)
        VolunteerApplication.objects.get_or_create(name="Imane Karimi", defaults={"city": "Tanger", "skills": "Animation, photo", "phone": "+212 6 11 24 90 10", "email": "imane@example.ma"})
        ContactMessage.objects.get_or_create(name="Hind El Fassi", email="hind@example.ma", defaults={"subject": "Demande partenariat", "message": "Bonjour, nous souhaitons proposer un partenariat local."})
        self.stdout.write(self.style.SUCCESS("Contenu Fondation Tanger Métropole initialisé dans MySQL."))
