[English version →](../../../en/projects/project-08-graph-engineering-first-graph/)

# Loyiha 08. Ish oqimingizni grafik qilib chizing

> Bogʻliq maʼruza: [L14. Yakka loopʼdan grafik muhandisligigacha](./../../lectures/lecture-14-graph-engineering/index.md)

## Nima qilasiz

Bu "Loop" dan "Graph" ga oʻtish loyihasi. Oʻtgan loyihada siz maker-checker loop qurdingiz — implement qilish, tekshirish, fikr-mulohaza, qayta implement qilish — barcha qarorlar bitta agentning kontekst oynasida roʻy berardi. Bu loyihada siz **loop ichida yashiringan tuzilmani eksplisit chizasiz**: tugunlar, chekkalar, umumiy holat va marshrutlash qoidalari, soʻzma-soʻz yozib chiqasiz.

Siz uchta progressiv eksperiment qilasiz: avval P07ʼdagi maker-checker loopʼni eksplisit grafik qilib chizasiz, keyin parallel fan-out/fan-in tugunini qoʻshasiz, soʻngra shartli qaytish chekkasi va inson tasdiqlash tugunini qoʻshasiz. Tugatgach, buni oʻz boshdan kechirgan boʻlasiz: **grafik yangi ixtiro emas — bu sizning loopʼingiz yetarlicha murakkablashgandan keyin aylanadigan narsa.**

## Foydalanadigan vositalar

- Claude Code yoki Codex
- Git
- P07ʼda qurgan maker-checker loopʼingiz (yoki qayta-qayta ishga tushira oladigan istalgan agent workflow)
- Matn muharriri yoki diagramma vositasi (chizish goʻzallik uchun emas — tuzilmani qogʻozga tushirish uchun; `mermaid` ham, qoʻlda yozilgan `graph.md` ham ishlaydi)

## Qadamlar

### Tayyorgarlik

1. P07ʼni tugatgan repoʼdan boshlang, yoki hozir ishlayotgan istalgan agent workflowʼdan.
2. Uchta branch yarating: `p08-explicit-graph`, `p08-parallel`, `p08-human-in-the-loop`.
3. Umumiy holat fayli sifatida `state.md` tayyorlang: talablar, taraqqiyot va tekshiruv natijalari — hammasi shu yerda. Bu grafikning "umumiy ish stoli".

### 1-eksperiment: Loopʼni eksplisit grafik qilib chizing

`p08-explicit-graph` branchʼiga oʻting.

1. **Barcha tugunlarni roʻyxatlang**: P07 maker-checker loopʼining har bir qadamini bitta tugun qilib yozing. Har bir tugun uchun yozing: uning vazifasi, kirishlari, chiqishlari va u agentmi yoki deterministik kodmi.
2. **Barcha chekkalarni chizing**: tugunlar oʻrtasidagi har bir chekkani roʻyxatlang. Ikki maxsus turini belgilang:
   - Shartli chekkalar: tekshiruv oʻtdi/yiqildi — har biri qaysi yoʻldan boradi?
   - Qaytish chekkalari: muvaffaqiyatsizlik qaysi tugunga qaytadi?
3. **Umumiy holatni yozing**: holatdagi maydonlarni (talablar, kod, test natijalari, koʻrib chiqish xulosalari) eksplisit roʻyxatlang va har birini kim oʻqiydi/yozadi.
4. **Marshrutlash qoidalarini yozing**: "keyingi bajarish qayerga ketadi"ni eng sodda if-then tili bilan yozing, masalan:
   ```
   if tekshiruv oʻtdi → merg tuguni
   if tekshiruv yiqildi → implementatsiya tuguni
   if implementatsiya tugunida axborot yetarli emas → tadqiqot tuguni
   ```
