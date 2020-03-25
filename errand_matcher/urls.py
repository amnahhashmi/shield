from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('requirements', views.requirements, name='requirements')
]