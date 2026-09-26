from pathlib import Path
import json, html
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.graphics.shapes import Drawing, Rect, Line, String, Circle

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
OUT=HERE/'NASA_FRET_Turkce_Tutorial.pdf'
OUT.parent.mkdir(parents=True,exist_ok=True)
for name,file in [('Arial','arial.ttf'),('ArialB','arialbd.ttf'),('ArialI','ariali.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(Path('C:/Windows/Fonts')/file)))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='ArialB',italic='ArialI',boldItalic='ArialB')
NAVY=colors.HexColor('#12253C'); TEAL=colors.HexColor('#087F8C'); GRAY=colors.HexColor('#526273'); LIGHT=colors.HexColor('#EDF4F8')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyTR',fontName='Arial',fontSize=10.2,leading=15,spaceAfter=9,textColor=NAVY))
styles.add(ParagraphStyle(name='SmallTR',fontName='Arial',fontSize=8.4,leading=11.5,spaceAfter=6,textColor=GRAY))
styles.add(ParagraphStyle(name='TitleTR',fontName='ArialB',fontSize=28,leading=33,spaceAfter=16,textColor=NAVY))
styles.add(ParagraphStyle(name='HeadTR',fontName='ArialB',fontSize=19,leading=24,spaceAfter=15,textColor=NAVY))
styles.add(ParagraphStyle(name='SubTR',fontName='ArialB',fontSize=12,leading=16,spaceBefore=8,spaceAfter=7,textColor=TEAL))
styles.add(ParagraphStyle(name='CodeTR',fontName='Arial',fontSize=10,leading=15,backColor=LIGHT,borderPadding=10,spaceBefore=8,spaceAfter=15,textColor=NAVY))
story=[]
def p(s,style='BodyTR'): story.append(Paragraph(s,styles[style]))
def title(n,t):
    p(f'NASA FRET / UYGULAMALI TÜRKÇE REHBER / {n:02d}','SmallTR'); p(t,'HeadTR')
def page(): story.append(PageBreak())
def code(s): p(html.escape(s).replace('\n','<br/>'),'CodeTR')
def table(rows,widths):
    cells=[[Paragraph(str(x),styles['SmallTR'] if i else ParagraphStyle('th',parent=styles['SmallTR'],fontName='ArialB',textColor=colors.white)) for x in r] for i,r in enumerate(rows)]
    t=Table(cells,colWidths=widths,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,LIGHT]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,-1),(-1,-1),0.5,colors.HexColor('#CCD8DF'))]))
    story.append(t); story.append(Spacer(1,12))
def shot(name,caption,maxh=275):
    path=HERE/name
    if not path.exists(): raise FileNotFoundError(path)
    w,h=ImageReader(str(path)).getSize(); scale=min(499/w,maxh/h)
    story.append(Image(str(path),width=w*scale,height=h*scale,hAlign='CENTER'))
    story.append(Spacer(1,7)); p(caption,'SmallTR')
def trace(label,request,response,color=TEAL):
    n=len(request); d=Drawing(495,103); x0=88; dx=36
    d.add(String(0,91,label,fontName='ArialB',fontSize=10,fillColor=NAVY))
    for k in range(n):
        x=x0+k*dx; d.add(Line(x,9,x,75,strokeColor=colors.HexColor('#DDE5EB'))); d.add(String(x-3,0,str(k),fontName='Arial',fontSize=8,fillColor=GRAY))
    for idx,(name,values) in enumerate([('request',request),('response',response)]):
        low=53-idx*32; high=low+15
        d.add(String(0,low+5,name,fontName='Arial',fontSize=9,fillColor=NAVY))
        for k,v in enumerate(values):
            x=x0+k*dx; y=high if v else low
            if k<n-1:
                d.add(Line(x,y,x+dx,y,strokeWidth=1.8,strokeColor=color))
                yn=high if values[k+1] else low
                d.add(Line(x+dx,y,x+dx,yn,strokeWidth=1.8,strokeColor=color))
            d.add(Circle(x,y,2.5,fillColor=color,strokeColor=color))
    return d

