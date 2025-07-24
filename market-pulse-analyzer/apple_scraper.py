# --- START OF FILE apple_scraper.py ---

import os
import json
import requests
import logging
import time

# --- TEMEL AYARLAR ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Çıktıların kaydedileceği klasör
OUTPUT_DIR = "output_data"
# Taranacak uygulamaların listesini içeren konfigürasyon dosyası
CONFIG_FILE = "apps_to_scrape.json"


def load_config(config_path):
    """Konfigürasyon dosyasını yükler ve uygulama listesini döndürür."""
    if not os.path.exists(config_path):
        logging.error(f"Konfigürasyon dosyası bulunamadı: '{config_path}'")
        logging.error("Lütfen taranacak uygulamaları içeren 'apps_to_scrape.json' dosyasını oluşturun.")
        return []
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        logging.error(f"'{config_path}' dosyası geçerli bir JSON formatında değil.")
        return []

def scrape_reviews_for_app(app_id, app_name):
    """Belirtilen bir uygulama için App Store yorumlarını çeker."""
    logging.info(f"--- '{app_name}' (ID: {app_id}) için yorumlar çekiliyor... ---")
    all_reviews = []
    
    # Apple genellikle en fazla 10 sayfa (500 yorum) sunar.
    for page in range(1, 11):
        target_url = f"https://itunes.apple.com/tr/rss/customerreviews/page={page}/id={app_id}/sortby=mostrecent/json"
        
        try:
            response = requests.get(target_url, timeout=20)
            if response.status_code != 200:
                logging.warning(f"'{app_name}' için sayfa {page} bulunamadı (HTTP {response.status_code}). Bu uygulama için durduruluyor.")
                break
            
            data = response.json()
            entries = data.get('feed', {}).get('entry')

            if not entries or len(entries) <= 1:
                logging.info(f"'{app_name}' için son sayfaya ulaşıldı (Sayfa {page}).")
                break

            # İlk entry genelde uygulama bilgisidir, onu atla
            for entry in entries[1:]:
                all_reviews.append({
                    "author": entry.get('author', {}).get('name', {}).get('label', 'Bilinmiyor'),
                    "rating": int(entry.get('im:rating', {}).get('label', '0')),
                    "title": entry.get('title', {}).get('label', ''),
                    "comment": entry.get('content', {}).get('label', '')
                })
            
            time.sleep(0.5) # Sunucuyu yormamak için nazik bir bekleme
        except requests.exceptions.RequestException as e:
            logging.error(f"'{app_name}' işlenirken ağ hatası (sayfa {page}): {e}")
            break
        except Exception as e:
            logging.error(f"'{app_name}' işlenirken beklenmedik hata (sayfa {page}): {e}")
            break
            
    return all_reviews


# --- ANA ÇALIŞMA AKIŞI ---
if __name__ == "__main__":
    logging.info("App Store Yorum Çekme Script'i Başlatıldı.")
    
    apps_to_scrape = load_config(CONFIG_FILE)
    
    if not apps_to_scrape:
        logging.warning("Taranacak uygulama bulunamadı. Script sonlandırılıyor.")
    else:
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
            logging.info(f"'{OUTPUT_DIR}' klasörü oluşturuldu.")

        for app_info in apps_to_scrape:
            app_name = app_info.get("app_name")
            app_id = app_info.get("app_id")

            if not app_name or not app_id:
                logging.warning(f"Geçersiz giriş atlanıyor: {app_info}")
                continue

            reviews_data = scrape_reviews_for_app(app_id, app_name)
            
            if reviews_data:
                file_path = os.path.join(OUTPUT_DIR, f"{app_name.lower()}_reviews.json")
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(reviews_data, f, ensure_ascii=False, indent=4)
                logging.info(f"BAŞARILI: '{app_name}' için {len(reviews_data)} yorum '{file_path}' dosyasına kaydedildi.")
            else:
                logging.warning(f"UYARI: '{app_name}' için hiç yorum bulunamadı veya çekilemedi.")
            
            time.sleep(1) # Bir sonraki uygulamaya geçmeden önce 1 saniye bekle

    logging.info("Tüm işlemler tamamlandı!")

# --- END OF FILE apple_scraper.py ---