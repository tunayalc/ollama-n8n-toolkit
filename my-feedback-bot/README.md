# Müşteri Geri Bildirim Yanıtlama Otomasyonu

Bu proje, Google Play Store ve Apple App Store gibi platformlardan gelen müşteri yorumlarını otomatik olarak toplayan, yapay zeka ile analiz eden ve her bir yoruma uygun, kişiselleştirilmiş yanıtlar üreten bir otomasyon sistemidir.

Projenin temel amacı, müşteri destek ekiplerinin üzerindeki yükü azaltmak, yanıt tutarlılığını artırmak ve marka imajını güçlendirmektir. Tüm sistem, **Docker** kullanılarak konteynerler içinde çalıştırılmaktadır.

## Bileşenler

### 1. Veri Toplama (Scrapers)

- **`google_scraper.py`**: Python ve `Flask` kullanılarak geliştirilmiş bir servistir. Ortam değişkenleri üzerinden belirtilen Google Play uygulama ID'si için en yeni yorumları çeker.
- **`apple_scraper.py`**: `apps_config.json` dosyasında tanımlanan Apple App Store uygulama ID'leri için en yeni yorumları çeken bir Python script'idir.

### 2. İş Akışı Otomasyonu (n8n)

Tüm sürecin orkestrasyonunu yapar. `Müşteri yorum yanıtlama botu.json` dosyasında tanımlanan iş akışı sayesinde veriyi okur, işler, yapay zekaya gönderir ve sonuçları birleştirir.

### 3. Yapay Zeka (Ollama & Llama 3)

Metin anlama ve üretme görevlerini yerine getirir. Tamamen lokalde çalıştığı için veri gizliliği sağlar ve API maliyetlerini ortadan kaldırır. n8n'den gelen API isteklerini yanıtlar.

## n8n İş Akışı Nasıl Çalışır?

1.  **Başlat**: Akış tetiklenir.
2.  **Dosyaları Oku**: Scraper'lar tarafından oluşturulan `google_reviews.json` ve `apple_reviews.json` dosyalarını okur.
3.  **Verileri Birleştir ve Döngüye Al**: Tüm yorumları tek bir listede birleştirir ve her bir yorumu tek tek işlemek üzere döngüye sokar.
4.  **Duygu Analizi (Yargıç Modeli)**:
    - Yorum metni, Ollama'ya yorumun duygusunu "Olumlu", "Olumsuz" veya "Nötr" olarak sınıflandırması için özel bir prompt ile gönderilir. Bu, süreci hızlandıran bir ön analiz adımıdır.
5.  **Koşullu Dallanma (IF)**:
    - Analiz sonucuna göre akış "Olumlu" veya "Olumsuz" olarak ikiye ayrılır.
6.  **Yanıt Üretimi**:
    - **Eğer yorum "Olumsuz" ise**: "Çözüm Odaklı Yanıt Üret" adımına gidilir. Burada LLM'ye; empatik, çözüm odaklı, markayı koruyan ve müşteriyi doğru kanala (örneğin destek e-postası) yönlendiren bir yanıt oluşturması için detaylı kurallar verilir.
    - **Eğer yorum "Olumlu" veya "Nötr" ise**: "Teşekkür Yanıtı Üret" adımına gidilir. Burada LLM'ye; müşteriye içten bir teşekkür eden, kısa ve samimi bir yanıt oluşturması istenir.
7.  **Sonuç**: Her yorum için üretilen özelleştirilmiş yanıt, akışın sonunda hazır hale gelir.

## Kurulum ve Çalıştırma

Bu projenin tüm bileşenleri (n8n, Ollama, Scraper servisleri) **Docker** ile çalışacak şekilde tasarlanmıştır.

1.  **Ön Gereksinimler:**
    - Docker ve Docker Compose'un sisteminizde kurulu olması gerekir.

2.  **Temel Yapılandırma Adımları:**
    - **Uygulama ID'lerini Belirleyin:** Google Scraper için ortam değişkenlerini ve Apple Scraper için `apps_config.json` dosyasını, yorumlarını çekmek istediğiniz hedef uygulamaların ID'leri ile güncelleyin.
    - **Servisleri Çalıştırın:** Proje için hazırlanmış `docker-compose.yml` dosyasını kullanarak tüm servisleri başlatın.
    - **LLM Modelini Hazırlayın:** Sistem ayağa kalktıktan sonra, n8n iş akışında kullanılan LLM modelini (örneğin, `llama3`) Ollama servisine indirin.
    - **n8n İş Akışını Yükleyin:** `Müşteri yorum yanıtlama botu.json` dosyasını n8n arayüzüne aktararak iş akışını kullanıma hazır hale getirin.

## Özelleştirme ve Geliştirme

- **Farklı LLM Modelleri**: n8n workflow'undaki HTTP Request nodlarında `model` parametresini değiştirerek farklı Ollama modellerini (örn: `mistral`) kullanabilirsiniz.
- **Prompt Mühendisliği**: Yanıtların kalitesini ve tarzını iyileştirmek için n8n içerisindeki prompt'ları kendi marka dilinize göre düzenleyebilirsiniz.
- **Yeni Veri Kaynakları**: Sisteme Şikayetvar, Twitter gibi yeni veri kaynakları için scraper'lar ekleyip n8n workflow'una kolayca entegre edebilirsiniz.