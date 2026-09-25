#!/usr/bin/env python3
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'app' / 'src' / 'main' / 'assets' / 'chinese_course'
AUTHORING = ROOT / 'authoring'
AUTHORING.mkdir(exist_ok=True)

scenes = [
(1,'搬家的最后几个箱子','Son Kutular','Nakliye ekibi erken gelir; kutular karışır ve aile son eşyaları düzenler.',['nesne göstermek','yer sormak','basit yerleştirme talimatı'],'ev eşyaları ve kutular','这是/那是, 在哪儿, 在这里/那里','zhè/nà karşıtlığı','LOC_ZH_OLD_HOME_001'),
(2,'火车票在哪儿？','Tren Biletleri Nerede?','Aile evden çıkmaya hazırlanırken Lele kendi tren biletini bulamaz.',['bir şeyin yerini sormak','sahiplik belirtmek','var/yok demek'],'bilet, çanta, aile eşyaları','有/没有, 我的/你的, 在哪儿','nǎr ve nàlǐ','LOC_ZH_OLD_HOME_001'),
(3,'站台在哪儿？','Peron Nerede?','İstasyonda yanlış yöne giderler ve görevliye doğru peronu sorarlar.',['yön sormak','teşekkür etmek','basit yön tarifini anlamak'],'istasyon ve yönler','请问…, 在哪儿, 左/右','qǐngwèn ve yön sözcükleri','LOC_ZH_OLD_STATION_001'),
(4,'火车上的早餐','Trende İlk Kahvaltı','Çocuklar trende yiyecek ister ve aile vagondaki satıcıdan alışveriş yapar.',['yiyecek istemek','adet söylemek','fiyat sormak'],'yiyecek, içecek, sayılar','我要…, 多少钱, 个/杯','yào, duōshao','LOC_ZH_TRAIN_001'),
(5,'丢失的玩具','Kayıp Oyuncak','Lele oyuncak trenini bulamaz; herkes koltukların çevresine bakar.',['kayıp eşya sormak','yer bildirmek','sahiplik belirtmek'],'oyuncaklar ve konum','谁的, 在…下面/旁边','shéi de, xiàmiàn','LOC_ZH_TRAIN_001'),
(6,'第一次看见新城','Yeni Kasabayı İlk Görüş','Tren yeni kasabaya yaklaşırken aile pencereden gördüklerini konuşur.',['bir yeri betimlemek','büyük/küçük demek','beğeni belirtmek'],'şehir yerleri ve sıfatlar','很…, 有…, 这是…','hěn ve temel ton akışı','LOC_ZH_TRAIN_001'),
(7,'车站的小麻烦','İstasyonda Karışıklık','Nakliye firmasından kimse görünmez; aile telefonla ne yapacağını anlamaya çalışır.',['telefonla basit bilgi vermek','beklemek/gelmek/gitmek','adres söylemek'],'telefon, adres, bekleme','来/去, 等, 现在','lái/qù','LOC_ZH_NEW_STATION_001'),
(8,'认识李晨','Li Chen ile Tanışma','Li Chen aileye yardım teklif eder; bu tanışma uzun bir dostluğun başlangıcı olur.',['kendini tanıtmak','isim sormak','nereli olduğunu söylemek'],'selamlaşma ve tanışma','我叫…, 你叫什么名字?, 你是哪儿人?','isimlerde tonlar','LOC_ZH_NEW_STATION_001'),
(9,'第一次坐出租车','İlk Taksi Yolculuğu','Taksi şoförü adresi yanlış anlar; Li Chen doğru yolu açıklamaya yardım eder.',['adres vermek','doğru/yanlış demek','durmasını istemek'],'taksi, sokak, numaralar','去…, 不是…, 对/不对','bù + 4. ton değişimi','LOC_ZH_TAXI_001'),
(10,'新家的门','Yeni Evin Kapısı','Anahtar ilk denemede kapıyı açmaz; doğru anahtarı bulurlar.',['ev eşyası adlandırmak','bu değil demek','aç/kapat talimatı vermek'],'ev, kapı, anahtar','不是这个, 是那个, 开/关','shì/bú shì','LOC_ZH_NEW_HOME_001'),
(11,'箱子放哪儿？','Kutular Nerede?','Mutfak kutuları yanlış odaya bırakılmıştır; aile kutuları yeniden düzenler.',['oda söylemek','nereye koyacağını belirtmek','yer sormak'],'odalar ve kutular','放在…, 哪个房间, 这里/那里','fángjiān','LOC_ZH_NEW_HOME_001'),
(12,'新家的第一个晚上','İlk Gece','İlk akşam yataklar hazırlanırken Mimi ortadan kaybolur.',['aramak','görmek/görmemek','evde konum belirtmek'],'ev, kedi, mobilya','看见/没看见, 在…吗','kànjiàn','LOC_ZH_NEW_HOME_001'),
(13,'咪咪在柜子旁边','Mimi Dolapta','Mimi mutfak dolabının yanında bulunur ve çocuklar rahatlar.',['konum söylemek','orada/burada demek','basit duyguyu ifade etmek'],'mobilya ve konum','在…旁边, 找到了','pángbiān','LOC_ZH_NEW_HOME_001'),
(14,'有人敲门','Kapı Çalıyor','Yeni komşu aileye hoş geldiniz demeye gelir.',['komşuyla tanışmak','aile bireylerini tanıtmak','teşekkür etmek'],'komşu ve aile','这是我…, 欢迎, 谢谢','huānyíng, xièxie','LOC_ZH_NEW_HOME_001'),
(15,'请邻居喝茶','Komşuya Çay','Liu Mei komşuya çay veya su ikram eder.',['içecek teklif etmek','istemek/istememek','sıcak/soğuk demek'],'içecekler','你喝…吗?, 我要…, 不要…','hē/chá/shuǐ','LOC_ZH_NEW_HOME_001'),
(16,'超市在哪儿？','Market Nerede?','Aile mahalledeki marketi bulmak için komşuya yol sorar.',['yer sormak','yakın/uzak demek','yön anlamak'],'mahalle ve market','离…远吗, 在哪儿, 往…走','yuǎn/jìn','LOC_ZH_NEIGHBORHOOD_001'),
(17,'第一次去超市','İlk Market Alışverişi','Lele sepete fazla atıştırmalık koyar; aile alışveriş listesini kontrol eder.',['ürün istemek','miktar söylemek','fiyat sormak'],'market ürünleri','我要这个, 几个, 多少钱','jǐ/ge','LOC_ZH_SUPERMARKET_001'),
(18,'钱够不够？','Kasada Para Yetiyor mu?','Kasada ödeme sırasında Zhang bozuk para ve toplam tutarı kontrol eder.',['fiyat anlamak','çok/az demek','ödemeyi tamamlamak'],'para ve sayılar','一共…, 太多/少, 给你','qián, gěi','LOC_ZH_SUPERMARKET_001'),
(19,'新家的早餐','Sabah Kahvaltısı','Aile yeni evde ilk sakin kahvaltısını yapar; herkes sevdiği yiyecekleri söyler.',['sevdiğini söylemek','yiyecek istemek','aile sohbeti yapmak'],'kahvaltı','我喜欢…, 我不喜欢…, 吃/喝','xǐhuan','LOC_ZH_NEW_HOME_001'),
(20,'全家福','Aile Fotoğrafı','Aile ilk fotoğrafını çekmeye çalışır; Mimi sürekli yer değiştirir.',['dur/gel/bak gibi komutları anlamak','aile üyelerini saymak'],'aile ve fotoğraf','来, 看这里, 坐/站','kàn, zhàn','LOC_ZH_NEW_HOME_001'),
(21,'新高中的校门','Yeni Lisenin Kapısı','Yutong yanlış binaya yönelir ve okul görevlisinden yardım ister.',['okulda yer sormak','hangi sınıf/bina demek'],'okul yerleri','哪个, 教室在哪儿, 我是学生','jiàoshì','LOC_ZH_HIGH_SCHOOL_001'),
(22,'新班级','Yeni Sınıf','Öğretmen Yutong’u sınıfa tanıtır; öğrenciler basit sorular sorar.',['yaş ve isim söylemek','kendini tanıtmak'],'sınıf ve tanışma','我叫…, 我今年…岁, 这是…','suì','LOC_ZH_HIGH_SCHOOL_001'),
(23,'第一个新朋友','İlk Yeni Arkadaş','Bir öğrenci Yutong’u öğle yemeğine davet eder.',['davete cevap vermek','birlikte gitmek','arkadaşlık kurmak'],'arkadaş ve öğle yemeği','一起…, 好啊, 我们去…','yìqǐ','LOC_ZH_HIGH_SCHOOL_001'),
(24,'乐乐的第一天','Lele’nin İlkokulu','Lele annesinden ayrılmak istemez; öğretmen onu rahatlatır.',['duygu söylemek','veda etmek','basit güvence vermek'],'okul ve duygular','别怕, 没事, 再见','bié pà','LOC_ZH_PRIMARY_SCHOOL_001'),
(25,'丢失的铅笔','Kaybolan Kalem','Lele mavi kaleminin başka bir öğrencide olduğunu sanır.',['renk söylemek','benim/senin demek','soru sormak'],'okul eşyaları ve renkler','这是你的吗?, 我的/你的, 蓝色','lán sè','LOC_ZH_PRIMARY_SCHOOL_001'),
(26,'张伟找工作','Zhang İş Arıyor','Zhang yerel ilanlara bakar ve Li Chen’den yardım ister.',['iş istediğini söylemek','telefon numarası paylaşmak'],'iş ve iletişim','我想找工作, 会…, 电话号码','gōngzuò','LOC_ZH_LICHEN_HOME_001'),
(27,'第一个工作电话','İlk Telefon Görüşmesi','Zhang bir iş yeriyle arama yapıp görüşme saati alır.',['telefonda kim olduğunu söylemek','zaman belirlemek'],'telefon ve zaman','喂, 我是…, 明天…点','wèi / wéi kullanım farkına giriş','LOC_ZH_NEW_HOME_001'),
(28,'面试前的准备','İş Görüşmesine Hazırlık','Liu Mei ve çocuklar Zhang için uygun gömlek seçer.',['kıyafet seçmek','renk ve beğeni söylemek'],'kıyafet ve renk','这个怎么样?, 我喜欢…, 穿…','chuān','LOC_ZH_NEW_HOME_001'),
(29,'工作面试','İş Görüşmesi','Zhang kendini ve temel becerilerini iş görüşmesinde tanıtır.',['meslek ve beceri söylemek','basit kişisel bilgi vermek'],'iş görüşmesi','我会…, 我以前…, 我想…','huì','LOC_ZH_WORKPLACE_001'),
(30,'好消息','Güzel Haber','Zhang işe kabul edilir; aile küçük bir kutlama yapar.',['iyi haber vermek','mutluluk ifade etmek','başlama tarihini söylemek'],'iş ve kutlama','太好了!, 我很高兴, 星期…开始','gāoxìng','LOC_ZH_NEW_HOME_001'),
(31,'上班第一天','İşe İlk Gün','Zhang iş yerine giriş kartını bulamayınca kısa süreli telaş yaşar.',['iş yerinde yardım istemek','eşya bulmak'],'iş yeri ve kimlik kartı','我的卡在哪儿?, 帮我一下','kǎ','LOC_ZH_WORKPLACE_001'),
(32,'新同事','Yeni İş Arkadaşları','Öğle arasında iş arkadaşları kendilerini tanıtır.',['meslek ve memleket sormak','tanışmayı sürdürmek'],'meslekler ve şehirler','你做什么工作?, 你从哪儿来?','tóngshì','LOC_ZH_WORKPLACE_001'),
(33,'午饭点什么？','Öğle Yemeği Siparişi','Zhang menüde ne seçeceğine karar veremez ve arkadaşından yardım ister.',['yemek sipariş etmek','öneri istemek'],'öğle yemeği ve menü','你吃什么?, 我要…, 这个好吃吗?','hǎochī','LOC_ZH_CANTEEN_001'),
(34,'错过公交车','Otobüsü Kaçırmak','Zhang eve dönüş otobüsünü kaçırır ve sonraki otobüsün saatini sorar.',['saat sormak','sonraki/şimdi demek'],'otobüs ve zaman','几点?, 下一班, 现在','xià yí bān','LOC_ZH_BUS_STOP_001'),
(35,'李晨一家来做客','Li Chen’in Ailesi Geliyor','İki aile ilk kez evde birlikte yemek yer ve yakınlaşır.',['misafir ağırlamak','yemek teklif etmek','aile tanıtmak'],'misafirlik ve sofra','请坐, 多吃一点, 这是…','qǐng zuò','LOC_ZH_NEW_HOME_001'),
(36,'孩子们一起玩','Çocuklar Birlikte Oynuyor','Çocuklar aynı oyuncakla oynamak ister ve küçük bir paylaşma sorunu çıkar.',['istemek','vermek/almak','paylaşmak'],'oyuncak ve çocuk konuşması','给我, 给你, 一起玩','gěi','LOC_ZH_NEW_HOME_001'),
(37,'公园里的星期天','Parkta Bir Pazar','Aile parkta yürür, oynar ve çevreyi keşfeder.',['hava hakkında konuşmak','aktivite söylemek'],'park, doğa, hava','天气很好, 我们走吧, 看…','tiānqì','LOC_ZH_PARK_001'),
(38,'掉在地上的冰淇淋','Dondurma Kazası','Lele’nin dondurması yere düşer; aile yenisini alıp onu neşelendirir.',['duygu ifade etmek','bir tane daha istemek','tat söylemek'],'dondurma, tatlar, duygular','别难过, 再来一个, 我喜欢…味','nánguò','LOC_ZH_PARK_001'),
(39,'突然下雨了','Yağmur Başlıyor','Park dönüşünde yağmur başlar ve şemsiyelerin evde kaldığını fark ederler.',['hava durumu söylemek','hızlı gitmeyi önermek'],'yağmur ve kıyafet','下雨了, 快走, 没带…','xiàyǔ','LOC_ZH_NEIGHBORHOOD_001'),
(40,'邻居的包裹','Komşunun Paketi','Kurye komşunun paketini yanlışlıkla Zhang ailesine bırakır.',['isim/adres kontrol etmek','bu sizin mi diye sormak'],'paket ve adres','这是你的吗?, 地址, 不是我们的','dìzhǐ','LOC_ZH_NEW_HOME_001'),
(41,'咪咪去看兽医','Mimi Veterinerde','Mimi yemek yemeyince aile onu veterinere götürür.',['basit sağlık durumu söylemek','yiyor/yemiyor demek'],'hayvan ve sağlık','它不吃饭, 怎么了?, 医生','yīshēng','LOC_ZH_VET_001'),
(42,'在宠物店买东西','Eczane/Pet Ürünü Alışverişi','Aile veterinerin önerdiği ürünü pet mağazasında arar.',['ürün sormak','var mı demek','bir tane istemek'],'pet ürünleri ve alışveriş','有这个吗?, 我要一个, 多少钱','yǒu…ma','LOC_ZH_PET_SHOP_001'),
(43,'雨桐的第一次考试','Yutong’un İlk Sınavı','Yutong sınavdan önce heyecanlıdır; aile onu destekler.',['ders ve sınav hakkında konuşmak','kolay/zor demek'],'dersler ve sınav','考试, 学习, 容易/难','kǎoshì','LOC_ZH_NEW_HOME_001'),
(44,'乐乐的全家福','Lele’nin Resmi','Lele okulda çizdiği aile resmini sınıfa anlatır.',['aile bireylerini tanıtmak','yaş/isim söylemek'],'aile ve çizim','这是我妈妈, 他/她叫…, …岁','tā sesleri','LOC_ZH_PRIMARY_SCHOOL_001'),
(45,'第一个发薪日','Zhang’ın Maaş Günü','Zhang ilk maaşını alınca aile küçük bir akşam yemeği planlar.',['para ve plan konuşmak','bugün/akşam demek'],'maaş, yemek, plan','今天晚上…, 我们去…, 钱','wǎnshang','LOC_ZH_WORKPLACE_001'),
(46,'刘梅的蛋糕','Liu Mei’nin Kekleri','Liu Mei komşular için kek yapar; herkes çok beğenir.',['tat ve beğeni belirtmek','yapabildiğini söylemek'],'tatlılar ve beceri','很好吃, 你会做吗?, 我会','dàngāo','LOC_ZH_NEW_HOME_001'),
(47,'一个小小的想法','Küçük Bir Fikir','Li Chen’in eşi Liu Mei’nin yiyecek satabileceğini söyler; ilk iş fikri doğar.',['beceri hakkında konuşmak','basit gelecek fikri söylemek'],'beceri ve iş fikri','你可以…, 以后, 做得很好','kěyǐ','LOC_ZH_NEW_HOME_001'),
(48,'社区活动','Mahalle Etkinliği','Aile yerel bir topluluk etkinliğine katılıp yeni insanlarla tanışır.',['yeni insanla tanışmak','birlikte etkinlik yapmak'],'topluluk ve etkinlik','我们一起…, 认识, 朋友','rènshi','LOC_ZH_COMMUNITY_CENTER_001'),
(49,'来新城三个月了','Kasabada Üç Ay','Aile eski yaşamla yeni kasabadaki ilk üç ayı basit şekilde karşılaştırır.',['eski/yeni demek','beğeni belirtmek','basit karşılaştırma'],'şehir yaşamı ve zaman','新/旧, 更…, 我喜欢这里','gèng','LOC_ZH_NEW_HOME_001'),
(50,'这里是我们的家','Artık Evimiz Burası','Aile ve Li Chen’ler birlikte yemek yer; herkes yeni kasabada sevdiği bir şeyi söyler.',['sevdiğini anlatmak','aile/arkadaş/okul/iş kelimelerini bütünlemek'],'HSK1 genel tekrar','我喜欢…, 这是我们的…, 我们在这里…','ritim ve temel ton tekrarı','LOC_ZH_NEW_HOME_001'),
]

