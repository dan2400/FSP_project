import django.contrib.auth.forms
import django.forms

import login.models


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class UserCreationForm(
    BootstrapFormMixin,
    django.contrib.auth.forms.UserCreationForm,
):
    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = login.models.User
        fields = (
            login.models.User.email.field.name,
            login.models.User.username.field.name,
        )


class UserChangeForm(
    BootstrapFormMixin,
    django.contrib.auth.forms.UserCreationForm,
):
    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        fields = (
            login.models.User.first_name.field.name,
            login.models.User.last_name.field.name,
        )


class UpdateProfileForm(
    BootstrapFormMixin,
    django.forms.ModelForm,
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields(
            login.models.Profile.mass.field.name
        ).disabled = True