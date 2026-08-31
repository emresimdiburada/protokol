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

## Görsel Değerlendirme Notları

> `referans-fotograflar/` klasöründeki vücut fotoğraflarına (ön, yan, arka)
> dayanan sadece görsel/gündelik bir izlenimdir — klinik bir postür analizi
> veya tıbbi değerlendirme yerine geçmez. Amaç, programın önceliklerini
> (Duruş → Sırt → Göğüs → Omuz) fotoğraflarla çapraz kontrol etmektir.

- **Duruş:** Yan profil fotoğrafında baş hafifçe öne kaymış ve omuzlar öne
  yuvarlanmış (masa başı / ekran çalışması ile tipik olarak ilişkilendirilen
  bir postür) görünüyor. Bu, kullanıcının kendi önceliklendirmesiyle
  (Duruş #1 sırada) birebir örtüşüyor — programdaki Face Pull, Prone Trap
  Raise, Dead Hang ve Cable Y-Raise hareketleri bu paterni doğrudan
  hedefliyor, sıralamaları korunmalı.
- **Sırt:** Arka fotoğrafta sırt kası gelişimi, vücudun geri kalanına göre
  nispeten az gelişmiş (beklenen bir durum, düzenli sırt çalışması
  geçmişi yoksa). Bu da sırtın Gün A ve Gün C'de haftada 2 kez
  çalışılmasını (programın zaten öngördüğü şekilde) destekliyor.
- **Göğüs / Omuz:** Orantılı ama az gelişmiş; ölçüm ekranındaki %21.4 vücut
  yağı ve 90.5 kg ile tutarlı, orta düzey bir yağ/kas dağılımı gösteriyor.
  Belirgin bir sağ-sol asimetri fotoğraflardan güvenilir şekilde tespit
  edilemedi.
- **Genel:** Vücut yağı fotoğraflardaki karın/bel bölgesi ile tutarlı
  görünüyor. Hafta 12 faz geçiş kontrolünde yeni fotoğraf çekilip bu
  notlarla karşılaştırılması önerilir.

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

> Aşağıdaki liste, kullanıcının ev spor salonundaki gerçek ekipmana göre
> gözden geçirilmiştir. Orijinal önerilerden salonda karşılığı olmayanlar
> (ör. squat rack, leg press makinesi, T-bar row landmine, pec deck)
> eşdeğer bir hareketle değiştirilmiştir. Detay ve gerekçe için bkz.
> [Ekipman Envanteri ve Hareket Eşleştirmesi](#ekipman-envanteri-ve-hareket-eşleştirmesi).

**Gün A — Sırt / Duruş**
1. Barbell Deadlift — kg
2. Wide-Grip Lat Pulldown — kg
3. Seated Cable Row — kg
4. Face Pull — kg
5. Single-Arm Dumbbell Row — kg/kol
6. Prone Trap Raise (Duruş) — kg
7. Dead Hang (Duruş) — dk

**Gün B — Göğüs / Omuz**
1. Dumbbell Bench Press — kg *(değişti: bkz. eşleştirme tablosu)*
2. Incline Dumbbell Press — kg
3. Cable Chest Fly — kg
4. Seated Dumbbell Shoulder Press — kg
5. Lateral Raise — kg
6. Weighted Dip — kg

**Gün C — Sırt / Omuz Sağlığı**
1. Weighted Pull-Up — kg
2. Chest-Supported Dumbbell Row — kg *(değişti: bkz. eşleştirme tablosu)*
3. Cable Reverse Fly — kg *(değişti: bkz. eşleştirme tablosu)*
4. Cable Y-Raise (Alt Makara, Omuz Sağlığı) — kg *(değişti: bkz. eşleştirme tablosu)*
5. Cable External Rotation (Omuz Sağlığı) — kg/kol
6. Farmer's Carry (Duruş/Core) — dk

**Gün D — Bacak / Kol / Core**
1. Dumbbell Goblet Squat — kg *(değişti: bkz. eşleştirme tablosu)*
2. Romanian Deadlift — kg
3. Dumbbell Bulgarian Split Squat — kg/bacak *(değişti: bkz. eşleştirme tablosu)*
4. Walking Lunge — kg/bacak
5. Barbell Curl — kg
6. Triceps Pushdown — kg
7. Plank (Core) — dk

## Ekipman Envanteri ve Hareket Eşleştirmesi

`referans-fotograflar/` klasöründeki salon fotoğrafları incelenerek şu
ekipman tespit edilmiştir:

- **Max Tech çift kule kablo istasyonu (functional trainer)** — ayarlanabilir
  makaralar, düz bar / ip / tek tutamaç aparatları dahil. Lat pulldown,
  cable row, face pull, cable fly, triceps pushdown, external rotation,
  cable reverse fly ve Y-raise gibi hareketlerin tamamı için yeterli.
- **Delta ayarlanabilir (flat/incline) bench**, bacak ataçmanlı, barbell
  tutucu ile birlikte.
- **Barbell + Olympic plakalar** (10/15/20 kg'lık diskler görüldü).
- **Dambıl seti** — hafif (2–4 kg, vinil) ve orta/ağır (hex, ~25 kg'a kadar)
  çiftler.
- **Duvara monteli dip / diz kaldırma istasyonu** (kırmızı ped'li) ve ayrı
  bir **duvar/kapı montajlı pull-up bar**.
- **Kondisyon aletleri** (eliptik x2, recumbent bike, koşu bandı) — programın
  kapsamı dışında, isteğe bağlı ısınma/kardiyo için kullanılabilir.

Tespit edilmeyen ekipman: **squat rack / power rack (emniyet çubuklu)**,
**leg press makinesi**, **T-bar row (landmine) aparatı**, **pec deck
makinesi**. Bu ekipmanı gerektiren orijinal öneriler aşağıdaki gibi
değiştirilmiştir:

| Orijinal Hareket | Gün | Neden Değiştirildi | Yeni Hareket | Kullanılan Ekipman |
|---|---|---|---|---|
| Barbell Bench Press | B | Spotter kolu/rack yok; ağır barbell bench press'te sıkışma riski var | **Dumbbell Bench Press** | Delta bench + dambıllar |
| Barbell Back Squat | D | Squat rack / emniyet çubuğu yok, sırttan barbell ile ağır squat güvenli değil | **Dumbbell Goblet Squat** | Dambıllar |
| Leg Press | D | Leg press makinesi yok | **Dumbbell Bulgarian Split Squat** | Dambıllar + Delta bench (arka ayak yükseltme) |
| T-Bar Row | C | Landmine / T-bar row aparatı yok | **Chest-Supported Dumbbell Row** | Dambıllar + eğimli Delta bench |
| Reverse Pec Deck Fly | C | Pec deck makinesi yok | **Cable Reverse Fly** | Max Tech kablo istasyonu |
| Band Pull-Apart | C | Direnç bandı fotoğraflarda net olarak tespit edilemedi | **Cable Y-Raise (Alt Makara)** | Max Tech kablo istasyonu |

Değişmeyen hareketler (mevcut ekipmanla zaten birebir uyumlu, doğrulandı):
Barbell Deadlift, Wide-Grip Lat Pulldown, Seated Cable Row, Face Pull,
Single-Arm Dumbbell Row, Prone Trap Raise, Dead Hang, Incline Dumbbell
Press, Cable Chest Fly, Seated Dumbbell Shoulder Press, Lateral Raise,
Weighted Dip, Weighted Pull-Up, Cable External Rotation, Farmer's Carry,
Romanian Deadlift, Walking Lunge, Barbell Curl, Triceps Pushdown, Plank.

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

### Mevcut Takviyeler (fotoğraflardan tespit edilen)

> Genel bilgi amaçlıdır, tıbbi tavsiye değildir. Kalıcı/yüksek dozlu
> takviye kullanımı öncesi bir doktor/diyetisyene danışılması önerilir.

| Takviye | İçerik | Programla İlgisi |
|---|---|---|
| Optimum Nutrition Gold Standard Whey (899g, çikolatalı) | Whey protein | Günlük protein hedefine (~199g) katkı için idman sonrası shake |
| Protein OCN Creatine Creapure (250g) | Kreatin monohidrat | Güç/hipertrofi desteği; günde sabit 3–5g, yükleme fazı gerekmez |
| WUPS Hydractive (elma, efervesan) | Elektrolit + Lösin | Yoğun/sıcak antrenman günlerinde terle kaybedilen elektrolitleri desteklemek için |
| Haver MAG Premium | Magnezyum (taurat/malat/sitrat/glisinat) + B6/B12 | Genel toparlanma/uyku desteği |
| Orzax Ocean ExtraMag | Magnezyum (200mg) | **Not:** MAG Premium ile aynı anda kullanılırsa toplam magnezyum dozu istemsizce yüksek olabilir |
| Orzax Ocean Omega 3 Plus | Balık yağı (1200mg, 780mg omega-3) | Genel sağlık, olası eklem/iltihap desteği |
| Orzax Ocean D3K2 (damla + kapsül) | Vitamin D3 + K2 | Kemik/genel sağlık; **damla ve kapsül formu aynı anda değil, tek biri kullanılmalı** |
| Riperin Collagen Peptides (Tip 1&3) | Hidrolize kolajen | Eklem/cilt desteği; tam amino asit profiline sahip olmadığından günlük protein hedefinin ana kaynağı sayılmamalı |
| Cogniviva | Fosfatidilserin, sitikolin, ginkgo, DHA | Bilişsel destek — fitness programıyla doğrudan ilgili değil |
| Orzax Ocean Capillus MEN | Saç/vitamin-mineral | Fitness programıyla doğrudan ilgili değil |

**Programa entegre öneri:**
- Antrenman sonrası: whey shake (günlük protein hedefine ekleme) + günde
  3–5g kreatin (antrenman günü olsun olmasın her gün).
- Sıcak/yoğun terleten günlerde antrenman öncesi/sırası: 1 adet Hydractive
  elektrolit tableti.
- D3K2 ve Omega-3, her iki fazda da günlük rutine dahil edilebilir (D3K2
  için sadece tek format — damla ya da kapsül — seçilmeli).
- Magnezyum için **iki üründen sadece biri** kullanılmalı; ikisinin
  birlikte kullanımı öncesi doktor/diyetisyene danışılması önerilir.
- Kolajen peptit, whey'in yerine değil onun **ek**i olarak düşünülmeli;
  günlük protein hedefi hesaplanırken kolajenden gelen gramaj birebir
  sayılmamalı.

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
