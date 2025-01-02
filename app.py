import requests
import os
import json
import urllib.parse
from requests.adapters import HTTPAdapter, Retry
import re

# Retry mekanizması ayarları
retry_strategy = Retry(
    total=3,  # Toplam 3 deneme
    backoff_factor=1,  # Her denemeden sonra bekleme süresi (2. deneme için 1 saniye, 3. deneme için 2 saniye vb.)
    status_forcelist=[429, 500, 502, 503, 504],  # Yeniden deneme yapılacak durum kodları
    allowed_methods=["HEAD", "GET", "OPTIONS"]  # Yeniden deneme yapılacak HTTP yöntemleri
)

adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("http://", adapter)
http.mount("https://", adapter)

# Dosya ismini geçerli hale getirmek için fonksiyon
def clean_filename(filename):
    # Geçersiz karakterleri temizle
    return re.sub(r'[<>:"/\|?*]', '_', filename)

# Kullanıcıdan hastalık ismi ve dosya yolu al
disease = "Zoonoses transmissible from non-human primates"
json_file = "C:\\Users\\ardac\\OneDrive\\Masaüstü\\pdfdowland\\all_pdf_links.json"  # JSON dosyasının yolunu belirtiyoruz

# JSON dosyasını oku
with open(json_file, 'r') as f:
    data = json.load(f)  # JSON verisini okuyoruz

# PDF dosyalarını kaydetmek için dizin
save_dir = "C:\\Users\\ardac\\OneDrive\\Masaüstü\\pdfdowland"
os.makedirs(save_dir, exist_ok=True)

# Hastalık ismiyle bir klasör oluştur
folder_name = disease.replace(" ", "").replace("(", "").replace(")", "").replace("/", "")
disease_dir = os.path.join(save_dir, folder_name)
os.makedirs(disease_dir, exist_ok=True)

# JSON verisinde girilen hastalığın linkleri varsa işlemi yap
if disease in data:
    links = data[disease]

    # PDF dosyalarını indir ve kaydet
    for url in links:
        try:
            response = http.get(url, timeout=10)  # Zaman aşımı süresi 10 saniye
            response.raise_for_status()  # İstek başarılı değilse HTTPError hatası fırlatır
            
            # Dosya ismini URL'den alıp geçerli bir dosya adı yap
            file_name = os.path.basename(url)
            file_name = urllib.parse.unquote(file_name)  # URL kodlamasını çözüyoruz
            file_name = clean_filename(file_name)  # Geçersiz karakterleri temizle

            # Dosyayı kaydet
            file_path = os.path.join(disease_dir, file_name)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"İndirilen dosya: {file_path}")
        except requests.exceptions.RequestException as e:
            print(f"İndirme başarısız: {url}\nHata: {e}")
            continue  # Hata durumunda sıradaki URL'ye geç
else:
    print(f"{disease} için link bulunamadı.")

print("İndirme işlemi tamamlandı.")