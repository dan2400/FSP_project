import django.contrib
from django.core.mail import send_mail
from django.shortcuts import redirect, render, reverse

import feedback.forms


def index(request):
    feedback_form = feedback.forms.FeedbackForm(request.POST or None)
    files_form = feedback.forms.FeedbackFileForm(request.POST or None)
    context = {
        'feedback_form': feedback_form,
        'files_form': files_form,
    }

    forms = (feedback_form, files_form)

    if request.method == 'POST' and all(form.is_valid() for form in forms):
        send_mail(
            f'Привет {feedback_form.cleaned_data["name"]}',
            f'{feedback_form.cleaned_data["text"]}',
            django.conf.settings.MAIL,
            [feedback_form.cleaned_data['mail']],
            fail_silently=True,
        )
        feedback_item = feedback.models.Feedback.objects.create(
            **feedback_form.cleaned_data,
        )
        feedback_item.save()
        for file in request.FILES.getlist(
            feedback.models.FeedbackFile.file.field.name,
        ):
            feedback.models.FeedbackFile.objects.create(
                file=file,
                feedback=feedback_item,
            )

        django.contrib.messages.success(
            request,
            'Фидбек отправлен. Спасибо!',
        )
        return redirect(
            reverse('feedback:feedback'),
        )

    return render(
        request,
        'feedback/feedback.html',
        context,
    )


__all__ = [
    'feedback',
]