blueprints=[]
for n,zh,tr,adv,goals,vocab,grammar,pron,loc in scenes:
    sid=f'ZH_HSK1_SC{n:03d}'
    blueprints.append({
        'schemaVersion':2,'id':sid,'level':'HSK1','number':n,
        'titleZh':zh,'titleTr':tr,'productionStatus':'blueprint_ready','complete':False,
        'miniAdventureTr':adv,'learning':{
            'communicationGoals':goals,'vocabularyTheme':vocab,'grammarTheme':grammar,
            'pronunciationTheme':pron,'targetActiveVocabularyCount': {'min':3,'max':6},
            'defaultSpeechSpeed':0.8,'defaultSubtitleMode':'ZH_PINYIN_TR'
        },
        'locationId':loc,
        'story':{'previousSceneId': None if n==1 else f'ZH_HSK1_SC{n-1:03d}',
                 'nextSceneId': 'ZH_HSK2_SC001' if n==50 else f'ZH_HSK1_SC{n+1:03d}'},
        'dialogues':[]
    })

(AUTHORING/'hsk1_blueprints.json').write_text(json.dumps({'schemaVersion':2,'level':'HSK1','sceneCount':50,'scenes':blueprints},ensure_ascii=False,indent=2),encoding='utf-8')

# locations registry
locations = [
('LOC_ZH_OLD_HOME_001','旧家','Eski ev'),('LOC_ZH_OLD_STATION_001','旧城火车站','Eski şehir istasyonu'),
('LOC_ZH_TRAIN_001','火车','Tren'),('LOC_ZH_NEW_STATION_001','新城火车站','Yeni kasaba istasyonu'),
('LOC_ZH_TAXI_001','出租车','Taksi'),('LOC_ZH_NEW_HOME_001','新家','Yeni ev'),
('LOC_ZH_NEIGHBORHOOD_001','新社区','Yeni mahalle'),('LOC_ZH_SUPERMARKET_001','社区超市','Mahalle marketi'),
('LOC_ZH_HIGH_SCHOOL_001','新城高中','Lise'),('LOC_ZH_PRIMARY_SCHOOL_001','新城小学','İlkokul'),
('LOC_ZH_LICHEN_HOME_001','李晨家','Li Chen’in evi'),('LOC_ZH_WORKPLACE_001','张伟的工作单位','Zhang’ın iş yeri'),
('LOC_ZH_CANTEEN_001','公司食堂','İş yeri yemekhanesi'),('LOC_ZH_BUS_STOP_001','公交车站','Otobüs durağı'),
('LOC_ZH_PARK_001','社区公园','Park'),('LOC_ZH_VET_001','宠物医院','Veteriner kliniği'),
('LOC_ZH_PET_SHOP_001','宠物用品店','Pet mağazası'),('LOC_ZH_COMMUNITY_CENTER_001','社区活动中心','Topluluk merkezi')]
(CONTENT/'locations.json').write_text(json.dumps({'schemaVersion':1,'locations':[{'id':i,'nameZh':z,'nameTr':t} for i,z,t in locations]},ensure_ascii=False,indent=2),encoding='utf-8')

