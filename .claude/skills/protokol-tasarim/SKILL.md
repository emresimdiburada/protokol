---
name: protokol-tasarim
description: PROTOKOL (fitness/takip app, tek dosyalık index.html) üzerinde görsel değişiklik yaparken kullanılır. Renk paleti, kart aksan sistemi, ikon kuralı, buton hiyerarşisi ve tutarlılık kuralları burada tanımlıdır.
---

# PROTOKOL Tasarım Kuralları

## Hedef kitle
Uygulamanın tek kullanıcısı var — kendisi. Karanlık, "gece antrenmanı" hissi
veren, sade bir tema kullanılıyor. Önceliği okunabilirlik ve antrenman
ortasında hızlı tarama (uzun metin okumadan durumu anlamak).

## Renk paleti
- Arkaplan: `--bg` #0b0d10
- Kart: `--card` #14181d, ikinci seviye yüzey (input, chip): `--card-2` #1b2028
- Kenarlık: `--border` #262c35
- Metin: `--text` #e8ecef, ikincil metin: `--muted` #8b95a1
- Ana vurgu (mavi): `--accent` #3b82f6 / `--accent-2` #60a5fa
- Tehlike (kırmızı): `--danger` #ef4444
- Başarı/tamamlandı (yeşil): `--success` #22c55e
- Uyarı (amber): `--warn` #f59e0b
- Su için ayrı camgöbeği: #22d3ee (bir CSS değişkeni değil, `.progress-fill.water` ve `.card-accent-cyan` içinde doğrudan kullanılıyor)

Yeni bir renk eklemeden önce yukarıdakilerden birinin kullanılıp
kullanılamayacağına bak — palet kasıtlı olarak dar tutuluyor.

## Kart aksan sistemi (kategori = renk + ikon)
Her kart aynı gri kutu olursa hiçbiri öne çıkmaz — bu yüzden her kart
**kategorisine göre** bir üst-kenarlık rengi (`.card-accent-*`) VE
card-title'ın başında bir emoji taşır:

| Kategori | Sınıf | Renk | Örnek |
|---|---|---|---|
| Program / antrenman ilerlemesi | `.card-accent-blue` | mavi | İlerleme kartı |
| Su | `.card-accent-cyan` | camgöbeği | Bugünkü Su Tüketimi 💧 |
| Protein / ısınma | `.card-accent-amber` | amber | Bugünkü Protein 🍗, Isınma 🔥 |
| Takviye / sağlık | `.card-accent-green` | yeşil | Bugünkü Takviyeler 💊 |
| Tehlikeli/geri alınamaz işlem | `.card-danger-zone` | kırmızı (üst kenarlık + hafif kırmızı gradient arka plan) | Tehlikeli Bölge ⚠️ |

Nötr/bilgi amaçlı kartlar (Profil, Yedekleme, Program Başlangıç Tarihi vb.)
aksansız kalabilir — her kartı renklendirmek sistemi anlamsızlaştırır, sadece
gerçekten bir kategoriye ait olanlar aksan alır.

Yeni bir kart eklerken önce "bu hangi kategoriye ait?" diye sor; net bir
kategori yoksa aksansız bırak, zorla renk uydurma.

## İkon kuralı
Her `card-title` bir emoji ile başlar (tek istisna: "Gün X · [başlık]"
antrenman kartı — o zaten renkli gün sekmeleriyle ayrışıyor, ayrıca ikon
gerekmiyor). İkon, kategoriyle aynı anlamı taşımalı (💧 su, 🍗 protein, 💊
takviye, 🔥 ısınma, 📈 ilerleme, ⚠️ tehlike, 👤 profil, 💾 yedekleme, 📏
ölçüm, 📊 program, 🗓️ tarih, 🗂️ geçmiş, 🎯 hedef).

