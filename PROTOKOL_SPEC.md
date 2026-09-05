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
- İlk seans (A) blok başlangıç tarihinde (varsayılan 29 Ağustos 2026) başlar.
  Hiç seans tamamlanmamışken bu başlangıç tarihi kullanıcı tarafından
  değiştirilebilir (bkz. Sürüm 2 Ek Özellikleri); ilk seans tamamlanır
  tamamlanmaz kilitlenir, çünkü kayan takvim artık son tamamlanan seansa
  göre ilerler.
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
1. Barbell Deadlift — kg — 4 set × 6-10 tekrar
2. Wide-Grip Lat Pulldown — kg — 3 set × 12-15 tekrar
3. Seated Cable Row — kg — 3 set × 12-15 tekrar
4. Face Pull — kg — 3 set × 12-15 tekrar
5. Single-Arm Dumbbell Row — kg/kol — 3 set × 12-15 tekrar
6. Prone Trap Raise (Duruş) — kg — 3 set × 15 tekrar
7. Chin Tuck (Boyun Retraksiyonu) — dk — 2 set × 30 sn tutuş *(Sürüm 6'da eklendi, Dead Hang'den hemen önce)*
8. Dead Hang (Duruş) — dk — 3 set × maks. asılı kal (hedef 20-30 sn)

**Gün B — Göğüs / Omuz**
1. Dumbbell Bench Press — kg — 4 set × 6-10 tekrar *(değişti: bkz. eşleştirme tablosu)*
2. Incline Dumbbell Press — kg — 4 set × 6-10 tekrar
3. Cable Chest Fly — kg — 3 set × 12-15 tekrar
4. Seated Dumbbell Shoulder Press — kg — 3 set × 12-15 tekrar
5. Lateral Raise — kg — 3 set × 12-15 tekrar
6. Weighted Dip — kg — 4 set × 6-10 tekrar

**Gün C — Sırt / Omuz Sağlığı**
1. Weighted Pull-Up — kg — 4 set × 6-10 tekrar
2. Chest-Supported Dumbbell Row — kg — 3 set × 12-15 tekrar *(değişti: bkz. eşleştirme tablosu)*
3. Cable Reverse Fly — kg — 3 set × 12-15 tekrar *(değişti: bkz. eşleştirme tablosu)*
4. Cable Y-Raise (Alt Makara, Omuz Sağlığı) — kg — 3 set × 12-15 tekrar *(değişti: bkz. eşleştirme tablosu)*
5. Cable External Rotation (Omuz Sağlığı) — kg/kol — 3 set × 12-15 tekrar
6. Farmer's Carry (Duruş/Core) — dk — 3 set × 40m ya da 45-60 sn

**Gün D — Bacak / Kol / Core**
1. Dumbbell Goblet Squat — kg — 4 set × 6-10 tekrar *(değişti: bkz. eşleştirme tablosu)*
2. Romanian Deadlift — kg — 4 set × 6-10 tekrar
3. Dumbbell Bulgarian Split Squat — kg/bacak — 4 set × 6-10 tekrar/bacak *(değişti: bkz. eşleştirme tablosu)*
4. Walking Lunge — kg/bacak — 3 set × 12-15 tekrar/bacak
5. Barbell Curl — kg — 4 set × 6-10 tekrar
6. Triceps Pushdown — kg — 3 set × 12-15 tekrar
7. Plank (Core) — dk — 3 set × 45-60 sn

### Bilimsel Dayanak (Set / Tekrar Şeması)

