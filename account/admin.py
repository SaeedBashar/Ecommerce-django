from django.contrib import admin

from django.contrib.auth.models import Group  # Import the Group model

# Unregister the Group model from the admin site
admin.site.unregister(Group)
# Register your models here.
