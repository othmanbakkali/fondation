from django.contrib import admin

from .models import (
    ContactMessage,
    ContentItem,
    FormationRegistration,
    PageContent,
    Partner,
    SiteSetting,
    VolunteerApplication,
)


@admin.register(ContentItem)
class ContentItemAdmin(admin.ModelAdmin):
    list_display = ("title", "module", "category", "status", "order", "featured", "updated_at")
    list_filter = ("module", "status", "category", "featured")
    search_fields = ("title", "title_fr", "title_ar", "title_en", "summary", "summary_fr", "summary_ar", "summary_en", "body")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ("slug", "title", "status", "updated_at")
    list_filter = ("status",)
    search_fields = ("slug", "title", "title_fr", "title_ar", "title_en", "content")


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "partner_type", "status", "order", "featured_home")
    list_filter = ("status", "partner_type", "featured_home")
    search_fields = ("name", "name_fr", "name_ar", "name_en", "description")


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("key", "group", "updated_at")
    list_filter = ("group",)
    search_fields = ("key", "value", "value_fr", "value_ar", "value_en")


admin.site.register(ContactMessage)
admin.site.register(VolunteerApplication)
admin.site.register(FormationRegistration)