Set ve tekrar aralıkları, direnç antrenmanı literatüründe yaygın kabul gören
birkaç genel prensibe dayanır: (1) hipertrofi (kas büyümesi) için ~6-15
tekrar aralığının geniş bir "etkili bölge" oluşturduğu, tekrar sayısından çok
haftalık toplam hacim ve çalışma setinin yorgunluğa yakınlığının belirleyici
olduğu; (2) çok eklemli/ağır bileşik hareketlerde (deadlift, squat, bench,
pull-up gibi) daha düşük tekrar (6-10) + göreceli daha yüksek yükün, sinir
sistemi yorgunluğunu yönetilebilir tutarken kuvvet ve kas kütlesini birlikte
geliştirdiği; (3) tek eklemli izolasyon ve kablo/dambıl yardımcı
hareketlerde daha yüksek tekrar (12-15) kullanmanın eklem üzerindeki yükü
azaltıp hedef kas grubuna daha fazla "time under tension" sağladığı; (4) core
ve duruş-stabilizasyon hareketlerinde (plank, farmer's carry, dead hang)
klasik tekrar yerine süre/izometrik tutuşun kas dayanıklılığı ve postür
kontrolü için daha uygun bir uyaran olduğu. Bu genel prensipler, kullanıcının
öncelik sırasına (Duruş → Sırt → Göğüs → Omuz) uygun şekilde uygulanmıştır;
belirli bir akademik kaynağa atıf yapılmamıştır, sadece yaygın antrenman
bilimi pratiğini yansıtır.

### Isınma Protokolü

Her antrenman öncesi, çalışma setlerine geçmeden önce ~8-10 dakikalık bir
ısınma uygulanır (uygulamada "Bugün" ekranında, günün egzersiz listesinden
hemen önce gösterilir):

1. **3-5 dk hafif kardiyo** (eliptik, bisiklet ya da koşu bandı) — kas ve
   eklem sıcaklığını yükseltmek için. Ekipman envanterindeki kondisyon
   aletleri (bkz. aşağıdaki bölüm) bu amaçla kullanılır.
2. **2-3 dk dinamik mobilite** — kol çemberleri, gövde rotasyonu, kalça
   açıcı bacak sallama, omuz/skapula hareketleri. Bantlı ekipman yok;
   kablo istasyonunda çok hafif ağırlıkla face pull / pull-apart aynı işi
   görür.
   - **Sadece Gün A ve Gün C'de** (Sürüm 6): ek olarak **Thoracic
     Extension** (foam roller ya da bench üzerinde, 60 saniye) — bu iki
     gün sırt/omuz ağırlıklı olduğundan torasik omurga mobilitesine
     öncelik veriliyor. Gün B/D'de yok.
3. **Günün ilk (en ağır bileşik) hareketine özel ramp-up setleri** —
   Barbell Deadlift, Dumbbell Bench Press ve Dumbbell Goblet Squat için
   çalışma ağırlığının yaklaşık %40 → %60 → %80'i ile azalan tekrarlarla
   (ör. 8-10-5) 2-3 ısınma seti; Ağırlıklı Pull-Up için ek ağırlık takmadan
   önce birkaç tekrar sadece vücut ağırlığıyla, ardından hafif ek ağırlıkla
   1-2 ısınma seti.

Bu, direnç antrenmanında yaygın kabul gören genel bir ısınma yaklaşımıdır
(genel aerobik aktivasyon → dinamik mobilite → harekete özel ramp-up);
belirli bir akademik kaynağa atıf yapılmamıştır.

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

- `hafta = floor(tamamlanan_seans_sayısı / 4) + 1` (henüz seans yoksa hafta 1).
- **Faz geçişi artık takvim haftasına değil, en son kaydedilen vücut yağı
  yüzdesine bağlı** (Sürüm 6):
  - Hafta ≥ 8 **VE** en son ölçülen vücut yağı ≤ %17 → Faz 2 (Lean Bulk).
  - **Güvenlik sınırı:** hafta ≥ 16 olduğunda, vücut yağı hedefine
    ulaşılmamış olsa bile otomatik olarak Faz 2'ye geçilir (çok uzun süre
    kalori açığında kalmayı engellemek için).
  - Bu ikisi sağlanmadıkça Faz 1 (Recomp) sürer.
  - Eşikler `PHASE2_BODYFAT_THRESHOLD` (17), `PHASE2_MIN_WEEK` (8),
    `PHASE2_SAFETY_WEEK` (16) olarak `index.html`'de sabit tanımlı.
- Hafta 12'ye girildiğinde (ya da 12. hafta içindeyken) faz geçiş kontrolü
  banner'ı gösterilir: kullanıcıyı vücut ölçümlerini güncellemeye davet
  eder ve yeni eşikleri (vücut yağı %17 + hafta 8, en geç hafta 16'da
  otomatik) açıklar. Bu banner'ın gösterildiği hafta (12) sabit kaldı;
  değişen sadece faz geçişinin KENDİSİNİN hangi koşulla tetiklendiği.

