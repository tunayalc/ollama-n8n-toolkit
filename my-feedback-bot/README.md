# my-feedback-bot

N Kolay Ödeme Kuruluşu A.Ş. stajım sırasında stajyer AI Engineer olarak geliştirdiğim kullanıcı geri bildirimi analizi ve yanıt üretimi prototipi

## Genel Bakış

`my-feedback-bot`, uygulama mağazalarındaki kullanıcı yorumlarını toplayıp bunları AI destekli biçimde yorumlamaya ve yanıt sürecine destek olacak bir akış kurmaya odaklanıyor. Proje, ürün geri bildirimi ile üretken yapay zekayı bir araya getiren bir prototip olarak geliştirildi.

## Proje Kapsamı

| Katman | İçerik |
| --- | --- |
| Veri Toplama | App Store ve Google Play yorumları |
| Yorum İşleme | geri bildirimleri anlamlandırma |
| Otomasyon | yorumların akış içinde işlenmesi |
| Yanıt Desteği | AI destekli müşteri iletişimi mantığı |

## Ana Dosyalar

### `apple_scraper.py`

App Store yorumlarını toplamak için kullanılan scraping bileşeni.

### `google_scraper.py`

Google Play yorum verisini çekmek için kullanılan script.

### `customer_reply_bot.json`

Yorumların işlenmesi ve yanıt akışının otomasyon içinde ilerlemesi için tasarlanmış bot / workflow tanımı.

## Repo Yapısı

```text
my-feedback-bot/
|-- apple_scraper.py
|-- customer_reply_bot.json
|-- google_scraper.py
`-- README.md
```

## Kullanılan Teknolojiler

- Python
- Ollama
- n8n
- kullanıcı geri bildirimi işleme
