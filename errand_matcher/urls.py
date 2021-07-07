from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='index'),
    path('404', views.error, name='error'),
    path('health', views.health_and_safety, name='health_and_safety'),
    path('volunteer/signup/', views.volunteer_signup, name='volunteer_signup'),
    path('volunteer/signup/done', views.volunteer_signup_done, name='volunteer_signup_done'),
    path('volunteer/login/', views.volunteer_login, name='volunteer_login'),
    path('volunteer/login/otp', views.volunteer_login_otp, name='volunteer_login_otp'),
    path('volunteer/dashboard/', views.volunteer_dashboard, name='volunteer_dashboard'),
    path('volunteer/signout/', views.volunteer_signout, name='volunteer_signout'),
    path('requestor/', views.requestor, name='requestor'),
    path('requestor/signup/', views.requestor_signup, name='requestor_signup'),
    path('requestor/login/', views.requestor_login, name='requestor_login'),
    path('requestor/login/otp', views.requestor_login_otp, name='requestor_login_otp'),
    path('partner/', views.partner, name='partner'),
    path('partner/setup/', views.partner_setup, name='partner_setup'),
    path('partner/signout/', views.partner_signout, name='partner_signout'),
    path('partner/dashboard/', views.partner_dashboard, name='partner_dashboard'),
    path('partner/request/', views.partner_request, name='partner_request'),
    path('partner/request/delete/<int:errand_id>', views.partner_request_delete, name='partner_request_delete'),
    path('partner/password_reset/', views.partner_password_reset, name='partner_password_reset'),
    path('partner/password_reset/done/', views.partner_password_reset_done, name='partner_password_reset_done'),
    path('partner/reset/<uidb64>/<token>', views.partner_password_reset_confirm, name='partner_password_reset_confirm'),
    path('errand', views.request_errand, name='request_errand'),
    path('errand/<int:errand_id>/accept/<int:volunteer_number>', views.accept_errand, name='accept_errand'),
    path('errand/<int:errand_id>/status/<uuid:access_id>', views.view_errand, name='view_errand'),
    path('errand/<int:errand_id>/complete/<uuid:access_id>', views.complete_errand, name='complete_errand'),
    path('sms', views.sms_inbound, name='sms_inbound'),
]