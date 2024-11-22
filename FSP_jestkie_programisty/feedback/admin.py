import django.contrib.admin

import feedback.models


class FeedbackFiles(django.contrib.admin.TabularInline):

    model = feedback.models.FeedbackFile
    fields = (feedback.models.FeedbackFile.file.field.name,)


@django.contrib.admin.register(feedback.models.Feedback)
class FeedbackAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        feedback.models.Feedback.text.field.name,
        feedback.models.Feedback.status.field.name,
        feedback.models.Feedback.name.field.name,
        feedback.models.Feedback.mail.field.name,
    )
    inlines = (
        FeedbackFiles,
    )


__all__ = [
    'FeedbackAdmin',
    'FeedbackAuther',
    'FeedbackFiles',
]
