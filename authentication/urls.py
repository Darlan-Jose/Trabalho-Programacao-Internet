from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admincar/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dealer/dashboard/', views.dealer_dashboard, name='dealer_dashboard'),
    path('dealer/vehicles/', views.dealer_vehicles, name='dealer_vehicles'),
    # NOVAS URLs PÚBLICAS
    path('public/dealers/', views.public_dealers, name='public_dealers'),
    path('public/vehicles/', views.public_all_vehicles, name='public_all_vehicles'),
    path('dealer/vehicles/search/', views.search_vehicles, name='search_vehicles'),
    path('public/dealer/<str:dealer_id>/vehicles/', views.public_dealer_vehicles, name='public_dealer_vehicles'),
    path('public/dealer/<str:dealer_id>/purchase/<int:vehicle_id>/', 
         views.purchase_vehicle, name='purchase_vehicle'),
    path('public/purchase/success/<str:purchase_code>/', 
         views.purchase_success, name='purchase_success'),
     #APIs
    path('api/dealers/public/', views.api_public_dealers, name='api-public-dealers'),
    path('api/vehicles/public/', views.api_public_vehicles, name='api-public-vehicles'),
    path('api/purchase/', views.api_purchase_vehicle, name='api-purchase'),
    path('api/purchase/<str:purchase_code>/', views.api_purchase_detail, name='api-purchase-detail'),
    path('api/dealer/stats/', views.api_dealer_stats, name='api-dealer-stats'),
    path('api/cep/<str:cep>/', views.api_search_cep, name='api-search-cep'),
]