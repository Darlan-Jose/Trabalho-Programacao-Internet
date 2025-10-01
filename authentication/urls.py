from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admincar/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dealer/dashboard/', views.dealer_dashboard, name='dealer_dashboard'),
]