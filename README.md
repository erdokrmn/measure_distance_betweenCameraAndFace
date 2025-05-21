
KAMERA MESAFE TESPİTİ ve UYARI SİSTEMİ
=====================================

Bu proje, bir web kamerası kullanarak kullanıcının yüzünü tespit eder ve tahmini kamera-yüz mesafesini (cm cinsinden) hesaplar.
Eğer kullanıcı çok yakında ya da çok uzakta duruyorsa, ekranda gerçek zamanlı olarak uyarı gösterir.

------------------------------------------------------------
🔧 ÖZELLİKLER
------------------------------------------------------------
- MediaPipe ile hızlı ve güvenilir yüz tespiti
- Yüz genişliğine göre mesafe tahmini (Z ekseni hesaplama)
- Kalibrasyon sistemi ile kişiye özel doğruluk
- Gerçek zamanlı mesafe ölçümü ve renkli uyarı mesajları
- `calibration.json` dosyasından otomatik A ve B katsayısı okuma
- Şeffaf arayüzde kullanıcı dostu uyarı yazıları

------------------------------------------------------------
📁 DOSYA YAPISI
------------------------------------------------------------
- main.py             → Ana uygulama (gerçek zamanlı sistem)
- calibration.py      → Kalibrasyon sihirbazı (manuel ölçüm gerektirmez)
- calibration.json    → Kalibrasyon çıktısı (otomatik A/B katsayıları)
- requirements.txt    → Gerekli kütüphaneler listesi

------------------------------------------------------------
📦 GEREKLİ KÜTÜPHANELER
------------------------------------------------------------
- opencv-python
- mediapipe
- scikit-learn
- numpy

Kurmak için:
    pip install -r requirements.txt

------------------------------------------------------------
⚙️ KULLANIM
------------------------------------------------------------

1. Kalibrasyon çalıştır:
    python calibration.py
    → Ekrandaki yönergelere göre 30cm, 50cm, 70cm mesafelerinde SPACE tuşuna bas

2. Ana uygulamayı başlat:
    python main.py
    → Yüz algılanır, mesafe hesaplanır, ekrana uyarı yazılır

------------------------------------------------------------
📌 MESAFE UYARI SINIRLARI
------------------------------------------------------------
- < 30 cm       → "Çok yakınsınız, biraz uzaklaşın."
- > 80 cm       → "Alan dışındasınız, lütfen yaklaşın."
- 30–80 cm      → "Mesafe uygun" (takip aktif)

------------------------------------------------------------
📝 NOTLAR
------------------------------------------------------------
- Kalibrasyon sırasında her kullanıcıya özel A ve B katsayıları üretilir
- Bu değerler calibration.json dosyasına otomatik yazılır
- main.py bu dosyayı okuyarak gerçek zamanlı çalışır
