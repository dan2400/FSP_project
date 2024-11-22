import http

from django.http import HttpResponse
from django.shortcuts import render




def main(request):
    template = 'main/index.html'
    context = {
        'items': [],
    }
    return render(request, template, context)


def coffee(request):
    return HttpResponse('Я чайник', status=http.HTTPStatus.IM_A_TEAPOT)


__all__ = [
    'main',
    'coffee',
]
