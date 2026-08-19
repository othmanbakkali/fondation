from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("من-نحن/", views.about, name="arabic_about_alias"),
    path("من نحن/", views.about, name="arabic_about_space_alias"),
    path("الرئيسية/", views.home, name="arabic_home_alias"),
    path("البرنامج/", views.programme, name="arabic_programme_alias"),
    path("الأنشطة/", views.activites, name="arabic_activites_alias"),
    path("الأخبار/", views.actualites, name="arabic_actualites_alias"),
    path("التكوينات/", views.formations, name="arabic_formations_alias"),
    path("الوسائط/", views.medias, name="arabic_medias_alias"),
    path("التطوع/", views.benevolat, name="arabic_benevolat_alias"),
    path("اتصل-بنا/", views.contact, name="arabic_contact_alias"),
    path("اتصل بنا/", views.contact, name="arabic_contact_space_alias"),
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("activites/", views.activites, name="activites"),
    path("actualites/", views.actualites, name="actualites"),
    path("formations/", views.formations, name="formations"),
    path("formations/<int:formation_id>/register/", views.register_formation, name="register_formation"),
    path("activites/<int:activity_id>/register/", views.register_activity, name="register_activity"),
    path("medias/", views.medias, name="medias"),
    path("benevolat/", views.benevolat, name="benevolat"),
    path("contact/", views.contact, name="contact"),
    path("programme/", views.programme, name="programme"),
]
