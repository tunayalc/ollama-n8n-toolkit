# Rakip Uygulama Analizi ve Strateji Otomasyonu

Bu proje, kendi uygulamanız ve rakiplerinizin uygulama mağazalarındaki (Google Play, Apple App Store) kullanıcı yorumlarını otomatik olarak toplayan, bu verileri yapay zeka ile derinlemesine analiz eden ve sonuçları stratejik bir pazar araştırma raporuna dönüştüren bütünleşik bir otomasyon sistemidir.

Projenin temel amacı, ürün yönetimi ve pazarlama ekiplerine veri odaklı kararlar alabilmeleri için rakiplere karşı güçlü ve zayıf yönleri gösteren, aksiyon alınabilir içgörüler sunmaktır. Tüm sistem, **Docker** kullanılarak konteynerler içinde çalışacak şekilde tasarlanmıştır.

## Bileşenler

### 1. Veri Toplama (Scrapers)
Bu modül, farklı uygulama mağazalarından yorumları toplar.

- **Google Play Scraper Servisi (`scraper_service.py`):** Belirtilen bir uygulama kimliği (`app_id`) için yorumları çeken bir Flask API servisidir.
- **Google Scraper Tetikleyici (`run_scraper.py`):** Bir konfigürasyon dosyasından (`google_play_apps.json`) uygulama listesini okur, her biri için Scraper Servisi'ni çağırır ve sonuçları ayrı JSON dosyaları olarak kaydeder.
- **Apple App Store Scraper (`apple_scraper.py`):** Bir konfigürasyon dosyasından (`apps_to_scrape.json`) aldığı listeye göre doğrudan Apple'dan yorumları çeken ve JSON dosyalarına kaydeden bağımsız bir script'tir.

### 2. Yorum Analiz Servisi (`analyzer_api.py`)
Toplanan ham veriyi anlamlı hale getiren yapay zeka destekli bir Flask API'sidir.

- **Veri Birleştirme:** Tüm scraper'ların ürettiği JSON dosyalarını okuyup tek bir veri havuzunda birleştirir.
- **Derinlemesine Analiz:** Her bir yorum metnini, lokalde çalışan **Ollama (LLM)** servisine göndererek yorumun **konusunu** (örn: "Performans", "Tasarım", "Hata"), **duygusunu** ("Pozitif", "Negatif") ve **kısa bir özetini** çıkarır.
- **Raporlama:** Analiz edilmiş tüm verileri, üzerinde daha fazla çalışılabilmesi için detaylı bir **Excel dosyası** olarak kaydeder.

### 3. Strateji ve Raporlama (n8n İş Akışı)
Tüm sürecin son ve en kritik adımıdır. `Rakip analiz ve kıyas botu.json` dosyasında tanımlanan bu akış, analitik veriyi stratejik bir rapora dönüştürür.

- **Veri Sentezi:** Analiz Servisi'nin ürettiği Excel raporunu okur.
- **İstatistiksel Kıyaslama:** Bir "Code" nodu aracılığıyla kendi uygulamanız ve rakipleriniz için "Pozitif Duygu Oranı", "En Çok Şikayet Edilen Konu" gibi metrikleri hesaplar ve kıyaslar.
- **Stratejik Rapor Üretimi:** Bu istatistiksel özeti, özel bir prompt ile tekrar **Ollama (LLM)** servisine gönderir. Yapay zekadan, bir pazar stratejisti gibi davranarak kapsamlı bir kıyaslama analizi ve somut çözüm önerileri içeren bir Markdown raporu oluşturması istenir.

## Sistem Nasıl Çalışır? (Uçtan Uca Akış)

1.  **Veri Toplama:** `run_scraper.py` ve `apple_scraper.py` script'leri çalıştırılarak hedef uygulamaların tüm yorumları toplanır ve JSON dosyalarına kaydedilir.
2.  **İlk Seviye Analiz (Analyzer API):** n8n veya manuel bir tetikleme ile `analyzer_api.py` içerisindeki `/start_analysis` endpoint'i çağrılır. Bu servis, tüm JSON dosyalarını okur, her bir yorumu LLM ile analiz eder (konu, duygu, özet) ve sonuçları tek bir zenginleştirilmiş Excel raporuna yazar.
3.  **İkinci Seviye Analiz (n8n İş Akışı):**
    - **Başlatma:** n8n iş akışı tetiklenir ve bir önceki adımda oluşturulan Excel dosyasını okur.
    - **İstatistiksel Özet:** "Code" nodu, verileri gruplayarak kendi uygulamanız ve rakipleriniz arasında istatistiksel bir karşılaştırma tablosu hazırlar.
    - **Stratejik Rapor:** Bu özet tablo, LLM'e gönderilir. LLM, bu verileri yorumlayarak "Nerede güçlüyüz?", "Rakiplerin en büyük sorunu ne?" ve "Hangi adımları atmalıyız?" gibi soruları yanıtlayan detaylı bir Markdown metni üretir.
    - **Sonuç:** Akışın sonunda, doğrudan paylaşılabilecek veya okunabilecek, stratejik içgörülerle dolu bir analiz raporu elde edilir.

## Kurulum ve Yapılandırma

Bu projenin tüm bileşenleri (n8n, Ollama, Scraper ve Analyzer Servisleri) **Docker** ile çalışacak şekilde tasarlanmıştır.

1.  **Ön Gereksinimler:**
    - Docker ve Docker Compose'un sisteminizde kurulu olması gerekir.

2.  **Temel Yapılandırma Adımları:**
    - **Uygulama Kimliklerini Belirleyin:** `google_play_apps.json` ve `apps_to_scrape.json` dosyalarını, yorumlarını çekmek istediğiniz kendi uygulamanızın ve rakiplerinizin kimlik bilgileri ile güncelleyin.
    - **Ortam Değişkenlerini Ayarlayın:** `docker-compose.yml` dosyasında veya `.env` dosyasında servislerin kullandığı portları, klasör yollarını ve API adreslerini yapılandırın.
    - **Servisleri Çalıştırın:** Proje kök dizininde `docker-compose up` komutuyla tüm servisleri başlatın.
    - **LLM Modelini Hazırlayın:** Sistem ayağa kalktıktan sonra, n8n iş akışında ve analiz servisinde kullanılan LLM modelini (örneğin, `llama3`) Ollama servisine indirin.
    - **n8n İş Akışını Yükleyin:** `Rakip analiz ve kıyas botu.json` dosyasını n8n arayüzüne aktararak iş akışını kullanıma hazır hale getirin.

## Özelleştirme ve Geliştirme

- **Farklı LLM Modelleri:** `analyzer_api.py` servisinde veya n8n workflow'undaki HTTP Request nodlarında `model` parametresini değiştirerek farklı Ollama modellerini (örn: `mistral`) deneyebilirsiniz.
- **Prompt Mühendisliği:** Analizlerin (konu/duygu sınıflandırma) ve stratejik raporun kalitesini artırmak için `analyzer_api.py` ve n8n içerisindeki prompt'ları kendi ihtiyaçlarınıza göre düzenleyebilirsiniz.
- **Yeni Veri Kaynakları:** Sisteme farklı platformlar (örneğin Şikayetvar, Trustpilot) için yeni scraper'lar ekleyip, bu verileri `analyzer_api.py` servisinin okuyacağı bir klasöre yerleştirerek analiz kapsamını kolayca genişletebilirsiniz.