# write scene files and index; preserve existing dialogues for SC001 as draft only
level_dir=CONTENT/'levels'/'HSK1'
index=[]
for bp in blueprints:
    p=level_dir/'scenes'/f"{bp['id']}.json"
    old={}
    if p.exists():
        try: old=json.loads(p.read_text(encoding='utf-8'))
        except: pass
    if bp['number']==1 and old.get('dialogues'):
        bp['dialogues']=old['dialogues']
        bp['productionStatus']='dialogue_draft'
        bp['draftDialogueCount']=len(old['dialogues'])
    p.write_text(json.dumps(bp,ensure_ascii=False,indent=2),encoding='utf-8')
    index.append({k:bp[k] for k in ['id','number','titleZh','titleTr','complete','productionStatus']})
(level_dir/'index.json').write_text(json.dumps({'level':'HSK1','storyArc':'Yeni kasabaya taşınma ve ilk aylar','blueprintReadyScenes':50,'completeScenes':0,'scenes':index},ensure_ascii=False,indent=2),encoding='utf-8')

manifest=json.loads((CONTENT/'manifest.json').read_text(encoding='utf-8'))
for lv in manifest['levels']:
    if lv['id']=='HSK1':
        lv['completeScenes']=0
        lv['blueprintReadyScenes']=50
    else:
        lv.setdefault('blueprintReadyScenes',0)
(CONTENT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')

status={
 'schemaVersion':1,
 'course':'CHINESE_HSK_LIFE_JOURNEY_001',
 'totalLevels':6,'totalSceneSlots':300,
 'blueprintReadyScenes':50,'completeScenes':0,
 'dialogueDraftScenes':1,
 'nextProductionTarget':'Complete full dialogue/learning/production data for HSK1 SC001-SC050',
 'noteTr':'HSK1 50 sahnenin gerçek sahne haritası/blueprint verisi hazır. Tam sahne sayılması için 90-110 doğal diyalog ve öğrenme modülleri tamamlanmalıdır.'
}
(CONTENT/'content_status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2),encoding='utf-8')
print('HSK1 blueprints upgraded:',len(blueprints))
