# --- START OF FILE run_scraper.py ---

import os
import json
import requests
import logging

# --- TEMEL AYARLAR ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Konfigürasyonlar ortam değişkenlerinden ve dosyadan okunur.
SERVICE_URL = os.getenv("SCRAPER_API_URL", "http://127.0.0.1:5000/scrape")
CONFIG_FILE = "google_play_apps.json"
OUTPUT_DIR = "google_play_reviews"


def load_config(config_path):
    """Uygulama listesini içeren JSON konfigürasyon dosyasını yükler."""
    if not os.path.exists(config_path):
        logging.error(f"Konfigürasyon dosyası bulunamadı: '{config_path}'")
        return None
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def fetch_reviews_for_app(app_name, app_id):
    """Belirtilen uygulama için scraper servisinden yorumları çeker."""
    logging.info(f"'{app_name}' ({app_id}) için yorumlar çekiliyor...")
    target_url = f"{SERVICE_URL}/{app_id}"
    try:
        response = requests.get(target_url, timeout=90)
        if response.status_code == 200:
            logging.info(f"'{app_name}' için veriler başarıyla alındı.")
            return response.json()
        else:
            logging.error(f"'{app_name}' için hata: Sunucu {response.status_code} kodu döndü. Yanıt: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"'{app_name}' için API'ye bağlanırken hata: {e}")
        return None

def save_reviews_to_file(app_name, reviews_data):
    """Çekilen yorum verilerini bir JSON dosyasına kaydeder."""
    if not reviews_data:
        logging.warning(f"'{app_name}' için kaydedilecek veri bulunamadı.")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    file_path = os.path.join(OUTPUT_DIR, f"{app_name.lower()}_reviews.json")
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(reviews_data, f, ensure_ascii=False, indent=4)
        logging.info(f"'{app_name}' için {len(reviews_data)} yorum '{file_path}' dosyasına kaydedildi.")
    except Exception as e:
        logging.error(f"Dosya yazma hatası ('{file_path}'): {e}")


if __name__ == "__main__":
    logging.info("Google Play scraping işlemi başlıyor...")
    
    apps_to_scrape = load_config(CONFIG_FILE)
    
    if not apps_to_scrape:
        logging.error("Taranacak uygulama listesi yüklenemedi. Script sonlandırılıyor.")
    else:
        for name, app_id in apps_to_scrape.items():
            reviews = fetch_reviews_for_app(name, app_id)
            save_reviews_to_file(name, reviews)
        
    logging.info("Tüm işlemler tamamlandı.")

# --- END OF FILE run_scraper.py ---