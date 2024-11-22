from django.urls import path

from main import views

app_name = 'main'

urlpatterns = [
    path('', views.main, name='main'),
    path('coffee/', views.coffee, name='coffee'),
]
