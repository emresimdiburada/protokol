# PROTOKOL — Spesifikasyon

Tek dosyalık (index.html), backend'siz, localStorage tabanlı bir fitness takip
uygulaması. iPhone'da Safari üzerinden "Ana Ekrana Ekle" ile PWA benzeri
kullanım için tasarlandı.

## Kullanıcı Profili

- Erkek, 38 yaş, 191 cm, 90.5 kg
- Vücut yağı: %21.4, Vücut Yaşı: 36
- Hedef: 6 ayda maksimum gelişim, "Kaptan Amerika" fizik hedefi
- Öncelik sırası: **Duruş, Sırt, Göğüs, Omuz** (bacak/kol ikincil ama gerçek
  bir antrenman günü var — göz ardı edilmiyor)

## Program Yapısı

4 günlük split:

| Gün | İçerik |
|-----|--------|
| A | Sırt / Duruş |
| B | Göğüs / Omuz |
| C | Sırt / Omuz Sağlığı |
| D | Bacak / Kol / Core |

- Hafta Pazar günü başlar.
- Hedef antrenman günleri: **Pazar (A), Salı (B), Perşembe (C), Cumartesi (D)**.
- 6 aylık blok: **29 Ağustos 2026 – 13 Şubat 2027**.
- Hafta 12'de bir **"faz geçiş kontrolü"** ekranı/uyarısı gösterilir
  (vücut ölçümlerini yeniden değerlendirme hatırlatması).

## Kayan Takvim Mantığı (ÖNEMLİ)

- Hesaplama **sabit takvime göre değil**, en son **tamamlanmış seansın
  tarihine** göre yapılır.
- Bir gün kaçırılırsa, sıradaki **tüm** seanslar otomatik olarak aynı
  gecikme kadar kayar.
- "Bugünün antrenmanı" her zaman `son tamamlanan seans tarihi + planlanan
  aralık` olarak hesaplanır; sabit hafta/gün isimlerine göre değil.
- Planlanan aralıklar (gün cinsinden, seans tipinden bir sonrakine):
  A→B: 2, B→C: 2, C→D: 2, D→A: 1 (döngü toplamı 7 gün, programda kayma
  yoksa haftalık Pazar/Salı/Perşembe/Cumartesi ritmine denk gelir).
- İlk seans (A) blok başlangıç tarihinde (29 Ağustos 2026) başlar.
- Uygulama, tamamlanan seans sayısını da programın "hafta" ilerlemesi için
  kullanır (bkz. Faz hesaplama) — böylece kaçırılan antrenmanlar sadece
  takvimi değil, faz geçişini de gerçekçi biçimde geciktirir.

## Egzersiz Kaydı

- Her egzersizde kullanıcı **kg** (veya **süre**, hareket tipine göre)
  girebilir.
- Geçmiş kayıtlarla karşılaştırma gösterilir (bir önceki seansta bu hareket
  kaç kg / kaç dakikaydı).
- Her egzersizin yanında **YouTube arama linki** olur (hareketin İngilizce
  ismiyle arama sorgusu oluşturan bir link):
  `https://www.youtube.com/results?search_query=...`
- Tek kol / tek bacak ile yapılan hareketlerde net şekilde **"kg/kol"** veya
  **"kg/bacak"** etiketi gösterilir (toplam ağırlıkla karıştırılmaz).

### Egzersiz Listesi (öncelik sırasına göre)

**Gün A — Sırt / Duruş**
1. Barbell Deadlift — kg
2. Wide-Grip Lat Pulldown — kg
3. Seated Cable Row — kg
4. Face Pull — kg
5. Single-Arm Dumbbell Row — kg/kol
6. Prone Trap Raise (Duruş) — kg
7. Dead Hang (Duruş) — dk

**Gün B — Göğüs / Omuz**
1. Barbell Bench Press — kg
2. Incline Dumbbell Press — kg
3. Cable Chest Fly — kg
4. Seated Dumbbell Shoulder Press — kg
5. Lateral Raise — kg
6. Weighted Dip — kg

**Gün C — Sırt / Omuz Sağlığı**
1. Weighted Pull-Up — kg
2. T-Bar Row — kg
3. Reverse Pec Deck Fly — kg
4. Band Pull-Apart (Omuz Sağlığı) — kg
5. Cable External Rotation (Omuz Sağlığı) — kg/kol
6. Farmer's Carry (Duruş/Core) — dk

