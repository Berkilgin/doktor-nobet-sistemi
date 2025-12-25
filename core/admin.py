from django.contrib import admin
from .models import Doktor, Nobet, IzinTalebi, HastaneAyarlari

# 1. DOKTOR YÖNETİMİ
@admin.register(Doktor)
class DoktorAdmin(admin.ModelAdmin):
    list_display = ('ad_soyad', 'kidem', 'user') # Listede görünecekler
    list_filter = ('kidem',) # Yan menüde filtreleme
    search_fields = ('ad_soyad',) # Arama kutusu

# 2. İZİN TALEPLERİ YÖNETİMİ
@admin.register(IzinTalebi)
class IzinTalebiAdmin(admin.ModelAdmin):
    # Modelinde 'durum' alanı olmadığı için sadece kim ve ne zaman olduğunu gösteriyoruz.
    list_display = ('doktor', 'tarih')
    list_filter = ('doktor',)
    ordering = ('-tarih',)

# 3. NÖBET TAKVİMİ YÖNETİMİ
@admin.register(Nobet)
class NobetAdmin(admin.ModelAdmin):
    list_display = ('tarih', 'doktor', 'bolum', 'izin_iptal_edildi')
    list_filter = ('bolum', 'tarih', 'izin_iptal_edildi')
    date_hierarchy = 'tarih' # Tarihe göre hızlı gezinti çubuğu ekler

# 4. HASTANE AYARLARI (YENİ)
@admin.register(HastaneAyarlari)
class HastaneAyarlariAdmin(admin.ModelAdmin):
    # Listede ayarların özetini gösterelim
    list_display = (
        '__str__', 
        'kirmizi_alan_doktor_sayisi', 
        'sari_alan_doktor_sayisi', 
        'yesil_alan_doktor_sayisi',
        'aylik_izin_limiti'
    )
    
    # Hastane ayarlarından sadece 1 tane olması gerektiği için
    # eğer içeride bir ayar varsa "Ekle" butonunu gizleyen özel fonksiyon:
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return True