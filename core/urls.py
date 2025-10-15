from django.urls import path
from . import views
from . views import *
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.http import HttpResponse
from .sitemaps import StaticViewSitemap

urlpatterns = [
    path('', views.index, name='index'),
    # path('home/', views.indexx, name='home'),
    path('stake/', views.stake, name='stake'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('terms/', views.terms, name='terms'),
    path('about/', views.about, name='about'),
    path('login/', login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('forgottenpassword/', views.forgottenpassword, name='forgottenpassword'),
    # path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('account/', views.account, name='account'),
    path('edit_account/', views.edit_account, name='edit_account'),
    path('deposit/', views.deposit, name='deposit'),
    path('referral/', views.referral, name='referral'),
    # path('password_reset_confirm/', views.password_reset_confirm, name='password_reset_confirm'),
    # path('deposit_list/', views.deposit_list, name='deposit_list'),
    path('security/', views.security, name='security'),
    # path('enable_tfa/', enable_tfa, name='enable_tfa'),
    path('withdrawal/', views.withdrawal, name='withdrawal'),
    # path('deposit_history/', views.deposit_history, name='deposit_history'),
    # path('earnings/', views.earnings, name='earnings'),
    path('history/', views.history, name='history'),
    # path('confirm_deposit/<int:deposit_id>/', confirm_deposit, name='confirm_deposit'),
    path('confirm_deposit/', views.confirm_deposit, name='confirm_deposit'),
    # path('confirm_deposit/<int:deposit_id>/', views.confirm_deposit, name='confirm_deposit'),
    # path('save_deposit_data/', views.save_deposit_data, name='save_deposit_data'),
    # path('qrcode/<str:secret_key>/', generate_qrcode, name='qrcode'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),  # Custom reset request
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),  # Done notification
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # Custom password reset confirm view
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),  # Custom complete view

    # Sitemap
    path('sitemap.xml', views.sitemap_view, name='sitemap'),
]


