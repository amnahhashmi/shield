from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='index'),
    path('404', views.error, name='error'),
    path('health', views.health_and_safety, name='health_and_safety'),
    path('volunteer', views.volunteer, name='volunteer'),
    path('volunteer/signup', views.volunteer_signup, name='volunteer_signup'),
    path('volunteer/login', views.volunteer_login, name='volunteer_login'),
    path('requestor', views.requestor, name='requestor'),
    path('requestor/signup', views.requestor_signup, name='requestor_signup'),
    path('requestor/login', views.requestor_login, name='requestor_login'),
    path('partner/', views.partner, name='partner'),
    path('partner/dashboard/', views.partner_dashboard, name='partner_dashboard'),
    path('partner/request/', views.partner_request, name='partner_request'),
    path('partner/password_reset/', views.partner_password_reset, name='partner_password_reset'),
    path('partner/password_reset/done/', views.partner_password_reset_done, name='partner_password_reset_done'),
    path('partner/reset/<uuid:token>', views.partner_reset_confirm, name='partner_password_reset_confirm'),
    path('partner/reset/done', views.partner_reset_complete, name='partner_password_complete'),
    path('errand', views.request_errand, name='request_errand'),
    path('errand/<int:errand_id>/accept/<int:volunteer_number>', views.accept_errand, name='accept_errand'),
    path('errand/<int:errand_id>/status/<uuid:access_id>', views.view_errand, name='view_errand'),
    path('sms', views.sms_inbound, name='sms_inbound'),
]