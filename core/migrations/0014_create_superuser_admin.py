from django.db import migrations


def create_or_update_superuser(apps, schema_editor):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Create or update 'Admin' user
    user, _ = User.objects.get_or_create(username='Admin')
    user.is_superuser = True
    user.is_staff = True
    user.is_active = True
    user.set_password('root')
    user.save()

    # Also update 'hp' user if present in database
    try:
        hp = User.objects.get(username='hp')
        hp.set_password('root')
        hp.is_superuser = True
        hp.is_staff = True
        hp.is_active = True
        hp.save()
    except User.DoesNotExist:
        pass


def reverse_superuser(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_userprofile'),
    ]

    operations = [
        migrations.RunPython(create_or_update_superuser, reverse_code=reverse_superuser),
    ]