**Gün D — Bacak / Kol / Core**
1. Barbell Back Squat — kg
2. Romanian Deadlift — kg
3. Leg Press — kg
4. Walking Lunge — kg/bacak
5. Barbell Curl — kg
6. Triceps Pushdown — kg
7. Plank (Core) — dk

## Su Takibi

- **700ml'lik şişe** bazlı sayaç.
- Kaç şişe içildiği takip edilir, günlük hedef kullanıcı tarafından
  belirlenebilir (varsayılan: 5 şişe ≈ 3.5L).
- Gün değiştiğinde sayaç otomatik sıfırlanır (tarihe göre).

## Beslenme / Protein Takibi

- Günlük protein hedefi otomatik hesaplanır: **vücut ağırlığı (kg) × 2.2
  g/kg** (90.5 kg × 2.2 ≈ **199 g**). Çarpan ve kilo ayarlanabilir.
- Gün içinde yenen protein miktarı **manuel** girilebilir:
  - Hızlı ekleme butonları (ör. +10g, +20g, +30g, +50g)
  - Serbest miktar girişi
  - **"Geri al"** (son eklemeyi geri alır) ve **"Sıfırla"** (günü sıfırlar)
    butonları
- **2 fazlı beslenme stratejisi**, programın "hafta"sına göre otomatik seçilir:
  - **Hafta 1–12 — Faz 1: Recomp.** Hafif kalori açığı + yüksek protein.
    Hedef: %21.4 → ~%16–17 vücut yağı.
  - **Hafta 13–24 — Faz 2: Lean Bulk.** Görünür tanımın üzerine kas ekleme;
    kalori dengeye/hafif fazlaya çekilir.
- Uygulama hangi haftada olduğunu (kayan takvim mantığına göre tamamlanan
  seans sayısından türetilen hafta) baz alarak doğru fazı otomatik gösterir.

## Faz / Hafta Hesabı

- `hafta = ceil(tamamlanan_seans_sayısı / 4)` (henüz seans yoksa hafta 1).
- Hafta ≤ 12 → Faz 1 (Recomp), Hafta ≥ 13 → Faz 2 (Lean Bulk).
- Hafta 12'ye girildiğinde (ya da 12. hafta içindeyken) faz geçiş kontrolü
  banner'ı gösterilir: kullanıcıyı vücut ölçümlerini güncellemeye ve Faz 2'ye
  geçişi onaylamaya davet eder.

## Tasarım

- Mobil öncelikli (iPhone ekran boyutuna göre).
- Sade, **koyu tema** (spor salonunda kolay okunur olsun).
- Büyük dokunma alanları (parmakla kullanım için).
- Tek HTML dosyası: inline `<style>` ve inline `<script>`, dış bağımlılık
  yok (CDN dahi kullanılmaz), pure vanilla JS.
- Tüm veri `localStorage`'da tutulur, sayfa yenilendiğinde veri kaybolmaz.

## Uygulama İçi Ekranlar

1. **Bugün** — sıradaki seans (gün tipi, gecikme durumu), egzersiz girişleri
   ve önceki seansla karşılaştırma, "Seansı Tamamla" butonu, faz/hafta
   bilgisi, faz geçiş kontrolü banner'ı (hafta 12).
2. **Su** — 700ml şişe sayacı, günlük hedef, ilerleme göstergesi.
3. **Protein** — günlük hedef (otomatik hesaplanan), hızlı ekleme butonları,
   geri al / sıfırla, aktif faz bilgisi.
4. **Geçmiş** — tamamlanmış seans listesi ve egzersiz bazlı ilerleme.
5. **Ayarlar** — kilo, boy, vücut yağı, su hedefi, protein çarpanı, verileri
   sıfırlama.

## Veri Modeli (localStorage, tek anahtar: `protokol_state`)

```json
{
  "profile": {
    "weightKg": 90.5,
    "heightCm": 191,
    "bodyFatPct": 21.4,
    "bodyAge": 36,
    "proteinPerKg": 2.2,
    "waterGoalBottles": 5
  },
  "blockStart": "2026-08-29",
  "sessions": [
    {
      "date": "2026-08-29",
      "dayType": "A",
      "exercises": { "deadlift": { "value": 100, "unit": "kg" } }
    }
  ],
  "water": { "date": "2026-08-31", "bottles": 3 },
  "protein": { "date": "2026-08-31", "grams": 80, "history": [20, 30, 30] }
}
```