## Tasarım

- Mobil öncelikli (iPhone ekran boyutuna göre).
- Sade, **koyu tema** (spor salonunda kolay okunur olsun).
- Büyük dokunma alanları (parmakla kullanım için).
- Tek HTML dosyası: inline `<style>` ve inline `<script>`, dış bağımlılık
  yok (CDN dahi kullanılmaz), pure vanilla JS.
- Tüm veri `localStorage`'da tutulur, sayfa yenilendiğinde veri kaybolmaz.
- `service-worker.js` ile app shell cache'lenir; internet olmadan da açılır
  (bkz. Sürüm 3 Ek Özellikleri).

## Uygulama İçi Ekranlar

1. **Bugün** — sıradaki seans (gün tipi, gecikme durumu), egzersiz girişleri
   ve önceki seansla karşılaştırma, "Seansı Tamamla" butonu, faz/hafta
   bilgisi, faz geçiş kontrolü banner'ı (hafta 12, varsa son ölçüm farkı
   ile birlikte), ilk seans öncesi düzenlenebilir program başlangıç tarihi,
   en az bir seans tamamlandıysa "Son Seansı Geri Al" butonu, ilerleme
   kartında bu haftaki seans sayısı (X/4).
2. **Su** — 700ml şişe sayacı, günlük hedef, ilerleme göstergesi.
3. **Protein** — günlük hedef (otomatik hesaplanan), hızlı ekleme butonları,
   geri al / sıfırla, aktif faz bilgisi, takviye notu.
4. **Geçmiş** — tarihe göre birleşik kayıt listesi (o günün antrenman seansı
   ve/veya su+protein toplamı bir arada), en üstte "Son Seansı Geri Al".
5. **Ayarlar** — profil (kilo, boy, vücut yağı, su hedefi, protein çarpanı),
   yedekleme (indir/geri yükle), yeni ölçüm ekleme + son 5 ölçüm geçmişi,
   program başlangıç tarihi (düzenlenebilir/kilitli), program özeti,
   verileri sıfırlama.

Header'ın alt satırı (`headerSub`), bugünün tarihinin yanında blok hedef
tarihini (`Hedef: 13 Şub 2027`) ve toplam 96 seanstan kaç tanesinin kaldığını
(`96 seanstan 92'si kaldı`) her zaman gösterir.

## Sürüm 2 Ek Özellikleri

- **Düzenlenebilir program başlangıcı:** `sessions.length === 0` iken
  `blockStart` bir tarih seçiciyle değiştirilebilir (bugünden en fazla 3 gün
  öncesine, en fazla 90 gün sonrasına kadar). Değiştirildiğinde
  `blockEnd = blockStart + 168 gün` olarak yeniden hesaplanır. İlk seans
  tamamlandıktan sonra alan kilitlenir ve salt okunur gösterilir.
- **Seans geri alma:** "Seansı Tamamla" davranışı aynı kalır; en az bir
  seans varken Bugün ve Geçmiş sekmelerinde görünen "Son Seansı Geri Al"
  butonu, onay sonrası sadece en son seansı `sessions` dizisinden çıkarır —
  kayan takvim otomatik olarak bir önceki duruma döner.
- **Vücut ölçüm geçmişi:** Ayarlar'daki "Yeni Ölçüm Ekle" bölümü, girilen
  kilo/vücut yağı/vücut yaşını hem `profile`'a hem `measurements` dizisine
  (tarih damgalı) kaydeder. Son 5 ölçüm, bir önceki ölçüme göre farkla
  birlikte listelenir. Hafta 12 faz geçiş banner'ında son iki ölçüm
  arasındaki fark (varsa) gösterilir.
- **Günlük su/protein geçmişi:** `dailyLogs` objesi her gün için
  `{ waterBottles, proteinGrams }` tutar; gün değişip su/protein sıfırlanmadan
  hemen önce o günün toplamı `dailyLogs`'a yazılır, bugünün değerleri de her
  değişiklikte anlık senkronize edilir. Geçmiş sekmesi artık seans ve
  su/protein verisini aynı tarih kartında birleşik gösterir.
