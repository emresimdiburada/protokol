# PROTOKOL — Program İçerik Özeti

`index.html`'in içindeki gerçek `EXERCISES`, `DAY_INFO`, `SUPPLEMENTS` ve
protein/faz mantığından (2026-09-04 itibarıyla, satır numaraları o tarihe
göredir) doğrudan çıkarılmıştır — yorum/tahmin içermez, sadece koddaki
gerçek değerlerin okunabilir listesidir. Ayrı bir konuşmada gözden
geçirilmek üzere hazırlandı.

## Gün A — Sırt / Duruş (`gapToNext: 2`, sıradaki: B)

| Egzersiz | Birim | Set × Hedef |
|---|---|---|
| Barbell Deadlift | kg | 4 set × 6-10 tekrar |
| Lat Pulldown (Geniş Tutuş) | kg | 3 set × 12-15 tekrar |
| Seated Cable Row | kg | 3 set × 12-15 tekrar |
| Face Pull | kg | 3 set × 12-15 tekrar |
| Tek Kol Dumbbell Row | kg/kol | 3 set × 12-15 tekrar |
| Prone Trap Raise (Duruş) | kg | 3 set × 15 tekrar |
| Dead Hang (Duruş) | dk | 3 set × maks. asılı kal (hedef 20-30 sn) |

## Gün B — Göğüs / Omuz (`gapToNext: 2`, sıradaki: C)

| Egzersiz | Birim | Set × Hedef |
|---|---|---|
| Dumbbell Bench Press | kg | 4 set × 6-10 tekrar |
| Incline Dumbbell Press | kg | 4 set × 6-10 tekrar |
| Cable Chest Fly | kg | 3 set × 12-15 tekrar |
| Seated Dumbbell Shoulder Press | kg | 3 set × 12-15 tekrar |
| Lateral Raise | kg | 3 set × 12-15 tekrar |
| Ağırlıklı Dips | kg | 4 set × 6-10 tekrar |

## Gün C — Sırt / Omuz Sağlığı (`gapToNext: 2`, sıradaki: D)

| Egzersiz | Birim | Set × Hedef |
|---|---|---|
| Ağırlıklı Pull-Up | kg | 4 set × 6-10 tekrar |
| Chest-Supported Dumbbell Row | kg | 3 set × 12-15 tekrar |
| Cable Reverse Fly | kg | 3 set × 12-15 tekrar |
| Cable Y-Raise (Alt Makara, Omuz Sağlığı) | kg | 3 set × 12-15 tekrar |
| Cable External Rotation (Omuz Sağlığı) | kg/kol | 3 set × 12-15 tekrar |
| Farmer's Carry (Duruş/Core) | dk | 3 set × 40m ya da 45-60 sn |

## Gün D — Bacak / Kol / Core (`gapToNext: 1`, sıradaki: A)

| Egzersiz | Birim | Set × Hedef |
|---|---|---|
| Dumbbell Goblet Squat | kg | 4 set × 6-10 tekrar |
| Romanian Deadlift | kg | 4 set × 6-10 tekrar |
| Dumbbell Bulgarian Split Squat | kg/bacak | 4 set × 6-10 tekrar/bacak |
| Walking Lunge | kg/bacak | 3 set × 12-15 tekrar/bacak |
| Barbell Curl | kg | 4 set × 6-10 tekrar |
| Triceps Pushdown | kg | 3 set × 12-15 tekrar |
| Plank (Core) | dk | 3 set × 45-60 sn |

Döngü toplamı: A→B→C→D→(A) = 2+2+2+1 = **7 gün** (gecikme yoksa haftada
tam olarak 4 seans, A/B/C/D sırasıyla).

## Isınma (her günün egzersiz listesinden hemen önce)

1. 3-5 dk hafif kardiyo (eliptik, bisiklet ya da koşu bandı)
2. 2-3 dk dinamik mobilite (kol çemberleri, gövde rotasyonu, kalça açıcı
   bacak sallama, omuz/skapula hareketleri)
3. Günün ilk hareketine özel ramp-up: Gün A/B/D için çalışma ağırlığının
   ~%40→%60→%80'i ile azalan tekrarlar (ör. 8-10-5); Gün C (Ağırlıklı
   Pull-Up) için önce vücut ağırlığıyla birkaç tekrar, sonra hafif ek
   ağırlıkla 1-2 set.

## Beslenme / Protein Mantığı

- **Hedef formülü:** `Math.round(vücut ağırlığı kg × proteinPerKg)`
  → varsayılan `proteinPerKg = 2.2` g/kg, varsayılan kilo `90.5` kg →
  varsayılan hedef **199g/gün** (kullanıcı kiloyu/çarpanı değiştirdikçe
  otomatik yeniden hesaplanır).
- **Hızlı ekleme miktarları:** +10g, +20g, +30g, +50g butonları + serbest
  miktar girişi.
- **Su hedefi:** varsayılan 5 şişe × 700ml = 3500ml/gün (Ayarlar'dan
  değiştirilebilir).

## Faz / Hafta Mantığı

- `hafta = floor(tamamlanan_seans_sayısı / 4) + 1` (hiç seans yoksa hafta 1).
- **Hafta ≤ 12 → Faz 1 (Recomp):** "hafif kalori açığı + yüksek protein
  (%[güncel vücut yağı] → hedef ~%16-17 vücut yağı)"
- **Hafta ≥ 13 → Faz 2 (Lean Bulk):** "tanımın üzerine kas ekleme, kalori
  dengeye/hafif fazlaya çekilir"
- Faz geçişi otomatiktir — kullanıcı bir şey seçmez, sadece hafta 12'de bir
  hatırlatma banner'ı görür (vücut ölçümü/fotoğraf güncelleme daveti).
- Bu eşikler (12 hafta ≈ %16-17 vücut yağı hedefi vb.) index.html içinde
  sabit kodlanmış; ayarlardan değiştirilemiyor.

## Takviyeler (günlük checklist, Protein sekmesinde)

| Kalem | Not |
|---|---|
| Whey Protein | Antrenman sonrası |
| Kreatin | 3-5g |
| Magnezyum | MAG Premium ya da Ocean ExtraMag — sadece biri |
| D3K2 | Damla ya da kapsül — sadece biri |
| Kolajen | Whey yerine değil, ek olarak |

Not: "sadece biri" kısıtları sadece metinle belirtiliyor, UI bunu
zorlamıyor (ikisi de aynı anda işaretlenebilir).

## Profil Varsayılanları

- Kilo: 90.5 kg, Boy: 191 cm, Vücut Yağı: %21.4, Vücut Yaşı: 36
- Protein Çarpanı: 2.2 g/kg, Su Hedefi: 5 şişe (700ml)
- Blok: 29 Ağustos 2026 – 168 gün sonrası (13 Şubat 2027), toplam hedef
  **96 seans**