p('NASA FRET 3.0  |  WINDOWS YEREL KURULUM','SmallTR')
p('Bir gereksinimin<br/>anlamını görünür kılmak','TitleTR')
p('Kurulum, FRETish, anlam diyagramı ve iki farklı yorumun karşılaştırılması','SubTR')
p('Bu rehber, tek bir gereksinimin belirsiz doğal dilden FRET’in işleyebildiği bir ifadeye nasıl dönüştürüldüğünü gösterir. Örnek, indirilen NASA FRET kaynak kodunun kendi ayrıştırıcısı ve anlambilim üreticisiyle işlenmiştir.')
code('when request the ResponseSystem\nshall within 3 ticks satisfy response')
p('<b>Öğreneceğiniz sonuç:</b> Talep ne zaman yükümlülük başlatır, yanıt ne zamana kadar gelmelidir ve bir kelime değişince davranış nasıl değişir?')
table([['Bu pakette','Durum'],['FRET masaüstü arayüzü ve yerel veri tabanı','Windows üzerinde yerel derleme; arayüz doğrulaması aşağıdaki ekranlarda.'],['FRETish ayrıştırma ve formül üretimi','REQ-001 ve REQ-002 gerçek FRET derleyicisinden geçirildi.'],['Örnek proje','NASA-FRET/tutorial/FRET_Tutorial_TR.json'],['LTLSIM ve realizability','Harici analiz araçları kurulmadı. Bu rehberdeki iz çizimleri açıklayıcıdır; LTLSIM çalıştırma sonucu değildir.']],[165,334])
p('Hızlı başlangıç','SubTR')
p('1. Çalışma klasöründeki <b>NASA-FRET/FRET-Baslat.cmd</b> dosyasına çift tıklayın.<br/>2. <b>Requirements</b> listesinde <b>REQ-001</b> kimliğine tıklayın.<br/>3. Açılan özette kalem simgesine basın; düzenleyicide <b>SEMANTICS</b> düğmesini seçin.')
p('Hazırlanma: 25 Eylül 2026. Kaynak: NASA-SW-VnV/fret, master arşivi, paket sürümü 3.0. Bu belge NASA’nın resmî eğitimi değildir; indirilen sürüm üzerinde hazırlanmış Türkçe uygulama rehberidir.','SmallTR')
page()

title(2,'Önce anlamı belirleyin')
p('Başlangıç cümlesi: <b>“Kullanıcı talep gönderdiğinde sistem kısa sürede yanıt vermelidir.”</b> FRET’in görevi, “kısa” sözcüğüne kendi başına bir süre atamak değildir. Aşağıdaki kararları analist verir ve kayıt altına alır.')
table([['Açık konu','Bu eğitimde verilen karar'],['Talep nedir?','request: Boolean giriş. FALSE değerinden TRUE değerine geçiş, yeni talep olayıdır. Başlangıçta TRUE olması da tetikler.'],['Yanıt nedir?','response: Boolean çıkış. Talebin alındı bildirimi değil, işlemin sonucunun hazır olmasıdır.'],['Kısa süre ne demek?','En fazla 3 zaman adımı; tetikleme anı da kabul edilir. Bu sayı eğitim varsayımıdır.'],['Hangi kapsam?','Tüm yürütme. Belirli bir çalışma modu kısıtı yoktur.'],['Birden fazla talep?','Bu basit örnek talep kimliklerini eşlemez. Eşzamanlı çoklu talepler için ek modelleme gerekir.']],[140,359])
p('FRETish alanlarına karşılığı','SubTR')
table([['Alan','Örnekteki ifade','Anlam'],['Scope','Yazılmadı','Tüm yürütme'],['Condition','when request','Başlangıçta TRUE / yükselen kenar'],['Component','the ResponseSystem','Sorumlu sistem bileşeni'],['Modal','shall','Zorunluluk'],['Timing','within 3 ticks','0, 1, 2 veya 3 adım uzaklıkta'],['Response','satisfy response','response doğru olmalı']],[85,173,241])
p('<b>Zaman birimi:</b> Bu sürümde FRET, seconds / milliseconds / ticks birimlerini fiziksel zamana dönüştürmez. 1 tick = 100 ms isteniyorsa, bu eşleme model ve doğrulama ortamında ayrıca kurulmalıdır. [3]','SmallTR')
page()

