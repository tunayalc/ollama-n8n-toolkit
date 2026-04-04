# market-pulse-analyzer

N Kolay Ödeme Kuruluşu A.Ş. stajım sırasında stajyer AI Engineer olarak geliştirdiğim pazar ve rakip analiz prototipi

## Genel Bakış

`market-pulse-analyzer`, uygulama mağazalarından toplanan kullanıcı yorumlarını işleyip yerel LLM desteğiyle pazar ve rakip içgörüsü üretmek için geliştirildi. Proje; veri toplama, düzenleme, analiz ve otomasyon entegrasyonu katmanlarını bir araya getiriyor.

## Proje Kapsamı

| Katman | İçerik |
| --- | --- |
| Veri Toplama | Google Play ve App Store yorumları |
| Düzenleme | yorumları analiz edilebilir yapıya getirme |
| Analiz | Ollama destekli yorum yorumu ve içgörü üretimi |
| Otomasyon | n8n akışına bağlanabilecek servis mantığı |

## Ana Dosyalar

### `scraper_service_google.py`

Google Play yorumlarını uygulama kimliği üzerinden servis mantığıyla çeken bileşen.

### `run_scraper_google.py`

Google scraping akışını tetikleyen yürütme script'i.

### `apple_scraper.py`

App Store tarafındaki kullanıcı yorumlarını toplayan yardımcı dosya.

### `analyzer_api.py`

Toplanan yorumları okuyup Ollama tabanlı analiz çıktısı üreten ana servis.

### `competitor_analysis_bot.json`

n8n tarafında kullanılabilecek otomasyon akışı tanımı.

## Repo Yapısı

```text
market-pulse-analyzer/
|-- analyzer_api.py
|-- apple_scraper.py
|-- competitor_analysis_bot.json
|-- run_scraper_google.py
|-- scraper_service_google.py
`-- README.md
```

## Kullanılan Teknolojiler

- Python
- Flask
- Ollama
- n8n
- App Store / Google Play veri işleme
