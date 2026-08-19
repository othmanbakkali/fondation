from core.models import ContactMessage, ContentItem, VolunteerApplication, FormationRegistration, ActivityRegistration


def dashboard_notifications(request):
    unread_messages = ContactMessage.objects.filter(status="non_lu")
    pending_volunteers = VolunteerApplication.objects.filter(status="en_attente")
    pending_content = ContentItem.objects.filter(status__in=["brouillon", "programme", "en_attente"])
    pending_formations_regs = FormationRegistration.objects.filter(status="en_attente")
    pending_activities_regs = ActivityRegistration.objects.filter(status="en_attente")
    
    latest_messages = unread_messages.order_by("-created_at")[:3]
    total = (
        unread_messages.count() 
        + pending_volunteers.count() 
        + pending_content.count()
        + pending_formations_regs.count()
        + pending_activities_regs.count()
    )
    return {
        "dashboard_notification_total": total,
        "dashboard_unread_messages_count": unread_messages.count(),
        "dashboard_pending_volunteers_count": pending_volunteers.count(),
        "dashboard_pending_content_count": pending_content.count(),
        "dashboard_pending_formations_registrations_count": pending_formations_regs.count(),
        "dashboard_pending_activities_registrations_count": pending_activities_regs.count(),
        "dashboard_latest_unread_messages": latest_messages,
    }