title(3,'Örneği açın ve düzenleyin')
p('Hazır örneği içe aktarmak için sol araç çubuğundaki <b>aşağı ok / Import</b> simgesini kullanın. <b>NASA-FRET/tutorial/FRET_Tutorial_TR.json</b> dosyasını seçin; Windows dosya penceresinde <b>Aç</b> düğmesine basın. Proje otomatik yüklenir. Proje zaten yüklüyse tekrar içe aktarmanız gerekmez.')
shot('01-project.png','Şekil 1. Bu bilgisayarda çalışan FRET ve eğitim projesi. Ekrandaki yeşil durum, gereksinimin biçimselleştirildiğini gösterir; uygulamanın doğru çalıştığının kanıtı değildir.',270)
p('Aynı gereksinimi sıfırdan yazmak için','SubTR')
p('1. Projects menüsünden ayrı bir deneme projesi oluşturun.<br/>2. <b>CREATE</b> ile yeni gereksinim açın.<br/>3. Requirement ID alanına <b>REQ-001</b> yazın.<br/>4. Aşağıdaki cümleyi metin alanına girin.<br/>5. Rationale alanına “Yanıt = işlem sonucu; sınır = 3 tick” kararını kaydedin.<br/>6. Ayrıştırma hatası olmadığını kontrol edin; <b>SEMANTICS</b> ile anlamı görün ve kaydedin.')
code('when request the ResponseSystem shall within 3 ticks satisfy response')
p('İfadeyi çift tırnak içine almayın. FRET’te tamamen tırnaklanmış metin, biçimselleştirilmeden saklanabilir. İngilizce anahtar sözcükler ve basit değişken adları kullanın; Türkçe açıklamayı gerekçe alanına yazabilirsiniz. [2]','SmallTR')
page()

title(4,'SEMANTICS ekranını okuyun')
shot('02-semantics.png','Şekil 2. REQ-001 için gerçek FRET anlam görünümü. Alan renkleri, sözel açıklama ve zaman ilişkisi aynı gereksinime aittir.',285)
p('Üç soruya yanıt arayın','SubTR')
p('<b>SCOPE:</b> Hangi yürütme aralığı geçerli? Burada tüm yürütme.<br/><b>TRIGGER:</b> Yükümlülük ne zaman başlar? request ilk noktada doğruysa veya sonradan FALSE → TRUE geçerse.<br/><b>REQUIRED BEHAVIOR:</b> Her tetiklemeden itibaren response, en geç üçüncü adımda en az bir kez doğru olmalıdır.')
p('<b>Diyagram:</b> Gri alan kapsamı, açık mavi şerit koşulun doğru kaldığı bir aralığı, turuncu şerit yanıtın en az bir kez gerçekleşmesi gereken pencereyi gösterir. TC tetikleme anıdır; n = 3. Ayrıntılar için Diagram Semantics bölümünü açın.','SmallTR')
p('FRET’in ürettiği sonsuz iz formülü','SubTR')
sem=json.loads((HERE/'verified-semantics.json').read_text(encoding='utf-8'))
code(sem[0]['formula'].replace(' & (request','\n& (request'))
p('<b>G:</b> her zaman; <b>X:</b> sonraki adım; <b>F[0,3]:</b> şu andan başlayarak üç adım içinde en az bir kez. Formülün ilk bölümü yükselen kenarları, ikinci bölümü yürütmenin ilk noktasında request doğru olmasını kapsar.','SmallTR')
p('Ekranın sözel açıklamasında sonlu aralığın erken bitmesine ilişkin ek cümle bulunur. Sonsuz iz formülünde LAST yoktur; sonlu iz formülünde vardır. Bu ayrımı 6. sayfadaki deneyle okuyun.','SmallTR')
page()

title(5,'Resmi davranışa çevirin')
p('Aşağıdaki çizimler FRET’in ürettiği anlamı açıklamak için hazırlanmıştır. Gerçek LTLSIM çıktısı değildir. request, t=1 anında tetikleniyor; bu nedenle izin verilen yanıt noktaları t=1, 2, 3 ve 4’tür.')
story.append(trace('A / Sınırda yanıt: gereksinim sağlanır',[0,1,0,0,0,0,0,0,0,0],[0,0,0,0,1,0,0,0,0,0]))
story.append(Spacer(1,15))
story.append(trace('B / Geç yanıt: gereksinim ihlal edilir',[0,1,0,0,0,0,0,0,0,0],[0,0,0,0,0,1,0,0,0,0],colors.HexColor('#C04638')))
story.append(Spacer(1,15))
table([['Deneme','Beklenen yorum'],['Yanıt t=1','Geçerli. “within” sıfır gecikmeyi de kabul eder.'],['Yanıt t=4','Geçerli. Tetiklemeden tam 3 adım sonra.'],['İlk yanıt t=5','İhlal. Tam gözlenen [1,4] penceresinde yanıt yok.'],['request hiç TRUE değil','Yükümlülük tetiklenmez. Bu, sistemin talep işlediğini kanıtlamaz.'],['response sürekli TRUE','Bu gereksinim sağlanabilir. “Yeni yanıt üretme” veya “yanıttan sonra sıfırlama” davranışı ayrıca istenmelidir.']],[150,349])
p('Bir sonraki gereksinim sorusu','SubTR')
p('“Yanıtın yalnızca doğru olması yeterli mi, yoksa her talep için yeni bir yanıt olayı mı gerekli?” Bu farkı görsel ortaya çıkarır. İkinci anlam isteniyorsa talep/yanıt kimliği, sayaç veya protokol durumu eklemek gerekebilir.')
page()