## Buton hiyerarşisi
`.btn-primary` (dolu, doygun mavi) **sadece o ekranın tek gerçek birincil
eylemi** için kullanılır — örn. "Seansı Tamamla". Rutin kaydetme eylemleri
(“Kaydet”, “Ölçümü Kaydet” gibi) `.btn-primary-soft` kullanır (yarı saydam
mavi, ince kenarlık) — buton hâlâ net bir CTA gibi görünür ama
"Seansı Tamamla" ile aynı görsel ağırlıkta yarışmaz. Bir ekranda birden
fazla `.btn-primary` varsa muhtemelen hiyerarşi bozulmuştur.

## Tekrarlanan statik içerik: varsayılan kapalı, özet + genişlet
Isınma kartı gibi **her açılışta aynı kalan, uzun talimat metni** içeren
kartlar varsayılan olarak kapalı gösterilir: tek satır özet + "Detaylar ▼"
ile genişleyen tam liste. Kullanıcı her gün aynı 3 paragrafı yeniden
okumak zorunda kalmamalı. Yeni bir "her zaman aynı olan bilgi" kartı
eklerken bu paterni (`.warmup-toggle` + `warmupExpanded` state'i, bkz.
`index.html`) örnek al.

## İlerleme her zaman görünür olmalı
En motive edici bilgi (toplam program ilerlemesi) sadece "Bugün"
sekmesinin en altında değil, **sticky header'da her sekmede görünür**
ince bir ilerleme çubuğuyla da gösteriliyor (`#headerProgressFill`).
Yeni bir "genel durum" metriği eklerken aynı ilkeyi uygula: en önemli
sayı scroll gerektirmeden görünsün.

## Liste içindeki tamamlanma durumu
Bir listede (egzersizler, takviyeler) her satır "yapıldı / yapılmadı"
olabiliyorsa, bunu satırın kendisinde göster (✓ rozeti, dolu checkbox
rengi) — kullanıcı her satırı tek tek okuyarak durumu çıkarmak zorunda
kalmasın. Örnek: `.ex-done-badge`, `.supp-check.checked`.

## Boş durumlar (empty state)
Kuru "Henüz kayıt yok" değil; uygulamanın motivasyonel tonuna uygun,
kısa ve sıcak bir cümle + küçük bir emoji ikon (`.empty-icon`) kullan.
Bkz. Geçmiş sekmesi boş durumu.

## Dokunma hedefleri / spacing (koru, değiştirme)
Butonlar min 48-52px yükseklik, sayaç butonları (su +/-) 56x56px. Bu
zaten doğru — yeni bir dokunulabilir eleman eklerken bu ölçünün altına
düşme.

## ÖNEMLİ teknik kısıt: render() egzersiz input'larını sıfırlar
`index.html`'deki her ekran tamamen `innerHTML` ile yeniden çiziliyor
(React gibi bir virtual-DOM/diffing yok). Bu yüzden "Bugün" ekranında
kullanıcı bir egzersiz ağırlığı yazıp henüz "Seansı Tamamla"ya
basmadan **herhangi bir şey** `render()`'ı tetiklerse (gün sekmesi
değişimi, ısınma detayını aç/kapa gibi), o `<input>` DOM'dan silinip
yeniden yaratılır ve yazılan değer kaybolur.

Bunu `pendingExerciseValues` (global, sayfa içi state) çözüyor: her
`input` olayında `pendingExerciseValues[exId] = value` olarak
saklanıyor, her render'da input'un `value=`'si oradan geri okunuyor,
sadece `completeSession()` tamamlandığında o günün girişleri siliniyor.

**"Bugün" ekranına render() tetikleyen yeni bir buton/toggle eklerken
bunu unutma** — egzersiz input'larının hâlâ görünür olduğu bir anda
tetiklenebiliyorsa, değerlerin `pendingExerciseValues` üzerinden
korunduğundan emin ol, yoksa sessizce veri kaybı olur (bu hatayı bir
kez canlı yakaladık, bkz. git log "visual/usability redesign pass").
