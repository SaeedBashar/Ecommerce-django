from django.contrib import admin

from django.contrib.auth.models import Group  # Import the Group model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class CustomUserAdmin(UserAdmin):
    # Add the fields you want to include in the user creation form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active'),
        }),
    )

# Register the User model with the custom UserAdmin class
admin.site.unregister(User)  # Unregister the default UserAdmin
admin.site.register(User, CustomUserAdmin)

# Unregister the Group model from the admin site
admin.site.unregister(Group)
# Register your models here.
