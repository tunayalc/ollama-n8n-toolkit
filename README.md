# ollama-n8n-toolkit

N Kolay Ödeme Kuruluşu A.Ş. stajım sırasında geliştirdiğim yerel LLM ve otomasyon odaklı prototip araç seti

## Genel Bakış

`ollama-n8n-toolkit`, Ollama ve n8n etrafında kurguladığım yerel AI iş akışlarını bir araya getiren çatı repo. Buradaki temel fikir, bulut servislerine bağlı kalmadan kullanıcı geri bildirimi, pazar / rakip analizi ve metin tabanlı otomasyon akışları geliştirmekti.

## Alt Modüller

| Modül | Amaç |
| --- | --- |
| `market-pulse-analyzer` | marka / rakip analizi ve yorum içgörüsü üretimi |
| `my-feedback-bot` | kullanıcı geri bildirimlerini yorumlama ve yanıt akışı |

## Teknik Odak Alanları

- yerel LLM kullanımı
- n8n ile otomasyon akışı kurgulama
- mağaza yorumlarından veri toplama
- AI destekli özetleme ve sınıflandırma
- analiz servislerini otomasyona bağlama

## Repo Yapısı

```text
ollama-n8n-toolkit/
|-- market-pulse-analyzer/
|-- my-feedback-bot/
`-- README.md
```

## Kullanılan Teknolojiler

- Python
- Ollama
- n8n
- Flask