- **Geriye uyumluluk:** Eski (sürüm 1) `protokol_state` kaydı yüklenirken
  `measurements` ve `dailyLogs` alanları yoksa boş dizi/obje olarak
  tamamlanır; hata verilmez, mevcut seans/su/protein verisi korunur.

## Sürüm 3 Ek Özellikleri

- **Header'da hedef tarih ve kalan seans:** `headerSub`, tamamlanan seans
  sayısına göre `96 - tamamlanan` (0'ın altına inmez) kalan seansı ve blok
  bitiş tarihini (`Hedef: 13 Şub 2027`) gösterir; blok süresi dolmuşsa
  "6 aylık blok tamamlandı" yazar, kalan seans sayısı yine gösterilir.
- **Yedekleme / geri yükleme:** Ayarlar → Yedekleme kartında "Yedeği İndir"
  tüm `state` objesini `protokol-yedek-TARİH.json` olarak indirir (Blob +
  `<a download>`); "Yedekten Geri Yükle" seçilen JSON dosyasını okur, temel
  alan doğrulaması yapar (`profile`, `sessions` var mı), onay ister ve
  onaylanırsa `localStorage`'a yazıp `loadState()` üzerinden (eski
  sürümlerle geriye uyumlu şekilde) state'i yeniler. Veri sadece cihazda
  tutulduğu için düzenli yedek alınması önerilir.
- **Offline çalışma:** `service-worker.js`, app shell'i (`./`, `./index.html`)
  ilk ziyarette cache'ler; sonraki isteklerde önce ağdan güncel sürümü almayı
  dener, başarısız olursa (internet yok) cache'ten sunar. Yollar GitHub
  Pages'in `/protokol/` alt yolunda da çalışacak şekilde göreceli tutulur;
  `index.html` bu worker'ı `navigator.serviceWorker.register('service-worker.js')`
  ile (göreceli yol) kaydeder.
- **Haftalık tutarlılık göstergesi:** Bugün → İlerleme kartında, hafta
  hesaplamasıyla aynı mantıkla (`tamamlanan seans sayısı % 4`) "Bu hafta:
  X/4 seans" gösterilir — kayan takvim felsefesiyle tutarlı biçimde,
  haftalar takvim günü değil tamamlanan 4'lü seans grupları olarak sayılır.

## Sürüm 4 Ek Özellikleri