title(6,'Bir kelime değişince ne olur?')
code('whenever request the ResponseSystem shall within 3 ticks satisfy response')
p('<b>REQ-002</b>, REQ-001’in karşılaştırma alternatifidir. İkisini birlikte zorunlu gereksinimler olarak kabul etmek yerine ayrı ayrı yorumlayın. “whenever”, request doğru kaldığı her noktada yeni bir yanıt penceresi başlatır.')
story.append(trace('Aynı iz / request yüksek kalıyor, tek yanıt t=3',[0,1,1,1,1,1,1,1,1,1],[0,0,0,1,0,0,0,0,0,0]))
story.append(Spacer(1,14))
table([['İfade','Aynı izde sonuç'],['when / REQ-001','Yalnızca t=1 tetiklemesi vardır; t=3 yanıtı yeterlidir.'],['whenever / REQ-002','Örneğin t=4 yeni bir pencere açar. [4,7] içinde yanıt yoktur; ihlal oluşur.']],[150,349])
p('REQ-002 için FRET’in ürettiği formül','SubTR')
code(sem[1]['formula'])
p('Kısa kayıt tuzağı','SubTR')
p('request t=1’de doğru olsun; response hiç doğru olmasın. Kayıt t=3’te biterse son tarih olan t=4 henüz görülmemiştir. Bu örneğin FRET sonlu iz anlambilimi, aralık erken bittiğinde yanıtın gerçekleşmesini zorunlu tutmaz. Dolayısıyla kısa izde olumlu değerlendirme, gerçek yanıtın alındığı anlamına gelmez.')
p('<b>Deney kararı:</b> Her tetikleme için en az t+3 noktasını içeren kayıt alın. Kayıt erken bitmişse analiz raporunda “gözlem penceresi tamamlanmadı” durumunu ayrıca gösterin. Bu ifade önerilen raporlama kararıdır; FRET’in yeni bir sonuç kategorisi değildir.')
page()

title(7,'Kendi gereksiniminize uygulayın')
table([['Adım','Yapılacak iş','Elde edilen kanıt'],['1. Ayır','Aktör, olay, tepki, kapsam ve süreyi ayır.','Metin → FRETish alan eşlemesi'],['2. Kararı kaydet','Belirsiz sözcükler için karar ver; gerekçesini yaz.','Varsayım ve paydaş kararı'],['3. Biçimselleştir','FRETish gir; ayrıştırmayı ve SEMANTICS açıklamasını kontrol et.','Formül ve anlam diyagramı'],['4. Ayırıcı iz kur','Bir yorumda geçen, diğerinde kalan davranış bul.','Somut yorum farkı'],['5. Sonraki soruyu seç','Davranışı değiştiren açık kararı sor.','Yeni bilgi / revizyon'],['6. Dışa aktar','Proje ve varsa değişken eşlemesini JSON olarak sakla.','Tekrar yüklenebilir proje']],[77,224,198])
p('Wolfram tarzı görselleştirmeye bağlantı','SubTR')
p('FRET’te resim, tanımlanmış anlamın bir gösterimidir. Projenizde de her hücre veya düğümü bir anlam alanına bağlayabilirsiniz. Örneğin “tetikleyici açık”, “süre kararlaştırıldı”, “test penceresi tamamlanmadı” farklı durumlardır. Hücrenin renk değiştirmesi, bir paydaş yanıtı veya kanıtla açıklanmalıdır.')
p('İsteğe bağlı gelişmiş analiz','SubTR')
p('<b>LTLSIM:</b> NuSMV ve LTLSIM yerel simülatör bileşeni gerekir. Kurulduğunda SEMANTICS sonrasında SIMULATE açılır; Boolean izlerde noktaya tıklayarak değerler değiştirilir. Bu kurulumda bu arka uç kurulmadı. [4]')
p('<b>Realizability:</b> Gereksinim kümesinin uygulanabilirliğini analiz eder; uygun çözümleyici ve giriş/çıkış değişken tanımları gerekir. Bir formülün üretilebilmesi, gereksinimlerin birlikte gerçekleştirilebilir olduğu anlamına gelmez. NASA’nın FSM örneği sonraki çalışma için uygundur. [5]')
p('<b>Şimdi sorulacak soru:</b> Sizin sisteminizde açık kalan en kritik ayrım “ne zaman tetiklenir”, “hangi tepki istenir” veya “nasıl ölçülür” seçeneklerinden hangisi? İlk görseli bu ayrımı görünür kılacak şekilde seçin.')
page()

