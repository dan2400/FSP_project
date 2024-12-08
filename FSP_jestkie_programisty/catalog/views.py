import django.db.models
from django.shortcuts import render

import catalog.models


def item_list(request):
    template = 'catalog/item_list.html'
    items = catalog.models.Competition.objects.published()
    context = {
        'items': items,
    }

    return render(request, template)


def item_detail(request, pk):
    template = 'catalog/item_detail.html'
    queryset = catalog.models.Competition.objects.published()

    item = django.shortcuts.get_object_or_404(queryset, pk=pk)
    try:
        regcomp = catalog.models.RegionalCompetition.objects.get(competition=pk)
    except catalog.models.RegionalCompetition.Content.DoesNotExist:
        regcomp = 'Не проходит'
        date = regcomp.date.strftime("%Y-%m-%d %H:%M:%S")  # или другой формат
    try:
         natcomp = catalog.models.NationwideCompetition.objects.get(competition=pk)
    except catalog.models.NationwideCompetition.Content.DoesNotExist:
        natcomp = 'Не проходит'
        date = natcomp.date.strftime("%Y-%m-%d %H:%M:%S")  # или другой формат
    context = {
        'item': item,
        'regcomp': regcomp,
        'natcomp': natcomp,
        'datetime': date,
    }
    return render(request, template, context)


__all__ = [
    'item_list',
    'item_detail',
]
