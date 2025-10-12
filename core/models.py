from django.db import models
from django.contrib.auth.models import User

class Doktor(models.Model):
    class Kidem(models.TextChoices):
        ACEMI = 'ACEMI', 'Acemi'
        ORTA_KIDEMLI = 'ORTA_KIDEMLI', 'Orta Kıdemli'
        KIDEMLI = 'KIDEMLI', 'Kıdemli'

    # Django'nun hazır kullanıcı sistemiyle doktoru eşleştirelim
    # Bu bize kullanıcı girişi gibi özellikleri hazır olarak sunar
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Kullanıcı Hesabı")
    ad_soyad = models.CharField(max_length=100, verbose_name="Adı Soyadı")
    kidem = models.CharField(max_length=20, choices=Kidem.choices, verbose_name="Kıdem")

    def __str__(self):
        return f"Dr. {self.ad_soyad} ({self.get_kidem_display()})"

    class Meta:
        verbose_name = "Doktor"
        verbose_name_plural = "Doktorlar"

class IzinTalebi(models.Model):
    doktor = models.ForeignKey(Doktor, on_delete=models.CASCADE, related_name="izin_talepleri")
    tarih = models.DateField(verbose_name="İzin İstenen Tarih")

    def __str__(self):
        return f"{self.doktor.ad_soyad} - {self.tarih.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "İzin Talebi"
        verbose_name_plural = "İzin Talepleri"
        # Bir doktorun aynı gün için birden fazla izin talebi oluşturmasını engelle
        unique_together = ('doktor', 'tarih')


class Nobet(models.Model):
    class Bolum(models.TextChoices):
        YESIL = 'YESIL', 'Yeşil Alan'
        SARI = 'SARI', 'Sarı Alan'
        KIRMIZI = 'KIRMIZI', 'Kırmızı Alan'
        YEDEK = 'YEDEK', 'Yedek/Diğer'

    doktor = models.ForeignKey(Doktor, on_delete=models.CASCADE, related_name="nobetleri")
    tarih = models.DateField(verbose_name="Nöbet Tarihi")
    bolum = models.CharField(max_length=20, choices=Bolum.choices, verbose_name="Atandığı Bölüm")
    
    # Zorunlu atama durumunu takip etmek için eklenen alan
    izin_iptal_edildi = models.BooleanField(
        default=False, 
        verbose_name="İzin İptal Edilerek Mi Atandı?"
    )

    def __str__(self):
        zorunlu_notu = " (Zorunlu)" if self.izin_iptal_edildi else ""
        return f"{self.tarih.strftime('%Y-%m-%d')} - {self.doktor.ad_soyad} [{self.get_bolum_display()}]{zorunlu_notu}"

    class Meta:
        verbose_name = "Nöbet"
        verbose_name_plural = "Nöbet Takvimi"
        unique_together = ('doktor', 'tarih')
        
# YENİ EKLENECEK MODEL
class HastaneAyarlari(models.Model):
    gunluk_doktor_sayisi = models.PositiveIntegerField(
        default=4, 
        verbose_name="Günlük Nöbetçi Doktor Sayısı"
    )
    minimum_dinlenme_gunu = models.PositiveIntegerField(
        default=2, 
        verbose_name="İki Nöbet Arası Minimum Dinlenme Günü"
    )
    aylik_izin_limiti = models.PositiveIntegerField(
        default=4, 
        verbose_name="Aylık Maksimum İzin Günü Limiti"
    )

    class Meta:
        verbose_name = "Hastane Ayarları"
        verbose_name_plural = "Hastane Ayarları"

    def __str__(self):
        return "Genel Hastane Ayarları"

    # Bu yardımcı fonksiyon, ayarlara her yerden kolayca erişmemizi sağlayacak
    @staticmethod
    def get_solo():
        obj, created = HastaneAyarlari.objects.get_or_create(pk=1)
        return obj