# --- START OF FILE scraper_service.py ---

import os
from google_play_scraper import reviews, Sort
from flask import Flask, jsonify
import logging

# --- TEMEL AYARLAR ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
app = Flask(__name__)

# Ayarlar, ortam değişkenlerinden (environment variables) okunur.
# Eğer değişken tanımlı değilse, varsayılan bir değer kullanılır.
REVIEW_COUNT = int(os.getenv("REVIEW_COUNT", 100))


def scrape_google_play(app_id):
    """Belirtilen 'app_id' için Google Play yorumlarını çeker."""
    logging.info(f"'{app_id}' için Google Play Store'dan {REVIEW_COUNT} yorum çekme işlemi başladı.")
    reviews_list = []
    try:
        result, _ = reviews(
            app_id,
            lang='tr',
            country='tr',
            sort=Sort.NEWEST,
            count=REVIEW_COUNT
        )
        for review in result:
            reviews_list.append({
                "comment": review['content'],
                "rating": review['score'],
                "source": "Google Play",
                "app_id": app_id
            })
        logging.info(f"'{app_id}' için {len(reviews_list)} yorum bulundu.")
    except Exception as e:
        logging.error(f"'{app_id}' scrape edilirken hata oluştu: {e}")
    
    return reviews_list

@app.route('/scrape/<app_id>', methods=['GET'])
def scrape_app(app_id):
    """URL'den gelen app_id'ye göre tek bir uygulamanın yorumlarını toplayıp JSON döndürür."""
    logging.info(f"API isteği alındı: /scrape/{app_id}")
    
    if not app_id:
        return jsonify({"error": "Uygulama ID'si (app_id) belirtilmedi."}), 400
        
    all_reviews = scrape_google_play(app_id)
    logging.info(f"'{app_id}' için toplam {len(all_reviews)} yorum toplandı.")
    
    return jsonify(all_reviews)

if __name__ == '__main__':
    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(host=host, port=port)

# --- END OF FILE scraper_service.py ---