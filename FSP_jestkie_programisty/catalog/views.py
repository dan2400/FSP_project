import django.db.models
from django.shortcuts import render

import catalog.models


def item_list(request):
    template = 'catalog/item_list.html'
#    items = catalog.models.Item.objects.published()
#    context = {
#        'items': items,
#    }

    return render(request, template)


def item_detail(request, pk):
    template = 'catalog/item_detail.html'
#    queryset = catalog.models.Item.objects.published().prefetch_related(
#        prefetched(),
#    )

#    item = django.shortcuts.get_object_or_404(queryset, pk=pk)
#    context = {
#        'item': item,
#    }
    return render(request, template)


__all__ = [
    'item_list',
    'item_detail',
]
