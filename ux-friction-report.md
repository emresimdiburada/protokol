# PROTOKOL — UX Sürtünme Raporu

**Yöntem:** `.claude/skills/run-protokol/driver.py simulate` ile 2026-08-29'dan
2027-01-16'ya kadar (140 gün, 64 tamamlanmış seans, Faz 2/Hafta 17'ye
ulaşmış) deterministik sahte bir kullanım geçmişi üretildi, sonra
`ux-walkthrough` bu "45+ günlük kullanıcı" durumundan başlayarak gerçek bir
dönen kullanıcının izleyeceği 9 adımlık akışı otomatik sürdü ve her adımda
ekran görüntüsü aldı (`.claude/skills/run-protokol/screenshots/walkthrough/`).
`ux-walkthrough` sadece mekanik kanıt topladı (hangi alan dolduruldu, hangi
buton tıklandı, ham DOM durumu); aşağıdaki değerlendirme bu ekran
görüntülerine bakarak eleştirel bir kullanıcı gözüyle bizzat yazıldı.

Not: Bu raporu yazarken sürecin kendisinde de bir hata bulundu ve düzeltildi
— ilk `ux-walkthrough` denemesi `goto_tab()` yardımcı fonksiyonunun "today"
sekmesine DÖNÜŞ yaparken tıklamayı atlaması yüzünden sessizce yanlış
sekmede takılı kaldı (header'daki "PROTOKOL" markası her sekmede göründüğü
için "hazır" kontrolü yanlışlıkla geçiyordu). Bu, uygulamanın değil,
test aracının hatasıydı; `driver.py`'de düzeltildi. Ayrıca simülatörün sınır
koşulu son üretilen seansın tam olarak "bugün"e denk gelmesine izin
veriyordu, bu da Geçmiş'te aynı tarihte iki seans görünmesine yol açıyordu
— bu da test verisi artefaktıydı, gerçek bir kullanıcının asla
karşılaşmayacağı bir durumdu; düzeltildi. Aşağıdaki bulgular bu düzeltmeler
SONRASI temiz bir koşudan alınmıştır.

---

## 1. Belirsiz etiket / ikon / yer

- **"İlerleme zamanı — bu sefer biraz daha ağırlık dene" rozeti neredeyse
  HER egzersizde, HER seansta görünüyor.** 64 seanslık simüle edilmiş
  geçmişte (`shouldShowProgressionHint`: son iki değer azalmadıysa göster)
  ekran görüntülerindeki 7 egzersizin 6-7'sinde bu rozet var — `01_bugun-acilis.png`,
  `02_egzersiz-girisi.png`, `09_gun-B.png`'de aynı amber kutu art arda
  tekrarlıyor. Sürekli ilerleyen bir kullanıcı için bu rozet "özel bir
  öneri" değil, **varsayılan görünüm** haline geliyor — kullanıcı bir süre
  sonra bunu göz ardı etmeyi öğrenir (banner blindness), asıl amacı
  (nadir/anlamlı bir dürtme olmak) kayboluyor.
- **Gün A/B/C/D sekmelerinin kendisi "bugün sırası gelen" ile "gelecek/geçmiş"
  günü ayırt etmiyor** — tek sinyal hangisinin mavi/seçili olduğu
  (`01_bugun-acilis.png`, `09_gun-B.png`). Kullanıcı bu bilgiyi almak için
  mutlaka altındaki karta bakmak zorunda; sekme satırının kendisi tek
  başına "acil mi, değil mi" sorusuna cevap vermiyor.

## 2. Gereğinden fazla tıklama / adım

- Temel günlük işlemler (su +/-, protein hızlı-ekle, egzersiz değeri
  yazma) tek dokunuşla çalışıyor — bu akışlarda fazladan adım bulunmadı.
