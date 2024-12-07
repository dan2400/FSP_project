import django.contrib.admin
import django.contrib.auth.admin
import login.models


class ProfileInlined(django.contrib.admin.TabularInline):
    model = login.models.Profile
    can_delete = False


class LoginFiles(django.contrib.admin.TabularInline):

    model = login.models.LoginFile
    fields = (login.models.LoginFile.file.field.name,)



class UserAdmin(django.contrib.auth.admin.UserAdmin):
    inlines = (
        ProfileInlined,
        LoginFiles,
    )


django.contrib.admin.site.unregister(
    django.contrib.auth.models.User,
)
django.contrib.admin.site.register(
    django.contrib.auth.models.User,
    UserAdmin,
)
