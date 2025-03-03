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
    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        model = login.models.User

        fields = (
            login.models.User.email.field.name,
            login.models.User.username.field.name,
        )


class UserChangeForm(
    BootstrapFormMixin,
    django.contrib.auth.forms.UserChangeForm,
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
            login.models.Profile.attempts_count.field.name,
        ).disabled = True

        class Meta:
            model = login.models.Profile
            fields = (
            login.models.Profile.image.field.name,
            )


class LoginFileForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LoginFileForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-cntrol'

    class Meta:
        model = login.models.LoginFile

        fields = (login.models.LoginFile.file.field.name,)
        help_text = {
            login.models.LoginFile.file.field.name: (
                'При необходимоти прикрепите файлы'
            ),
        }
        widgets = {
            login.models.LoginFile.file.field.name: (
                django.forms.FileInput(
                    attrs={
                        'class': 'form-control',
                        'type': 'file',
                        'allow_multiple_selected': True,
                    },
                )
            ),
        }
