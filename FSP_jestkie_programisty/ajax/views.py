from django.shortcuts import render

import ajax.models
from mako.filters import xml_escape


def chat(request):
    template = 'ajax/chat.html'
    item = ajax.models.Chat.objects.get()xml_escape()
    return render(request, template)


__all__ = [
    'description',
]