5. **Hammasini `graph.md` qilib yozing**: yuqoridagilarni bitta hujjatga aylantiring — mermaid diagrammasi, tugunlar jadvali va marshrutlash qoidalari bilan.
6. **Bu savolga javob bering**: chizib boʻlgach, kamida bitta **yashirin chekka** toping — avval agent kontekstida yashagan, siz hatto mavjudligini bilmagan qaror yoʻli.

### 2-eksperiment: Parallel Fan-out / Fan-in tugunini qoʻshing

`p08-parallel` branchʼiga oʻting.

1. **Parallellashtirish mumkin boʻlgan nuqtani tanlang**: vazifani ikkita mustaqil qismga boʻlish mumkin boʻlgan joyni toping. Masalan:
   - Implementatsiyani ikkita mustaqil modulga boʻling, ikki agent parallel yozadi
   - Tekshiruvni ikkita mustaqil koʻrib chiqishga boʻling: biri test va lint ishga tushiradi, ikkinchisi kod koʻrib chiqish qiladi (turli koʻrsatmalar, turli diqqat)
   - Tadqiqotni ikki yoʻnalishga boʻling, har bir yoʻnalishga bitta agent
2. **Fan-out qoidasini yozing**: umumiy holatda "bu vazifa N ta parallel kichik vazifaga boʻlingan"ni yozib qoʻying, har biri oʻz konteksti va oʻz tuguniga ega.
3. **Fan-in qoidasini yozing**: barcha kichik vazifalar tugagach, natijalarni kim birlashtiradi? Birlashtirish mezonlari nima (masalan, ikkala koʻrib chiqish ham oʻtishi kerak, yoki bittasi yetarli)?
4. **Worktree bilan izolyatsiya qiling**: har bir parallel kichik vazifani oʻz git worktreeʼsida ishlating, fayl toʻqnashuvlarini jismonan oldini olish uchun (13-maʼruzadagi Worktree primitivini qayta koʻrib chiqing).
5. **Bir marta ishga tushiring va yozib oling**: parallellashtirishdan oldin va keyin wall-clock vaqtini, token xarajatini va natija sifatini yozib oling. Parallellashtirish haqiqatan tezroqmi? Yoki muvofiqlashtirish xarajati tejashni yeb qoʻydimi?

### 3-eksperiment: Qaytish chekkasi va inson tasdiqlash tugunini qoʻshing

`p08-human-in-the-loop` branchʼiga oʻting.

Bu uchta eksperimentning eng muhimi. Grafikka ikki turdagi tugun qoʻshasiz:

1. **Shartli qaytish chekkasi**: tekshiruv tuguniga "qisman oʻtdi" yoʻlini qoʻshing — hammasini implementatsiya tuguniga qaytarish oʻrniga, aniq fikr-mulohaza bilan **muammoni keltirib chiqargan tugunga** qayting. Masalan: testlar hammasi oʻtadi, lekin kod koʻrib chiqish talablar notoʻgʻri tushunilganini topadi — implementatsiya tuguniga emas, tadqiqot tuguniga qayting. Bu umumiy holatingiz "muammo qaysi qatlamdan kelganini" yozib qoʻyishini talab qiladi.
2. **Inson tasdiqlash tuguni (human-in-the-loop)**: merg tugunidan oldin inson tugunini qoʻshing. Bu yerga yetganda bajarilish **toʻxtaydi** va siz `state.md` ga "tasdiqlangan" yoki "qaytarilgan" yozishingizni kutadi. Tasdiqlash tugunida timeout qoidasi boʻlishi mumkin: N soatdan keyin javob boʻlmasa, avtomatik qaytarish yoki avtomatik yuqoriga koʻtarish.
3. **Interrupt formatini yozing**: tasdiqlash soʻrovi qanday yozilishi kerak — nima boʻldi, nima oʻzgardi, nima uchun inson kerak, tasdiqlash/qaytarishning oqibatlari nima?
4. **Kamida 2 ta toʻliq pass ishlating**: har bir pass inson tasdiqlash tugunida toʻxtaydi va siz bir marta tasdiqlaysiz yoki qaytarasiz. Yozib oling: sizning tasdiqlash qarorlaringiz tekshiruv tuguni bilan mos keldimi? Tasdiqlash tuguni tekshiruv tuguni oʻtkazib yuborgan narsani ushlab oldimi?