- **Set × tekrar / süre reçeteleri:** Her egzersizin `EXERCISES` tanımına
  `prescription: { sets, target }` alanı eklendi (ör. `{ sets:4, target:'6-10
  tekrar' }`). Bugün sekmesinde her egzersiz kartında, hareket adının hemen
  altında "4 set × 6-10 tekrar" gibi net bir hedef gösterilir. Şemanın
  gerekçesi için bkz. [Bilimsel Dayanak](#bilimsel-dayanak-set--tekrar-şeması).
- **Güvenli ilerleme ipucu:** `shouldShowProgressionHint(dayType, exId)`,
  bir hareketin son 2 tamamlanmış kaydını karşılaştırır; değer aynı kalmış
  veya artmışsa egzersiz kartında "💡 İlerleme zamanı" rozeti gösterilir.
  Bu **tamamen görsel bir öneridir** — hiçbir alanı otomatik değiştirmez,
  kullanıcı yine kendi girer.
- **Günlük motivasyon sözü:** Bugün sekmesinin en üstünde, 32 cümlelik
  `MOTIVATION_QUOTES` listesinden güne göre deterministik seçilen (gün
  sayısı % liste uzunluğu) bir söz gösterilir; aynı gün içinde sabit kalır,
  ertesi gün değişir. Header'daki hedef tarih / kalan seans sayısı bilgisi
  (bkz. Sürüm 3) değişmeden aynı şekilde çalışmaya devam eder.

## Sürüm 5 Ek Özellikleri — Görsel/Kullanılabilirlik Geçişi

Kullanıcının "görsel ve kullanılabilirlik açısından yetersiz" geri
bildirimi üzerine yapılan tasarım geçişi. Tüm kurallar
`.claude/skills/protokol-tasarim/SKILL.md` içinde kalıcı olarak
tanımlı; buradaki liste sadece neyin, neden değiştiğinin özeti.

- **Kart aksan sistemi + ikon kuralı:** Önceden tüm kartlar aynı gri
  kutu görünümündeydi, hiçbiri öne çıkmıyordu. Artık her kart
  kategorisine göre 3px'lik renkli bir üst kenarlık taşıyor
  (`.card-accent-blue/cyan/amber/green`) ve `card-title` bir emoji ile
  başlıyor (💧 su, 🍗 protein, 💊 takviye, 🔥 ısınma, 📈 ilerleme, ⚠️
  tehlike, vb.) — nötr/bilgi kartları (Profil, Yedekleme gibi) bilerek
  aksansız bırakıldı.
- **Header'da her zaman görünen ilerleme çubuğu:** Program ilerlemesi
  (tamamlanan/96 seans) artık sadece Bugün sekmesinin en altındaki
  kartta değil, sticky header'da ince bir çubukla (`#headerProgressFill`)
  her sekmede görünüyor.
- **Isınma kartı katlanabilir oldu:** Her gün aynı kalan 3 paragraflık
  talimat artık varsayılan olarak kapalı; tek satır özet ("Kardiyo +
  mobilite + [ilk hareket] ısınma seti") + "Detaylar ▼" ile açılıyor
  (`warmupExpanded` state'i, `toggleWarmup()`).
- **Egzersiz satırlarında tamamlanma rozeti:** Bir egzersize değer
  girildiğinde hareket adının yanında "✓ kaydedildi" rozeti (`.ex-done-badge`)
  beliriyor — antrenman ortasında hangi hareketin kaydedildiğini görmek
  için artık her input'u tek tek okumak gerekmiyor.
- **Buton hiyerarşisi:** "Kaydet" / "Ölçümü Kaydet" gibi rutin kaydetme
  butonları yeni `.btn-primary-soft` stiline (yarı saydam mavi, ince
  kenarlık) geçirildi; dolu/doygun `.btn-primary` artık sadece
  uygulamanın tek gerçek birincil eylemi olan "Seansı Tamamla" için
  kullanılıyor.
- **Tehlikeli Bölge görsel olarak ayrıştı:** Ayarlar → Tehlikeli Bölge
  kartı artık `.card-danger-zone` ile kırmızı üst kenarlık + hafif
  kırmızı gradient arka plan taşıyor, diğer ayar kartlarıyla
  karıştırılmıyor.
- **Daha sıcak boş durum metni:** Geçmiş sekmesi boşken artık kuru
  "Henüz kayıt yok" yerine kısa, motivasyonel bir cümle + ikon
  (`.empty-icon`) gösteriyor.
- **Bug fix — `render()` egzersiz input'larını siliyordu:** Uygulamada
  React benzeri bir diffing yok, her ekran `innerHTML` ile baştan
  çiziliyor. Isınma detayını aç/kapa gibi `render()` tetikleyen yeni
  bir eylem eklenince, kullanıcı henüz "Seansı Tamamla"ya basmadan
  yazdığı egzersiz ağırlıkları sessizce siliniyordu (aynı sorun gün
  sekmesi önizlemesinde de zaten vardı, fark edilmemişti). Artık yazılan
  değerler sayfa içi `pendingExerciseValues` objesinde tutulup her
  render'da input'a geri yazılıyor; sadece `completeSession()`
  tamamlandığında o günün girişleri temizleniyor.

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
  "blockEnd": "2027-02-13",
  "sessions": [
    {
      "date": "2026-08-29",
      "dayType": "A",
      "exercises": { "deadlift": { "value": 100, "unit": "kg" } }
    }
  ],
  "measurements": [
    { "date": "2026-08-29", "weightKg": 90.5, "bodyFatPct": 21.4, "bodyAge": 36 }
  ],
  "dailyLogs": {
    "2026-08-30": { "waterBottles": 5, "proteinGrams": 190 }
  },
  "water": { "date": "2026-08-31", "bottles": 3 },
  "protein": { "date": "2026-08-31", "grams": 80, "history": [20, 30, 30] }
}
```
