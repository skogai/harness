[English Version →](../../../en/projects/project-08-graph-engineering-first-graph/)

> İlgili Ders: [L14. Tek Döngülerden Graf Mühendisliğine](./../../lectures/lecture-14-graph-engineering/index.md)

# Proje 08. İş Akışınızı Bir Graf Olarak Çizin

## Ne Yapacaksınız

Bu, "Loop"tan "Graph"a geçiş projesidir. Önceki derste bir maker-checker loop kurdunuz — uygula, doğrula, geri bildirim, tekrar uygula; tüm kararlar aynı ajanın bağlam penceresinde gerçekleşiyordu. Bu derste yapacağınız şey, **loop'un içinde gizlenen yapıyı açıkça çizmektir**: düğümler, kenarlar, paylaşılan durum, yönlendirme kuralları — kelime kelime netçe yazın.

Üç aşamalı deney yapacaksınız: önce P07'deki maker-checker loop'unu açık bir graf olarak çizin, sonra grafa paralel bir fan-out/fan-in düğümü ekleyin ve son olarak bir koşullu geri alma kenarı ile bir insan onayı düğümü ekleyin. Bitirdiğinizde bir şeyi bizzat hissedeceksiniz: **graf yeni bir icat değil, loop'unuz yeterince karmaşık hale geldiğinde kendisinin dönüştüğü şeydir.**

## Ne Kullanacaksınız

- Claude Code veya Codex
- Git
- P07'de kurduğunuz maker-checker loop (veya tekrar tekrar çalıştırabileceğiniz herhangi bir ajan iş akışı)
- Bir metin düzenleyici veya çizim aracı (çizmek güzel görünmek için değil, yapıyı netleştirmek içindir; `mermaid` veya elle yazılmış `graph.md` ikisi de olur)

## Adımlar

### Hazırlık

1. P07'den sonraki depodan başlayın ya da doğrudan şu anda çalıştırdığınız herhangi bir ajan iş akışını kullanın.
2. Üç dal oluşturun: `p08-explicit-graph`, `p08-parallel`, `p08-human-in-the-loop`.
3. Paylaşılan durum dosyası olarak bir `state.md` hazırlayın: gereksinimler, ilerleme, doğrulama sonuçları buraya yazılır. Bu, graf'ın "ortak çalışma yüzeyidir".

### Deney 1: Loop'u Açık Bir Graf Olarak Çizin

`p08-explicit-graph` dalına geçin.

1. **Tüm düğümleri listeleyin:** P07 maker-checker loop'undaki her adımı bir düğüm olarak yazın. Her düğüm için netleştirin: sorumluluğu, girdisi, çıktısı, ajan mı yoksa deterministic kod mu olduğu.
2. **Tüm kenarları çizin:** Düğümler arasındaki her kenarı listeleyin. İki özel kenara odaklanın:
   - Koşullu kenar: doğrulama geçti/başarısız, hangi kenardan gidilir
   - Geri alma kenarı: başarısızlık hangi düğüme geri döner
3. **Paylaşılan durumu yazın:** Durumda hangi alanların olduğunu (gereksinimler, kod, test sonuçları, inceleme sonuçları) ve kimin okuduğunu/kim yazdığını açıkça listeleyin.
4. **Yönlendirme kurallarını yazın:** En sade if-then diliyle "sırada nereye gidilir" kurallarını yazın, örneğin:
   ```
   if doğrulama geçti → birleştirme düğümü
   if doğrulama başarısız → uygulama düğümü
   if uygulama düğümünde bilgi yetersiz → araştırma düğümü
   ```
5. **`graph.md` olarak yazın:** Yukarıdakileri bir dokümana toparlayın. mermaid ile bir graf çizin, düğüm tablosunu ve yönlendirme kurallarını ekleyin.
6. **Bu soruyu yanıtlayın:** Çizimi bitirdikten sonra, en az bir **eskiden örtük olan kenar** bulun — daha önce ajanın context'inde gizlenmiş, varlığını sizin bile bilmediğiniz bir karar yolu.

### Deney 2: Paralel Fan-out / Fan-in Düğümü Ekleyin

`p08-parallel` dalına geçin.

1. **Paralel çalıştırılabilecek bir nokta seçin:** Görevde iki bağımsız parçaya ayrılabilecek bir yer bulun. Örneğin:
   - uygulamayı iki bağımsız modüle ayırın, iki ajan paralel yazsın
   - doğrulamayı iki bağımsız incelemeye ayırın: biri testleri ve lint'i çalıştırır, biri kod incelemesi yapar (farklı talimatlar, farklı odaklar)
   - araştırmayı iki yöne ayırın, iki ajan birer yolu araştırsın
2. **Fan-out kurallarını yazın:** Paylaşılan durumda "bu görevin N paralel alt göreve ayrıldığını" kaydedin; her alt görev bağımsız bir context'e ve bağımsız bir düğüme sahiptir.
3. **Fan-in kurallarını yazın:** Tüm alt görevler tamamlandığında sonuçları kim birleştirir? Birleştirme standardı nedir (örneğin: yalnızca iki inceleme de geçerse birleştir, yoksa birinin geçmesi yeterli mi)?
4. **Worktree izolasyonu kullanın:** Her paralel alt görev bağımsız bir git worktree'de çalışır ve dosya çarpışmalarını fiziksel olarak önler (Ders 13'teki Worktree ilkesini gözden geçirin).
5. **Bir kez çalıştırın ve kaydedin:** Paralel öncesi ve sonrası duvar saati süresini, token tüketimini ve sonuç kalitesini kaydedin. Paralel gerçekten daha hızlı mı? Yoksa koordinasyon yükü kazanılan zamanı mı yedi?

