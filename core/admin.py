from django.contrib import admin
from .models import Doktor, IzinTalebi, Nobet, HastaneAyarlari

@admin.register(Doktor)
class DoktorAdmin(admin.ModelAdmin):
    # Doktor listesinde hangi bilgilerin görüneceğini belirtir
    list_display = ('ad_soyad', 'kidem', 'user')
    # Kıdeme göre filtreleme kutucuğu ekler
    list_filter = ('kidem',)
    # İsme göre arama çubuğu ekler
    search_fields = ('ad_soyad',)

@admin.register(IzinTalebi)
class IzinTalebiAdmin(admin.ModelAdmin):
    list_display = ('doktor', 'tarih')
    list_filter = ('tarih', 'doktor')

@admin.register(Nobet)
class NobetAdmin(admin.ModelAdmin):
    list_display = ('tarih', 'doktor', 'bolum')
    list_filter = ('tarih', 'bolum', 'doktor')

@admin.register(HastaneAyarlari)
class HastaneAyarlariAdmin(admin.ModelAdmin):
    # Bu modelin listelenmesini veya silinmesini istemiyoruz, sadece tek bir tane olmalı
    def has_add_permission(self, request):
        return not HastaneAyarlari.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False