## Natijalarni qanday oʻlchash kerak

| Metrika | 1-eksperiment (Eksplisit grafik) | 2-eksperiment (Parallel) | 3-eksperiment (Inson ishtiroki) |
|---------|-------------------------------|--------------------------|----------------------------------|
| Strukturaviy koʻrinuvchanlik | Nechta yashirin chekka topdingiz? | Umumiy holat parallel kichik vazifalarni qoʻllab-quvvatlay oladimi? | Qaytish chekkasi muammo qatlamini aniq koʻrsata oladimi? |
| Muvaffaqiyatsizlikni lokalizatsiya qilish | Qaysi chekka xato ekanini koʻrsata olasizmi? | Kichik vazifa yiqilganda, qaysi biri ekanini topa olasizmi? | Tasdiqlash qaytarilganda, qaysi qatlam ekanini aytasizmi? |
| Muvofiqlashtirish xarajati | Grafik yozishga qancha vaqt ketdi? | Parallellik tejagan vaqt vs muvofiqlashtirish xarajati | Tasdiqlash kutish vaqti vs ushlangan muammolar qiymati |
| Kuzatuvchanlik | Har bir qadamda nima boʻlayotganini endi koʻra olasizmi? | Har bir kichik vazifaning holati koʻrinadimi? | Tasdiqlash soʻrovlari aniq yozilganmi? |
| Ishonchlilik | Grafik tavsifi haqiqiy ishlashlarga mos keladimi? | Fan-in birlashtirish mezoni ishonchlimi? | Timeout/koʻtarish qoidalari haqiqatan ishga tushadimi? |

## Nima topshirish kerak

- `graph.md` (1-eksperimentning toʻliq grafik tavsifi: mermaid diagrammasi + tugunlar jadvali + chekkalar jadvali + umumiy holat maydonlari + marshrutlash qoidalari)
- 1-eksperimentda topilgan yashirin chekkalar roʻyxati (kamida bittasi)
- 2-eksperimentning fan-out/fan-in qoidalari va bitta parallel ishlash yozuvi (vaqt/xarajat/sifat taqqoslash)
- 3-eksperimentning qaytish chekkasi qoidalari, tasdiqlash tuguni formati va 2 ta inson ishtiroki raund yozuvi
- Yakuniy retro: loopʼdan graphʼga oʻtganingizda, ishlash uslubingiz qanday oʻzgardi? Qaysi vazifalar grafikka arzir, qaysilari arzimaydi?

## Bogʻliq maʼruzalar

- [14-maʼruza — Yakka loopʼdan grafik muhandisligigacha](../../lectures/lecture-14-graph-engineering/index.md)
- [13-maʼruza — Qoʻlda prompt yozishdan avtonom loopʼlargacha](../../lectures/lecture-13-loop-engineering/index.md) (sizning loopʼingiz grafikdagi bitta tugun; bu loyiha tugunning ichki tuzilishini ochib beradi)
- [9-maʼruza — Nega agentlar vaqtidan oldin gʻalabani eʼlon qiladi](../../lectures/lecture-09-why-agents-declare-victory-too-early/index.md) (tekshiruv tuguni nega implementatsiya tugunidan mustaqil boʻlishi kerak — struktura masalasi, prompt masalasi emas)
- [11-maʼruza — Nega kuzatuvchanlik harness ichida boʻlishi kerak](../../lectures/lecture-11-why-observability-belongs-inside-the-harness/index.md) (grafik qancha murakkab boʻlsa, har bir tugunda nima boʻlayotganini koʻrish shuncha zarur)