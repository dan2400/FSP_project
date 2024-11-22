from django.shortcuts import render


def description(request):
    template = 'about/about.html'
    return render(request, template)


__all__ = [
    'description',
]
