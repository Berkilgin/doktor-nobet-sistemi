from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # --- Giriş/Çıkış URL'leri ---
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # --- Doktor Paneli URL'leri ---
    # /panel/ isteğini o anki ayın paneline yönlendirir
    path('panel/', views.doktor_paneli_redirect, name='doktor_paneli_redirect'), 
    # Belirli bir ayın panelini gösterir, örn: /panel/2025/10/
    path('panel/<int:yil>/<int:ay>/', views.doktor_paneli, name='doktor_paneli'),
    # Belirli bir izni siler
    path('panel/izin-sil/<int:izin_id>/', views.izin_sil, name='izin_sil'),

    # --- Takvim URL'leri ---
    # /takvim/ isteğini o anki ayın takvimine yönlendirir
    path('takvim/', views.takvim_redirect, name='takvim_redirect'),
    # Belirli bir ayın takvimini gösterir, örn: /takvim/2025/11/
    path('takvim/<int:yil>/<int:ay>/', views.takvim_gorunumu, name='takvim_gorunumu'),
    # Belirli bir ayın takvimini Excel olarak dışa aktarır
    path('takvim/export/<int:yil>/<int:ay>/', views.export_takvim_excel, name='export_takvim_excel'),

    # --- Yönetim Paneli URL'si ---
    path('yonetim/', views.yonetim_paneli, name='yonetim_paneli'),

    # --- Ana Sayfa URL'si ---
    # Ana dizine gelen isteği o anki ayın paneline yönlendirir
    path('', views.doktor_paneli_redirect, name='home'),
]