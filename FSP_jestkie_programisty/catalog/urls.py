from django.urls import path, register_converter

from catalog import converters, views

register_converter(converters.Positive, 'pn')

app_name = 'catalog'

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('<int:pk>/', views.item_detail, name='item_detail'),
]
