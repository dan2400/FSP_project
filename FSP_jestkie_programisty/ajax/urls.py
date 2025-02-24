from django.urls import path, register_converter

from ajax import views

app_name = 'ajax'

urlpatterns = [
    path('', views.chat, name='chat'),
]
