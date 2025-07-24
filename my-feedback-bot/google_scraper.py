# C:\Users\ytuna\my-feedback-bot\scraper_service\app.py - SADELEŞTİRİLMİŞ VERSİYON

import json
import requests
from bs4 import BeautifulSoup             # İsterseniz artık kullanılmadığı için silebilirsiniz
from google_play_scraper import reviews, Sort
from flask import Flask, jsonify
import logging

# Loglama ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# --- START OF FILE google_scraper.py ---

import os
import json
import requests
from google_play_scraper import reviews, Sort
from flask import Flask, jsonify
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Ayarlar ortam değişkenlerinden (environment variables) okunur.
# Eğer değişken tanımlı değilse, varsayılan bir değer kullanılır.
GOOGLE_PLAY_ID = os.getenv("GOOGLE_PLAY_APP_ID", "com.google.android.gm") # Varsayılan: Gmail
REVIEW_COUNT = int(os.getenv("REVIEW_COUNT", 50))

def scrape_google_play():
    logging.info(f"Google Play Store'dan '{GOOGLE_PLAY_ID}' için scraping işlemi başladı.")
    reviews_list = []
    try:
        result, _ = reviews(
            GOOGLE_PLAY_ID,
            lang='tr',
            country='tr',
            sort=Sort.NEWEST,
            count=REVIEW_COUNT
        )
        for review in result:
            reviews_list.append({
                "comment": review['content'],
                "rating": review['score'],
                "source": "Google Play"
            })
        logging.info(f"Google Play'den {len(reviews_list)} yorum bulundu.")
    except Exception as e:
        logging.error(f"Google Play scrape edilirken hata: {e}")
    return reviews_list

@app.route('/scrape', methods=['GET'])
def scrape_all():
    logging.info("Scrape isteği alındı.")
    all_reviews = scrape_google_play()
    logging.info(f"Toplam {len(all_reviews)} yorum toplandı.")
    return jsonify(all_reviews)

if __name__ == '__main__':
    # Flask portu da ortam değişkeninden okunabilir.
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# --- END OF FILE google_scraper.py ---
app = Flask(__name__)

# --- HEDEFLER ---
GOOGLE_PLAY_ID = "com.aktifbank.nkolay"
REVIEW_COUNT = 50  # Her kaynaktan alınacak yorum sayısı

def scrape_google_play():
    """
    Google Play yorumlarını 'google-play-scraper' kütüphanesi ile çeker.
    """
    logging.info("Google Play Store scraping işlemi başladı.")
    reviews_list = []
    try:
        result, _ = reviews(
            GOOGLE_PLAY_ID,
            lang='tr',
            country='tr',
            sort=Sort.NEWEST,
            count=REVIEW_COUNT
        )
        for review in result:
            reviews_list.append({
                "comment": review['content'],
                "rating": review['score'],
                "source": "Google Play"
            })
        logging.info(f"Google Play'den {len(reviews_list)} yorum bulundu.")
    except Exception as e:
        logging.error(f"Google Play scrape edilirken hata: {e}")
    return reviews_list

@app.route('/scrape', methods=['GET'])
def scrape_all():
    """
    Tek kaynaktan (Google Play) yorumları toplayıp JSON döndürür.
    """
    logging.info("Google Play için scrape isteği alındı.")
    all_reviews = scrape_google_play()
    logging.info(f"Toplam {len(all_reviews)} yorum toplandı.")
    return jsonify(all_reviews)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