- Asıl sürtünme **scroll** üzerinden geliyor: haftalık ilerleme detayı
  ("Bu hafta: X/4 seans") İlerleme kartında, Bugün sekmesinin en altında —
  ısınma kartı + 7 egzersiz girişinin TAMAMI geçildikten sonra görünüyor
  (`04_seansi-tamamla.png`'de ancak sayfanın en altına inince görünüyor).
  Sadece haftalık durumunu görmek isteyen bir kullanıcı her seferinde
  bunca içeriği geçmek zorunda. (Header'daki genel ilerleme çubuğu bu
  sorunun bir kısmını zaten hafifletiyor — bkz. madde 4.)

## 3. Eksik geri bildirim

- **En büyük bulgu budur.** "Seansı Tamamla" tıklandığında **HİÇBİR görünür
  onay yok** — ne toast, ne check-mark animasyonu, ne "Harika iş!" mesajı.
  Sayfa sessizce bir sonraki güne geçiyor (`04_seansi-tamamla.png`, log:
  *"tamamlama sonrası GÖRÜNÜR BİR ONAY/TOAST YOK, sayfa sessizce sıradaki
  güne geçti"*). Bu, uygulamanın TEK en önemli eylemi — bir antrenmanı
  bitirmek — ve tam da bu an için hiçbir duygusal/görsel karşılık yok.
  Çelişki: Ayarlar sekmesindeki rutin "Kaydet" butonu bile artık 1.5
  saniyelik yeşil "✓ Kaydedildi" flash'ı gösteriyor (bu oturumda eklendi),
  ama uygulamanın kalbi olan "Seansı Tamamla" hâlâ sessiz.
- Bir seansı tamamlamak **kayan takvimin TÜMÜNÜ** kaydırıyor (sıradaki tüm
  günlerin planlanan tarihini), ama bu geri bildirim hiçbir yerde
  belirtilmiyor — kullanıcı "az önce ne değişti" sorusunu sadece gün
  sekmelerindeki tarihleri manuel karşılaştırarak anlayabilir.

## 4. Görünür olması gerekirken gizli kalan bilgi

- Genel blok ilerlemesi (X/96 seans) artık header'da her sekmede ince bir
  çubukla görünüyor (`08_ilerleme.png` — bu oturumun daha önceki bir
  turunda eklendi) — bu iyi, madde 2'deki sorunu kısmen çözüyor.
  Ama **haftalık kırılım** ("Bu hafta: 1/4 seans") hâlâ sadece Bugün
  sekmesinin en altında, madde 2'de anlatıldığı gibi gömülü.
- **Bir seansı planlanan tarihinden ERKEN tamamlamanın sonucu görünmüyor.**
  `01_bugun-acilis.png`'de "1 GÜN SONRA PLANLANDI" pili açıkça gösteriliyor
  — ama "Seansı Tamamla" butonu yine de tam etkin ve tek tıkla çalışıyor,
  hiçbir yumuşak uyarı ("bu henüz sıran değil, yine de tamamlamak mı
  istiyorsun?") yok. Kayan takvim mantığı tamamen "son tamamlanan seansın
  tarihine" dayandığından, erken tamamlama sessizce TÜM kalan programı bir
  gün öne çeker — kullanıcı bunun farkında olmayabilir.
- Magnezyum/D3K2 için "sadece biri" kısıtı sadece küçük bir metin notu
  (`06_protein-quick-add.png`) — UI bunu hiçbir şekilde zorlamıyor, ikisi
  de aynı anda işaretlenebilir. Bilgi orada ama uygulanmıyor.

---

## Öncelik sırası (öznel)

1. **"Seansı Tamamla" sonrası görünür onay yok** (madde 3) — en yüksek
   etkili, en düşük maliyetli düzeltme; Ayarlar'daki flash pattern zaten
   var, aynı fikir buraya taşınabilir.
2. **İlerleme zamanı rozeti neredeyse her zaman açık** (madde 1) — ya eşik
   sıkılaştırılmalı (ör. sadece art arda 2+ artıştan sonra) ya da rozet
   daha az göze batan bir forma indirilmeli.
3. **Erken tamamlamada yumuşak uyarı yok** (madde 4) — kayan takvimin özü
   bu davranışa dayandığı için, en azından bir kerelik bir onay/bilgi
   satırı eklenebilir.
4. Haftalık kırılımın gömülü kalması (madde 2) ve takviye "sadece biri"
   kısıtının uygulanmaması (madde 4) — daha düşük öncelikli cila.
