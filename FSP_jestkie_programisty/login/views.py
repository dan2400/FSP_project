from certifi import contents
from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
import django.contrib.messages
import django.contrib.auth.decorators
import django.utils
import login.models
import login.forms
import datetime


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
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    if (
        request.method == 'POST'
        and user_form.is_valid()
        and profile_form.is_valid()
    ):
        user_form.save()
        profile_form.save()
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
        user = login.models.AddRequest(email=form.cleaned_data["email"])
        send_mail(
            f'Привет {form.cleaned_data["username"]}',
            f'Перейдите по ссылке:/n auth/confirm/{user.id}',
            django.conf.settings.MAIL,
            [form.cleaned_data['email']],
            fail_silently=True,
        )
        user.save()
        django.contrib.messages.success(
            request,
            'Запрос отправлен. Спасибо!',
        )
        return redirect(
            reverse('auth:login'),
        )
    return render(request, template, context)

def accept(request):
    template = 'registration/done.html'

