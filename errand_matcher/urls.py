from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('volunteer', views.begin_signup, name='begin_signup'),
    path('signup', views.complete_signup, name='complete_signup'),
]