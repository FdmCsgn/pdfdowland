# PDF İndirme Aracı

Bu Python betiği, belirtilen hastalık kategorisine ait PDF dosyalarını bir JSON dosyasından okuyarak otomatik olarak indiren ve düzenli bir şekilde kaydeden bir araçtır.

## 🔍 Özellikler

- JSON dosyasından PDF linklerini okuma
- Otomatik yeniden deneme mekanizması
- Hata yönetimi ve raporlama
- Dosya adı temizleme ve düzenleme
- Kategoriye göre klasörleme

## 🛠️ Teknik Detaylar

### Bağımlılıklar

```python
import requests
import os
import json
import urllib.parse
from requests.adapters import HTTPAdapter, Retry
import re
```

### Yeniden Deneme Mekanizması

Betik, ağ hatalarına karşı dayanıklı bir yapıya sahiptir:
- Toplam 3 deneme hakkı
- Artan bekleme süresi (backoff)
- HTTP 429, 500, 502, 503, 504 hata kodları için otomatik yeniden deneme
- HEAD, GET ve OPTIONS metodları için yeniden deneme desteği

### Dosya İsimlendirme

`clean_filename()` fonksiyonu ile dosya adlarındaki geçersiz karakterler temizlenir:
- Windows'da geçersiz olan `<>:"/\|?*` karakterleri '_' ile değiştirilir
- URL kodlaması çözülür

### Klasör Yapısı

- Ana dizin: Kullanıcı tarafından belirlenir
- Alt dizinler: Hastalık isimlerine göre otomatik oluşturulur
- PDF dosyaları: İlgili hastalık klasörüne kaydedilir

## 📝 Kullanım

1. JSON dosyasında aşağıdaki formatta PDF linkleri bulunmalıdır:
```json
{
    "Hastalık Adı": [
        "http://örnek.com/dosya1.pdf",
        "http://örnek.com/dosya2.pdf"
    ]
}
```

2. Betiği çalıştırmadan önce aşağıdaki değişkenleri ayarlayın:
```python
disease = "Hastalık Adı"
json_file = "JSON_dosyasının_yolu"
save_dir = "PDF_kayıt_dizini"
```

## ⚠️ Hata Yönetimi

- Ağ bağlantı hataları için yeniden deneme
- Zaman aşımı kontrolü (10 saniye)
- Başarısız indirmeler için hata raporlama
- Geçersiz hastalık isimleri için kontrol

## 🔄 İşlem Akışı

1. JSON dosyası okunur
2. Hastalık ismi kontrol edilir
3. Hedef klasörler oluşturulur
4. PDF dosyaları sırayla indirilir
5. İndirilen dosyalar ilgili klasöre kaydedilir
6. İşlem durumu raporlanır

## 📋 Çıktı

Betik çalışırken:
- Başarılı indirmeler için dosya yolu
- Başarısız indirmeler için hata mesajı
- İşlem tamamlandığında bilgi mesajı

## 🤝 Katkıda Bulunma

1. Bu projeyi fork edin
2. Feature branch'i oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Pull Request oluşturun
