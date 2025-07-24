# --- START OF FILE apple_scraper.py ---

import os
import json
import requests
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

OUTPUT_DIR = os.path.join("..", "app_store_data")
CONFIG_FILE = "apps_config.json"

def load_apps_to_scrape(config_path):
    if not os.path.exists(config_path):
        logging.error(f"Konfigürasyon dosyası bulunamadı: {config_path}")
        logging.error("Lütfen 'apps_config.json' adında bir dosya oluşturun.")
        return []
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def scrape_all_reviews_for_app(app_id, app_name):
    all_reviews = []
    page = 1
    
    while page <= 10:
        target_url = f"https://itunes.apple.com/tr/rss/customerreviews/page={page}/id={app_id}/sortby=mostrecent/json"
        logging.info(f"'{app_name}' için sayfa {page} çekiliyor...")

        try:
            response = requests.get(target_url, timeout=20)
            if response.status_code != 200:
                break
            
            data = response.json()
            entries = data.get('feed', {}).get('entry')

            if not entries or len(entries) <= 1:
                break

            for entry in entries[1:]:
                comment = entry.get('content', {}).get('label', '')
                if not comment: continue

                all_reviews.append({
                    "comment": comment,
                    "rating": int(entry.get('im:rating', {}).get('label', '0')),
                    "source": "Apple App Store"
                })
            
            page += 1
            time.sleep(0.5) 
        except Exception as e:
            logging.error(f"'{app_name}' için sayfa {page}'de hata: {e}")
            break

    logging.info(f"'{app_name}' için toplam {len(all_reviews)} yorum çekildi.")
    return all_reviews

if __name__ == '__main__':
    logging.info("App Store Yorum Çekme Script'i Başlatıldı.")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        logging.info(f"'{OUTPUT_DIR}' klasörü oluşturuldu.")

    apps_list = load_apps_to_scrape(CONFIG_FILE)

    for app_info in apps_list:
        app_name = app_info.get("app_name")
        app_id = app_info.get("app_id")

        if not app_name or not app_id:
            continue
        
        logging.info(f"--- '{app_name}' için yorumlar işleniyor... ---")
        reviews_data = scrape_all_reviews_for_app(app_id, app_name)
        
        if reviews_data:
            file_path = os.path.join(OUTPUT_DIR, f"{app_name.lower()}_reviews.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(reviews_data, f, ensure_ascii=False, indent=4)
            logging.info(f"BAŞARILI: '{app_name}' için {len(reviews_data)} yorum kaydedildi.")

    logging.info("Tüm işlemler tamamlandı!")

# --- END OF FILE apple_scraper.py ---