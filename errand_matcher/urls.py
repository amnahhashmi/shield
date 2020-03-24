from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/volunteer/', views.signup_volunteer, name='signup_volunteer')
]