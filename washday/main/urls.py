from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('pages/login', views.clientlogin, name='clientlogin'),
    path('register', views.register, name='register'),
    path('my_washday-hero', views.client_dashboard, name='dashboard'),
    path('place-order', views.new_order, name='new_order'),
    path('profile', views.profile, name='profile'),
    path('help-center', views.help_center, name='help_center'),
    path('billing', views.billing, name='billing'),
    path('mybag', views.bag, name='mybag'),
    path('logout', views.Logout, name='logout'),
    path('my_washday-hero/<str:orderID>', views.view_bag, name='view_bag'),
    path('pages/terms-of-service', views.terms, name='terms'),
    path('pages/privacy-policy', views.privacy_policy, name='privacy_policy'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
