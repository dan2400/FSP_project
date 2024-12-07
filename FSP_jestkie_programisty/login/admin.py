import django.contrib.admin
import django.contrib.auth.admin
import login.models


class ProfileInlined(django.contrib.admin.TabularInline):
    model = login.models.Profile
    can_delete = False


class UserAdmin(django.contrib.auth.admin.UserAdmin):
    inlines = (ProfileInlined,)


django.contrib.admin.site.unregister(
    django.contrib.auth.models.User,
)
django.contrib.admin.site.register(
    django.contrib.auth.models.User,
    UserAdmin,
)
