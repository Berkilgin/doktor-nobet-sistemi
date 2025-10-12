from django.contrib import admin
from django.urls import path, include # include'ı buraya ekleyin

urlpatterns = [
    path('admin/', admin.site.urls),
    # Ana sayfa ve diğer tüm core bağlantıları için gelen istekleri
    # core uygulamasının kendi urls.py dosyasına yönlendir.
    path('', include('core.urls')),
]