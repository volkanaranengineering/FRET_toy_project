# Üçüncü revizyon: kapsamı daraltılmış araştırma notu

Ana çıktı `paper.pdf`; düzenlenebilir kaynak `paper.tex`. Yazar atfı: ChatGPT; yönlendiren Volkan Aran. `REVIZYON_YANITI.md` değişiklik gerekçelerini ve kalan sınırları açıklar.

## Yeniden üretim

Python 3.10+ standart kitaplığı yeterlidir. Paket kökünden:

```
python artifact/experiments.py
python artifact/http_case.py
python artifact/trajectory.py
python artifact/validate_bundle.py
```

HTTP deneyi yalnızca 127.0.0.1 üzerinde geçici yerel port kullanır; dış siteye istek göndermez. Dört çeşit araştırma için oluşturulmuş sunuculardır. Yerel bağlantıya izin veren çalışma ortamı gerekir.

MATLAB R2018b ile test edildi:

```
addpath('artifact');
verify_matlab;
```

MATLAB temel kayıtları kendi durum ve entropi fonksiyonlarıyla yeniden hesaplar, makale grafiğini üretir. Beklenen değerleri kopyalamaz. Şekil `.png` ve düzenlenebilir `.fig` olarak `assets` altına yazılır. HTTP deneyini MATLAB yürütmez.

XeLaTeX ve Times New Roman gerekir; iki kez çalıştırın:

```
xelatex -interaction=nonstopmode -halt-on-error paper.tex
```

## Kod / veri

- `artifact/model.py`: yeni sınıf, destek ve kabul sözleşmesi.
- `artifact/experiments.py`: 2.480 temel kayıt, 7.440 dönüşüm kontrolü, 52 sınır, 41 geçersiz kayıt.
- `artifact/fixtures.json`: MATLAB'a verilen 2.573 temel kontrol girdisi ve Python çıktısı.
- `artifact/finite_cases.csv`, `boundary_cases.csv`, `invalid_cases.csv`: ham kontrol sonuçları.
- `artifact/summary.json`, `matlab_validation.json`: özetler.
- `artifact/http_case.py`: RFC 9110 Bölüm 8.6 ve 9.3.2'den türetilmiş iki koşulun çalıştırılan örneği.
- `artifact/http_raw.json`: 40 gerçek yerel yanıtın base64 baytları ve SHA-256 özetleri.
- `artifact/http_pairs.csv`: 20 GET/HEAD çiftinden ölçülen değerler.
- `artifact/http_records.json`: ölçümlerden türetilen kanıt kayıtları ve kabul durumları.
- `artifact/trajectory.csv`: altı olaylık proje kaydı; insan deneyi veya zaman ölçümü değildir.
- `artifact/validate_bundle.py`: ham yanıt/ölçüt/özet ve dosya tutarlılığı denetimi.

## Sınır

Entropi, bu kayıttaki aday ağırlıklarını ölçer. Gerçek dünyadaki toplam belirsizliğin, başarının veya kanıt güvenilirliğinin ölçüsü değildir. Sınıf eşlemesi ve kapsam dışarıdan verilir. Kodun kabulü yalnızca bu kapsam ve kayıtlara göredir. Tamsayı toplamı 1 ile 2^52 arasındadır. Kaynak ve değerlendirici bilgileri beyan niteliğindedir; kimlik doğrulaması yapılmaz.

Önceki V2 klasörü değiştirilmedi. V3, eski hücresel otomat çizicisinin yeni sürümü değil, daha dar araştırma sorusu için yeni uygulamadır. Yeni sonucun açıklaması makalededir; eski büyük koşu sayıları başarı iddiasına eklenmemiştir.
