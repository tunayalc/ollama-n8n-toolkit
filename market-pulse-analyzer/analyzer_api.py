# --- START OF FILE analyzer_api.py ---

import os
import json
import pandas as pd
import requests
import logging
from flask import Flask, jsonify
import threading
import datetime

# --- TEMEL AYARLAR ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
app = Flask(__name__)

# --- YAPILANDIRMA (Ortam Değişkenlerinden Oku) ---
# Birden fazla girdi klasörü virgülle ayrılarak belirtilebilir.
INPUT_FOLDERS_STR = os.getenv("INPUT_FOLDERS", "app_store_data,google_data")
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "output")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://ollama_core:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
OUTPUT_FILENAME_BASE = os.getenv("OUTPUT_FILENAME_BASE", "analysis_report")

# --- ANALİZ FONKSİYONLARI ---

def read_reviews_from_all_folders():
    """Belirtilen tüm girdi klasörlerindeki yorumları okur ve birleştirir."""
    all_reviews = []
    folder_list = [folder.strip() for folder in INPUT_FOLDERS_STR.split(',')]
    
    for folder_path in folder_list:
        if not os.path.exists(folder_path):
            logging.warning(f"Girdi klasörü bulunamadı, atlanıyor: '{folder_path}'")
            continue
            
        logging.info(f"'{folder_path}' klasöründeki yorumlar okunuyor...")
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        for review in data:
                            comment = review.get('comment', '') or review.get('content', '')
                            if comment:
                                all_reviews.append({
                                    "comment": comment,
                                    "rating": review.get('rating', 0) or review.get('score', 0),
                                    "source": review.get('source', 'Bilinmiyor'),
                                    "app_id": review.get('app_id', 'Bilinmiyor')
                                })
                except Exception as e:
                    logging.error(f"'{filename}' okunurken hata: {e}")
                    
    return all_reviews

def analyze_comment_with_ollama(comment):
    """Verilen bir yorum metnini Ollama API'si ile analiz eder."""
    if not isinstance(comment, str) or len(comment.strip()) < 10:
        return {"konu": "Geçersiz", "duygu": "Nötr", "ozet": "Analiz için yorum çok kısa."}
        
    prompt = f"Bir ürün analisti gibi davran. Şu yorumu analiz et: '{comment}'. Yorumun konusunu ('Tasarım', 'Performans', 'Hata', 'Ödeme', 'Uygulama Özelliği', vb.), duygu durumunu ('Pozitif', 'Negatif', 'Nötr') ve 10 kelimelik özetini çıkar. Cevabını SADECE şu JSON formatında ver: {{\"konu\": \"...\", \"duygu\": \"...\", \"ozet\": \"...\"}}"
    payload = {"model": OLLAMA_MODEL, "prompt": prompt, "format": "json", "stream": False}
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        response.raise_for_status()
        analysis_result = json.loads(response.json().get('response', '{}'))
        return analysis_result
    except requests.exceptions.RequestException as e:
        logging.error(f"Ollama API'sine ulaşılamadı: {e}")
        return {"konu": "Hata", "duygu": "Hata", "ozet": "API bağlantı hatası."}
    except Exception as e:
        logging.error(f"Ollama analizi sırasında beklenmedik hata: {e}")
        return {"konu": "Hata", "duygu": "Hata", "ozet": "Analiz sırasında genel hata."}

def run_the_full_analysis():
    """Tüm analiz sürecini yürüten ve sonucu Excel dosyasına yazan ana fonksiyon."""
    logging.info("--- TAM ANALİZ SÜRECİ BAŞLATILDI ---")
    
    all_comments = read_reviews_from_all_folders()
    if not all_comments:
        logging.warning("Analiz edilecek yorum bulunamadı. Süreç sonlandırılıyor.")
        return
    
    logging.info(f"Toplam {len(all_comments)} yorum analiz için sıraya alındı.")
    analyzed_data = []
    for i, review in enumerate(all_comments):
        logging.info(f"Yorum {i+1}/{len(all_comments)} analiz ediliyor...")
        analysis = analyze_comment_with_ollama(review['comment'])
        full_data = {**review, **analysis}
        analyzed_data.append(full_data)

    df = pd.DataFrame(analyzed_data)
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
        
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    output_file = os.path.join(OUTPUT_PATH, f"{OUTPUT_FILENAME_BASE}_{timestamp}.xlsx")
    
    df.to_excel(output_file, index=False)
    logging.info(f"--- ANALİZ TAMAMLANDI! Rapor '{output_file}' dosyasına kaydedildi. ---")

# --- API ENDPOINT'İ (n8n'in çağıracağı adres) ---

@app.route('/start_analysis', methods=['POST'])
def start_analysis_endpoint():
    """n8n'den gelen isteği alır ve analizi arka planda başlatır."""
    logging.info("API üzerinden analiz başlatma isteği alındı!")
    
    thread = threading.Thread(target=run_the_full_analysis)
    thread.start()
    
    return jsonify({"status": "success", "message": "Analiz görevi arka planda başlatıldı."}), 202

if __name__ == '__main__':
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", 5002))
    app.run(host=host, port=port)

# --- END OF FILE analyzer_api.py ---