### Deney 3: Bir Geri Alma Kenarı ve Bir İnsan Onayı Düğümü Ekleyin

`p08-human-in-the-loop` dalına geçin.

Bu, üç deneyin en önemlisidir. Grafa iki tür düğüm ekleyeceksiniz:

1. **Koşullu geri alma kenarı:** Doğrulama düğümüne bir "kısmen geçti" yolu ekleyin — her şeyi uygulama düğümüne geri göndermek yerine, spesifik geri bildirimle **sorunu üreten düğüme** dönün. Örneğin: testlerin hepsi geçiyor ama kod incelemesi gereksinim anlayışının yanlış olduğunu buluyorsa, uygulama düğümü yerine araştırma düğümüne geri dönün. Bu, paylaşılan durumunuzun "sorunun hangi katmanda olduğunu" kaydetmesini gerektirir.
2. **İnsan onayı düğümü (Human-in-the-loop):** Birleştirme düğümünden önce bir insan düğümü ekleyin. Buraya geldiğinde graf **durur** ve sizin `state.md`'ye "onay" veya "geri çevir" yazmanızı bekler. Onay düğümü bir zaman aşımı kuralına sahip olabilir: N saat sonra yanıt verilmezse otomatik geri çevirir veya otomatik yükseltir.
3. **Interrupt formatını yazın:** Onay isteğini nasıl net tutacağınız — ne oldu, ne değişti, neden bir insana ihtiyaç var, onay/geri çevirmenin sonuçları neler.
4. **En az 2 tam tur çalıştırın:** Her turda insan onayı düğümüne ulaşın ve kendiniz bir kez onaylayın veya geri çevirin. Kaydedin: onay kararınız doğrulama düğümünün yargısıyla tutarlı mı? Onay düğümü, doğrulama düğümünün yakalayamadığı bir şeyi durdurdu mu?

## Sonuçları Nasıl Ölçersiniz

| Metrik | Deney 1 (Açık graf) | Deney 2 (Paralel) | Deney 3 (İnsan-ortada) |
|------|----------------|--------------|------------------|
| Yapısal görünürlük | Kaç örtük kenar buldunuz? | Paylaşılan durum paralel alt görevleri destekleyebiliyor mu? | Geri alma kenarı sorun katmanını hassas şekilde bulabiliyor mu? |
| Başarısızlık konumlandırma | Başarısızlıkta hangi kenarın yanlış olduğunu doğrudan söyleyebiliyor musunuz? | Paralel bir alt görev başarısız olduğunda hangisini konumlandırabiliyorsunuz? | Onay geri çevirdiğinde hangi katmanın sorunu olduğunu gösterebiliyor musunuz? |
| Koordinasyon yükü | Graf'ı yazmak ne kadar sürdü? | Paralelliğin kazandırdığı zaman vs koordinasyon yükü | Onay bekleme süresi vs durdurulan sorunun değeri |
| Gözlemlenebilirlik | Her adımda ne olduğu artık görünüyor mu? | Her paralel alt görevin durumu görünür mü? | Onay isteği yeterince net yazılmış mı? |
| Güvenilirlik | Graf açıklaması gerçek çalışmayla tutarlı mı? | Fan-in birleştirme standardı güvenilir mi? | Zaman aşımı/yükseltme kuralları gerçekten tetikleniyor mu? |

## Ne Teslim Edeceksiniz

- `graph.md` (Deney 1'in tam graf açıklaması: mermaid grafı + düğüm tablosu + kenar tablosu + paylaşılan durum alanları + yönlendirme kuralları)
- Deney 1'de bulunan örtük kenar listesi (en az bir tane)
- Deney 2'nin fan-out/fan-in kuralları ve bir paralel çalışma kaydı (zaman/maliyet/kalite karşılaştırması)
- Deney 3'ün geri alma kenarı kuralları, onay düğümü formatı ve 2 tur insan-ortada kaydı
- Son öz değerlendirme: loop'tan graf'a, çalışma biçiminizde ne değişti? Hangi görevler graf çizmeye değer, hangileri değil?

## İlgili Dersler

- [Lecture 14 — Tek Döngülerden Graf Mühendisliğine](../../lectures/lecture-14-graph-engineering/index.md)
- [Lecture 13 — Manuel Prompting'den Otonom Loop'lara](../../lectures/lecture-13-loop-engineering/index.md) (loop'unuz graf'taki bir düğümdür; bu proje düğümün iç yapısını açmaktır)
- [Lecture 09 — Ajanlar neden zaferi çok erken ilan eder](../../lectures/lecture-09-why-agents-declare-victory-too-early/index.md) (verify düğümü neden implement düğümünden bağımsız olmalı; graf'ta bu yapısal bir sorundur)
- [Lecture 11 — Gözlemlenebilirlik neden harness'ın bir parçasıdır](../../lectures/lecture-11-why-observability-belongs-inside-the-harness/index.md) (graf ne kadar karmaşıksa, her düğümün ne yaptığını görmek o kadar gerekli olur)