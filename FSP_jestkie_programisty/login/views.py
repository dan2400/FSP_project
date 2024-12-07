from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
import django.core.mail
from django.contrib.auth import authenticate, login, logout
import django.contrib.messages
import django.contrib.auth.decorators
import django.utils
import login.models
import login.forms
import datetime
import django.conf


def user_detail(request, pk: int):
    search_user = django.shortcuts.get_object_or_404(
        login.models.User.objects.active(),
        pk=pk,
    )

    context = {'user': search_user}

    return render(request, 'registration/user_detail.html', context)

def user_list(request):
    context = {'users': login.models.User.object.activate()}

    return render(request, 'registration/user_list.html', context)

def reactivate(request, pk):
    user = login.models.User.objects.get(pk=pk)
    if (
        login.profile.block_date + datetime.timedelta(days=7)
        > django.utils.timezone.now()
    ):
        user.is_activate = True
        user.save()
    return redirect(reverse('main:main'))

@django.contrib.auth.decorators.login_required
def profile(request):
    user_form = login.forms.UserChangeForm(
        request.POST or None,
        instance=request.user,
    )

    profile_form = login.forms.UpdateProfileForm(
        request.POST or None,
        instance=request.user.profile,
    )

    file_form = login.forms.LoginFileForm(
        request.POST or None,
        instance=request.user,
    )

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'file_form': file_form,
    }

    if (
        request.method == 'POST'
        and user_form.is_valid()
        and profile_form.is_valid()
        and file_form.is_valid()
    ):
        user_form.save()
        profile_form.save()
        file_form.save()
        django.contrib.messages.success(request, 'Изменения сохранены')
        return redirect(reverse('auth:profile'))
    return render(request, 'registration/profile.html', context)

def signup(request):
    form = login.forms.UserCreationForm(request.POST or None)
    template = 'registration/signup.html'
    context = {
        'form': form,
    }

    if request.method == 'POST' and form.is_valid():
        code = login.models.AddRequest(email=form.cleaned_data["email"])
        user = login.models.User(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            is_active=False,
        )
        user.set_password(form.cleaned_data['password1'])
        user.save()
        send_mail(
            f'Привет {form.cleaned_data["username"]}',
            f'Перейдите по ссылке для подтверждения пароля: 109.195.243.60:5003/auth/confirm/{user.id}',
            django.conf.settings.MAIL,
            [form.cleaned_data['email']],
            fail_silently=False,
        )
        code.save()
        django.contrib.messages.success(
            request,
            'Запрос отправлен. Спасибо!',
        )
        return redirect(
            reverse('auth:login'),
        )
    return render(request, template, context)

def confirm(request, pk: int):
    user = django.shortcuts.get_object_or_404(login.models.User, pk=pk)
    user.is_active = True
    user.save()
    return redirect(reverse('auth:login'))

