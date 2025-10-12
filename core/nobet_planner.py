import calendar
from collections import defaultdict
from datetime import date, timedelta
import random

from .models import Doktor, Nobet, IzinTalebi, HastaneAyarlari 

class NobetPlanlayici:
    """
    Belirli bir ay için nöbet takvimini oluşturan sınıf.
    Artık veritabanındaki HastaneAyarlari modelinden gelen dinamik kurallara göre çalışır.
    """
    def __init__(self, yil, ay):
        self.yil = yil
        self.ay = ay
        self.ay_gun_sayisi = calendar.monthrange(yil, ay)[1]
        self.plan_tarihleri = [date(yil, ay, gun) for gun in range(1, self.ay_gun_sayisi + 1)]

        # --- DİNAMİK AYARLARI VERİTABANINDAN ÇEK ---
        self.ayarlar = HastaneAyarlari.get_solo()

        # Veritabanından diğer verileri çek
        self.doktorlar = list(Doktor.objects.all())
        self.izinler = self._get_izinler()

        # Algoritma durumunu takip etmek için
        self.nobet_gecmisi = defaultdict(list)
        self.nobet_sayilari = defaultdict(int)

    def _get_izinler(self):
        """O ayki tüm izin taleplerini veritabanından çeker."""
        izinler = defaultdict(list)
        qs = IzinTalebi.objects.filter(tarih__year=self.yil, tarih__month=self.ay)
        for izin in qs:
            izinler[izin.tarih].append(izin.doktor_id)
        return izinler

    def _get_gunun_uygun_doktorlari(self, gunun_tarihi):
        """Belirli bir gün için izinli olmayan ve dinlenme süresini doldurmuş doktorları döndürür."""
        uygun_doktorlar = []
        izinli_doktor_idler = self.izinler.get(gunun_tarihi, [])
        
        for dr in self.doktorlar:
            if dr.id in izinli_doktor_idler:
                continue
            
            son_nobet_tarihi = self.nobet_gecmisi.get(dr.id, [])[-1] if self.nobet_gecmisi.get(dr.id) else None
            if son_nobet_tarihi:
                gun_farki = (gunun_tarihi - son_nobet_tarihi).days
                # SABİT SAYI YERİNE DİNAMİK AYARI KULLAN
                if gun_farki <= self.ayarlar.minimum_dinlenme_gunu:
                    continue
            
            uygun_doktorlar.append(dr)
        
        return uygun_doktorlar

    def _takim_gecerli_mi(self, takim):
        """Bir doktor ekibinin kurallara uyup uymadığını kontrol eder."""
        kidemler = [dr.kidem for dr in takim]
        # SABİT DEĞİŞKEN YERİNE DOĞRUDAN MODEL SEÇENEKLERİNİ KULLAN
        if Doktor.Kidem.ACEMI in kidemler and Doktor.Kidem.KIDEMLI not in kidemler:
            return False # Acemi varsa, yanında mutlaka Kıdemli olmalı
        return True

    def _takim_skorla(self, takim):
        """Bir takıma adalet ve verimlilik puanı verir. Düşük skor daha iyidir."""
        skor = 0
        for dr in takim:
            skor += self.nobet_sayilari.get(dr.id, 0) * 10 
            son_nobet = self.nobet_gecmisi.get(dr.id, [])[-1] if self.nobet_gecmisi.get(dr.id) else None
            if son_nobet:
                gun_farki = (date(self.yil, self.ay, 1) - son_nobet).days
                skor -= gun_farki
        return skor

    def plani_olustur(self):
        """
        Ana planlama fonksiyonu. Yetersizlik durumunda izinli doktorları zorunlu olarak atar.
        """
        olusturulan_plan = []
        # Bu liste, hangi günlerde kimlerin izninin iptal edildiğini takip edecek
        self.zorunlu_atama_kaydi = defaultdict(list) 

        for gunun_tarihi in self.plan_tarihleri:
            # 1. Aşama: İdeal adayları bul (İzinli olmayan ve dinlenmiş olanlar)
            uygun_doktorlar = self._get_gunun_uygun_doktorlari(gunun_tarihi)
            
            eksik_doktor_sayisi = self.ayarlar.gunluk_doktor_sayisi - len(uygun_doktorlar)

            # 2. Aşama: Yetersizlik var mı? Varsa Acil Durum Prosedürünü başlat.
            if eksik_doktor_sayisi > 0:
                print(f"UYARI: {gunun_tarihi} için {eksik_doktor_sayisi} doktor eksik. İzinli doktorlardan zorunlu atama yapılacak.")
                
                # İzinli olan ama dinlenme süresi uygun olan doktorları bul
                izinli_ama_uygun_doktorlar = []
                izinli_doktor_idler = self.izinler.get(gunun_tarihi, [])
                for dr in self.doktorlar:
                    if dr.id in izinli_doktor_idler:
                        son_nobet_tarihi = self.nobet_gecmisi.get(dr.id, [])[-1] if self.nobet_gecmisi.get(dr.id) else None
                        if son_nobet_tarihi:
                            gun_farki = (gunun_tarihi - son_nobet_tarihi).days
                            if gun_farki <= self.ayarlar.minimum_dinlenme_gunu:
                                continue # İzinli olsa bile dinlenemeyecekse atama
                        izinli_ama_uygun_doktorlar.append(dr)
                
                # Eksik sayı kadar izinli doktoru rastgele seç
                if len(izinli_ama_uygun_doktorlar) >= eksik_doktor_sayisi:
                    zorunlu_atananlar = random.sample(izinli_ama_uygun_doktorlar, eksik_doktor_sayisi)
                    uygun_doktorlar.extend(zorunlu_atananlar) # Ana havuza ekle
                    # Kimlerin izninin iptal edildiğini kaydet
                    self.zorunlu_atama_kaydi[gunun_tarihi] = [dr.id for dr in zorunlu_atananlar]
                else:
                    print(f"KRİTİK HATA: {gunun_tarihi} için izinliler dahil yeterli doktor yok!")
                    continue # Bu durumda bile doktor yoksa günü boş bırak

            # 3. Aşama: Tamamlanan havuzdan en iyi takımı oluştur
            gecerli_takimlar = []
            for _ in range(500):
                aday_takim = random.sample(uygun_doktorlar, self.ayarlar.gunluk_doktor_sayisi)
                if self._takim_gecerli_mi(aday_takim):
                    skor = self._takim_skorla(aday_takim)
                    gecerli_takimlar.append((skor, aday_takim))
            
            if not gecerli_takimlar:
                print(f"UYARI: {gunun_tarihi} için geçerli bir takım oluşturulamadı!")
                continue

            gecerli_takimlar.sort(key=lambda x: x[0])
            en_iyi_takim = gecerli_takimlar[0][1]

            olusturulan_plan.append((gunun_tarihi, en_iyi_takim))
            for dr in en_iyi_takim:
                self.nobet_sayilari[dr.id] += 1
                self.nobet_gecmisi[dr.id].append(gunun_tarihi)

        return olusturulan_plan

    def _bolumlere_ata(self, takim):
        """Verilen bir takımı kıdem sırasına göre bölümlere atar. (Dinamik sayıya uygun hale getirildi)"""
        kidem_siralamasi = {Doktor.Kidem.KIDEMLI: 3, Doktor.Kidem.ORTA_KIDEMLI: 2, Doktor.Kidem.ACEMI: 1}
        takim.sort(key=lambda dr: kidem_siralamasi[dr.kidem], reverse=True)
        
        atama = {
            Nobet.Bolum.KIRMIZI: None,
            Nobet.Bolum.SARI: None,
            Nobet.Bolum.YESIL: [],
        }

        if len(takim) > 0:
            atama[Nobet.Bolum.KIRMIZI] = takim[0]
        if len(takim) > 1:
            atama[Nobet.Bolum.SARI] = takim[1]
        if len(takim) > 2:
            atama[Nobet.Bolum.YESIL] = takim[2:]
        
        return atama

    def plani_kaydet(self, plan):
        """Oluşturulan planı veritabanına kaydeder. Zorunlu atamaları işaretler."""
        Nobet.objects.filter(tarih__year=self.yil, tarih__month=self.ay).delete()
        print(f"{self.yil}-{self.ay} dönemine ait eski nöbetler silindi.")

        nobet_listesi = []
        for tarih, takim in plan:
            atama = self._bolumlere_ata(takim)
            
            # Tüm atama işlemlerini tek bir döngüde yapalım
            for bolum, doktorlar in atama.items():
                # Doktorlar tek bir obje veya liste olabilir, bunu yönetelim
                if not isinstance(doktorlar, list):
                    doktorlar = [doktorlar]
                
                for dr in doktorlar:
                    if not dr: continue # Doktor None ise atla

                    # Bu doktorun izni bu gün için iptal edildi mi?
                    is_zorunlu = dr.id in self.zorunlu_atama_kaydi.get(tarih, [])

                    nobet_listesi.append(
                        Nobet(doktor=dr, tarih=tarih, bolum=bolum, izin_iptal_edildi=is_zorunlu)
                    )

        Nobet.objects.bulk_create(nobet_listesi)
        print(f"{len(nobet_listesi)} adet yeni nöbet başarıyla veritabanına kaydedildi.")