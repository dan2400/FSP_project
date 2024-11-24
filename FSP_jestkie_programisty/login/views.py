from django.shortcuts import render


def profile(request):
    template = 'main/index.html'
    context = {
        'items': [],
    }
    return render(request, template, context)

def signup(request):
    template = 'main/index.html'
    context = {
        'items': [],
    }
    return render(request, template, context)