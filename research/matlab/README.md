# Gereksinimin algilayici tarafindan genisletilmesi

MATLAB R2018b ve sonrasi, ek toolbox gerektirmez.

## Calistirma

```matlab
cd('C:\Users\volka\OneDrive\Belgeler\MATLAB\RequirementUncertainity')
run_requirement_demo
```

`outputs` altina 7 aciklamali PNG ve duzenlenebilir FIG, 4 ham otomat PNG,
CSV olcumleri ve simulation_data.mat yazilir. Yalnizca bu adlandirilmis
uretilen dosyalar tekrar calistirmada yenilenir. Grafikler batch kullanim icin
gorunmez olusturulur; `openfig('outputs/01_observers.fig')` ile acilabilir.

## Son konusmayla baglanti

19 Eylul: dokuz cumle parcasi, belirsizlik isaretli hucreler ve iki ust
capraz farkliysa siyah hucre uretimi. Bu sonuncusu Wolfram Kural 90'dur.
21 Eylul: satir entropisi ve ucgenin tasarim kararlariyla daralmasi sorusu.
ZIP sadece chat.txt ve chat.md iceriyor; raporlar ve cizimler dahil degil.
Bu nedenle demo tohumu [0 0 1 0 1 1 0 0 1] temsili ve elle atanmistir.
Gercek cumlenin dogrulanmis kodlamasi oldugu iddia edilmez.

## Model

Ilk satir r(0), sonraki satirlar isleme adimlaridir. Her hucre ikilidir.
Baslangicta 1, kullanicinin isaretledigi acik konuyu; sonraki satirlarda
1, kuralla uretilen aktif simgesel durumu temsil eder. Sonraki her siyah
hucrenin gercek bir belirsizlik veya tasarim alternatifi oldugu varsayilmaz.

Algilayici bu ilk prototipte bir yerel donusum kuralidir. 90, 30, 110 veya
204 sayilari insan kapasitesinin siralamasi degildir. Gozlem cozunurlugu
ayri olarak observe_expansion ile temsil edilir, evrime geri beslenmez.

Mahalle kodu q = 4*sol + 2*merkez + sag; cikis bitget(kural,q+1).
Kural 90: yeni(i) = xor(eski(i-1),eski(i+1)).
Kural 204: yeni(i)=eski(i). Guncelleme eszamanlidir.
Genislik n+2*T, n tohum uzunlugu, T adim sayisi. Acik gri alan o andaki
nedensel pencerenin disidir; pencere her adimda iki hucre genisler.
Dis ortam baslangicta 0, kullanilan kuralla gelisir; periyodik sarma yoktur.

## Ornekler

1. Ayni dokuz bit, dort algilayici kurali.
2. Klasik tek hucreli Kural 90 ile dokuz bitli tohum karsilastirmasi.
3. Tekli ve ikili desen entropileri; buyuyen ve sabit pencere farki.
4. Ayni fiziksel/simgesel evrimin 1, 3 ve 9 hucrelik bloklarla gozlenmesi.
   Sabit bloklar, cogunluk kurali, esitlikte beyaz. Kismi bloklar gosterilmez.
5. 28. adimdan sonra disaridan daralan merkez bandi disinda sifira sabitleme.
   Bu ek bir tasarim politikasi varsayimidir; karar etkisini gostermek icindir.
   Kuralin dogal sonucu ya da gercek alternatif elemesinin kaniti degildir.
6. 25. ve 50. adimda algilayici degisimi: 90 -> 30 -> 110.
7. Sekiz acik kural hipotezinden, gozlenen uc merkez hucreyle uyumsuz olanlari
   eleme. Es onsel agirliklar ve hatasiz gozlem varsayilir. Piksel daraltmadan
   farkli olarak burada gercekten tanimli sonlu bir hipotez kumesi elenir.

## Entropi ve yorumlama

H1: satirdaki siyah/beyaz frekansinin Shannon entropisi, 0..1 bit/hucre.
H2: ust uste binen, sarilmayan 00/01/10/11 ikililerinin entropisi, 0..2 bit/cift.
H4: dort bitlik desenlerin entropisi, 0..4 bit/desen; kisa satirda kestirim zayiftir.
H2/2 yalnizca gorsel olceklendirmedir; entropi hizi kestirimi degildir.
Bir satir kisa ise desen sayisi yetersiz olabilir; yeterli uzunluk yoksa NaN.
Buyuyen pencere ve sabit merkez penceresi ayri raporlanir; dis gri dolgu sayilmaz.
Kararli ve serbest durum ayni buyuyen pencereyle karsilastirilir; sifira
sabitlenen hucreler bu karsilastirmada dahildir, dolayisiyla dusus politikanin
matematiksel etkisini de yansitir.

Bilinen tek tohum ve kuralla tum resim deterministiktir. Pozitif H1/H2,
resmin tamaminda olasiliksal belirsizlik yaratildigi anlamina gelmez.
Gorsel duzensizlik, semantik gereksinim belirsizligi ve hipotez belirsizligi
ayri kavramlardir. Hicbir monoton artis/azalis veya insan modeli kanitlanmaz.
Es olasilikli 8 alternatif log2(8)=3 bit veya ln(8)=2.079 nat verir.
Bu degeri piksel entropisine zorla esitlemeyin. Ornek 7'de baslangic 3 bit
olmasi gercekten 8 tanimli es olasilikli KURAL hipotezi olmasindandir.

## Kendi deneyiniz

```matlab
seed = [0 1 0 1 1 0 0 1 0];
r = expand_requirement(seed,90,60);
imagesc(r.x,0:r.steps,r.bits); colormap([1 1 1;0 0 0]); caxis([0 1]);
xlabel('Hucre'); ylabel('Adim');
m = measure_expansion(r,4);
figure; plot(m.Step,m.H2_bits_per_pair); ylabel('H2 bit/cift');
```

Dogal dil kodlamasini ayri tabloda saklayin: parca, verilen bit, gerekce,
kodlayan kisi. Tek cumleden otomatik anlam cikaran bir model burada yoktur.
`test_requirement_ca` kural tablosu, bilinen Kural 90 deseni, sinir kosullari
ve olasilik hesaplarini kontrol eder. Bir sonraki arastirma adimi, kural ve
baslangic kodlamasinin insan yorumlariyla deneysel baglantisini sinamaktir.

## Kaynaklar

- Wolfram (2023), Computational Foundations for the Second Law of Thermodynamics:
  https://writings.stephenwolfram.com/2023/02/computational-foundations-for-the-second-law-of-thermodynamics/
- Rule 90: https://mathworld.wolfram.com/Rule90.html
- Cellular automata: https://mathworld.wolfram.com/CellularAutomaton.html
- MATLAB imwrite: https://www.mathworks.com/help/matlab/ref/imwrite.html

Bu kod temel hucre otomati fikrinin gereksinim tartismasi icin acik bir
oyuncak modelidir; Wolfram'in termodinamik simulasyonunun birebir kopyasi degildir.