title(8,'Kurulum kaydı ve kaynaklar')
p('Bu bilgisayardaki kurulum','SubTR')
p('NASA deposunun master ZIP arşivi indirildi. Paket sürümü <b>3.0</b>. Node.js <b>20.19.0</b>, yalnızca NASA-FRET/runtime altında tutuldu. Ana npm bağımlılıkları kilit dosyasından kuruldu; masaüstü ve CLI bileşenleri derlendi. NASA’nın önerdiği Windows yolu WSL2’dir; burada WSL olmadığı için yerel Windows derlemesi kullanıldı.')
p('Kurulum sırasında Unix temizleme komutlarını ve isteğe bağlı yerel simülatör derlemesini çalıştırmamak için npm yaşam döngüsü betikleri otomatik başlatılmadı. Electron kurulumu ve FRET derlemesi ayrı çalıştırıldı. Bu nedenle bu paket, tüm harici analiz araçları kurulmuş bir WSL ortamıyla eşdeğer değildir.')
table([['Dosya / klasör','Görevi'],['NASA-FRET/FRET-Baslat.cmd','Çift tıklayarak masaüstü uygulamasını açar.'],['NASA-FRET/fret-master','NASA kaynak kodu ve derlenmiş FRET.'],['NASA-FRET/runtime','Uygulamaya ayrılmış Node.js.'],['NASA-FRET/data','Gereksinim, model ve uygulama profil verileri.'],['NASA-FRET/tutorial/FRET_Tutorial_TR.json','İçe aktarılabilir, iki gereksinimli eğitim projesi.'],['NASA-FRET/tutorial/verified-semantics.json','Gerçek FRET derleyicisinden alınan metin, formül ve diyagram yolları.'],['tmp/fret-install','İndirme, bağımlılık ve derleme günlükleri.']],[245,254])
p('Kaynaklar / erişim: 25 Eylül 2026','SubTR')
base='https://github.com/NASA-SW-VnV/fret'
sources=[('1. NASA FRET deposu ve kurulum',base),('2. Gereksinim yazımı',base+'/blob/master/fret-electron/docs/_media/user-interface/writingReqs.md'),('3. Zaman alanı ve birim uyarısı',base+'/blob/master/fret-electron/docs/_media/user-interface/examples/timing.md'),('4. LTLSIM kullanımı',base+'/blob/master/fret-electron/docs/_media/UsingTheSimulator/ltlsim.md'),('5. NASA sonlu durum makinesi örneği',base+'/blob/master/caseStudies/FiniteStateMachine/fsm_instructions.md'),('6. Windows / WSL kurulum yolu',base+'/blob/master/fret-electron/docs/_media/installingFRET/installation_windows.md'),('7. when / whenever ayrımı',base+'/blob/master/fret-electron/docs/_media/user-interface/examples/condition.md')]
for label,url in sources: p(f'<link href="{url}" color="#087F8C">{label}</link>','SmallTR')
p('Ekran görüntüleri: bu bilgisayardaki FRET çalıştırması. Davranış çizimleri ve Türkçe açıklamalar: bu rehber için üretildi. FRET kaynak lisansı: Apache 2.0. Kaynak arşivinin SHA-256 özeti kurulum kayıt dosyasında tutulur.','SmallTR')

def footer(c,doc):
    c.setStrokeColor(colors.HexColor('#D6E0E7')); c.line(48,43,547,43)
    c.setFont('Arial',8); c.setFillColor(GRAY); c.drawString(48,29,'NASA FRET 3.0 | Türkçe uygulama rehberi')
    c.drawRightString(547,29,str(doc.page))
doc=SimpleDocTemplate(str(OUT),pagesize=(595.28,841.89),rightMargin=48,leftMargin=48,topMargin=43,bottomMargin=57,title='NASA FRET - Türkçe Uygulamalı Tutorial',author='Codex')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
