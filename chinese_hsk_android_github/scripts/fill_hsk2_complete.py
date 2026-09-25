#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the complete HSK2 authoring payload for all 50 scenes.

This is deterministic, offline, and writes back to authoring/hsk2_blueprints.json.
The payload is data-complete for the app while retaining a native/editorial review flag.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'authoring' / 'hsk2_blueprints.json'

# Simplified Chinese, tone-marked Hanyu Pinyin, Turkish meaning.
W = {
'routine':('日常','rìcháng','günlük rutin'),'morning':('早上','zǎoshang','sabah'),'bathroom':('洗手间','xǐshǒujiān','banyo / tuvalet'),'first':('先','xiān','önce'),'then':('再','zài','sonra'),
'buscard':('公交卡','gōngjiāo kǎ','otobüs kartı'),'month':('一个月','yí ge yuè','bir ay'),'day':('一天','yì tiān','bir gün'),'ticketoffice':('服务台','fúwùtái','hizmet bankosu'),
'vegetable':('蔬菜','shūcài','sebze'),'fruit':('水果','shuǐguǒ','meyve'),'jin':('斤','jīn','yarım kilo ölçüsü'),'price':('价格','jiàgé','fiyat'),'fresh':('新鲜','xīnxiān','taze'),
'late':('迟到','chídào','geç kalmak'),'schoolbus':('校车','xiàochē','okul servisi'),'wait':('等','děng','beklemek'),'neighbor':('邻居','línjū','komşu'),'hurry':('来不及','láibují','yetişememek'),
'club':('社团','shètuán','kulüp'),'sport':('运动','yùndòng','spor'),'music':('音乐','yīnyuè','müzik'),'because':('因为','yīnwèi','çünkü'),'therefore':('所以','suǒyǐ','bu yüzden'),
'overtime':('加班','jiābān','fazla mesai'),'latehome':('晚一点回家','wǎn yìdiǎn huí jiā','eve biraz geç dönmek'),'call':('打电话','dǎ diànhuà','telefon etmek'),'work':('工作','gōngzuò','iş'),
'birthday':('生日','shēngrì','doğum günü'),'gift':('礼物','lǐwù','hediye'),'choose':('选择','xuǎnzé','seçmek'),'pretty':('漂亮','piàoliang','güzel'),'useful':('有用','yǒuyòng','kullanışlı'),
'upstairs':('楼上','lóushàng','üst kat'),'downstairs':('楼下','lóuxià','alt kat'),'doorway':('门口','ménkǒu','kapı önü'),'cat':('猫','māo','kedi'),'find':('找到','zhǎodào','bulmak'),
'plan':('套餐','tàocān','tarife / paket'),'data':('流量','liúliàng','internet kotası'),'minute':('分钟','fēnzhōng','dakika'),'compare':('比较','bǐjiào','karşılaştırmak'),'monthly':('每月','měiyuè','her ay'),
'picnic':('野餐','yěcān','piknik'),'food':('食物','shíwù','yiyecek'),'forget':('忘了','wàng le','unutmak'),'bag':('包','bāo','çanta'),'luckily':('还好','háihǎo','neyse ki / iyi ki'),
'parentmeeting':('家长会','jiāzhǎnghuì','veli toplantısı'),'teacher':('老师','lǎoshī','öğretmen'),'progress':('进步','jìnbù','ilerleme'),'need':('需要','xūyào','gerekmek'),'study':('学习','xuéxí','ders çalışma'),
'guest':('客人','kèrén','misafir'),'friend':('朋友','péngyou','arkadaş'),'sit':('坐','zuò','oturmak'),'welcome':('欢迎','huānyíng','hoş geldin'),'polite':('别客气','bié kèqi','çekinme / rica ederim'),
'equipment':('设备','shèbèi','ekipman'),'problem':('问题','wèntí','sorun'),'step':('步骤','bùzhòu','adım'),'check':('检查','jiǎnchá','kontrol etmek'),'fix':('修好','xiūhǎo','tamir etmek'),
'haircut':('理发','lǐfà','saç kestirmek'),'short':('短','duǎn','kısa'),'long':('长','cháng','uzun'),'style':('样子','yàngzi','şekil / görünüm'),'barber':('理发师','lǐfàshī','berber'),
'recipe':('菜谱','càipǔ','tarif'),'salt':('盐','yán','tuz'),'spice':('调料','tiáoliào','baharat'),'salty':('咸','xián','tuzlu'),'taste':('味道','wèidào','tat'),
'powercut':('停电','tíngdiàn','elektrik kesintisi'),'light':('灯','dēng','ışık / lamba'),'flashlight':('手电筒','shǒudiàntǒng','el feneri'),'candle':('蜡烛','làzhú','mum'),'dark':('黑','hēi','karanlık'),
'wintercoat':('冬衣','dōngyī','kışlık kıyafet'),'size':('尺码','chǐmǎ','beden'),'tryon':('试','shì','denemek'),'bigger':('大一点','dà yìdiǎn','biraz daha büyük'),'smaller':('小一点','xiǎo yìdiǎn','biraz daha küçük'),
'lostbag':('丢了包','diū le bāo','çantayı kaybetmek'),'lostfound':('失物招领处','shīwù zhāolǐng chù','kayıp eşya bürosu'),'inside':('里面','lǐmiàn','içinde'),'color':('颜色','yánsè','renk'),'describe':('说明','shuōmíng','tarif etmek / açıklamak'),
'sick':('生病','shēngbìng','hasta olmak'),'rest':('休息','xiūxi','dinlenmek'),'better':('好一点','hǎo yìdiǎn','biraz daha iyi'),'medicine':('药','yào','ilaç'),'visit':('看望','kànwàng','ziyaret etmek'),
'movie':('电影','diànyǐng','film'),'opinion':('觉得','juéde','düşünmek'),'funny':('好笑','hǎoxiào','komik'),'interesting':('有意思','yǒuyìsi','ilginç'),'decide':('决定','juédìng','karar vermek'),
'librarycard':('借书证','jièshūzhèng','kütüphane kartı'),'borrow':('借','jiè','ödünç almak'),'return':('还','huán','iade etmek'),'book':('书','shū','kitap'),'library':('图书馆','túshūguǎn','kütüphane'),
'match':('比赛','bǐsài','maç / yarışma'),'win':('赢','yíng','kazanmak'),'lose':('输','shū','kaybetmek'),'cheer':('加油','jiāyóu','haydi / başarılar'),'team':('队','duì','takım'),
'order':('订单','dìngdān','sipariş'),'cake':('蛋糕','dàngāo','pasta'),'large':('大','dà','büyük'),'small':('小','xiǎo','küçük'),'peoplecount':('几个人','jǐ ge rén','kaç kişi'),
'budget':('预算','yùsuàn','bütçe'),'spend':('花钱','huā qián','para harcamak'),'necessary':('必要','bìyào','gerekli'),'save':('省钱','shěng qián','para tasarrufu'),'cost':('费用','fèiyòng','masraf'),
'past':('以前','yǐqián','önceden'),'now':('现在','xiànzài','şimdi'),'already':('已经','yǐjīng','çoktan / artık'),'life':('生活','shēnghuó','hayat'),'city':('城市','chéngshì','şehir'),
'raincoat':('雨衣','yǔyī','yağmurluk'),'rain':('下雨','xiàyǔ','yağmur yağmak'),'umbrella':('雨伞','yǔsǎn','şemsiye'),'outside':('外面','wàimiàn','dışarı'),'bring':('带','dài','yanına almak'),
'tooth':('牙','yá','diş'),'pain':('疼','téng','ağrımak'),'fallout':('掉了','diào le','düşmek'),'scared':('害怕','hàipà','korkmak'),'okay':('没关系','méi guānxi','önemli değil'),
'wrongstop':('下错站','xià cuò zhàn','yanlış durakta inmek'),'direction':('方向','fāngxiàng','yön'),'turn':('转','zhuǎn','dönmek'),'straight':('一直走','yìzhí zǒu','dümdüz gitmek'),'map':('地图','dìtú','harita'),
'wrongfile':('发错文件','fā cuò wénjiàn','yanlış dosya göndermek'),'file':('文件','wénjiàn','dosya'),'sorry':('对不起','duìbuqǐ','özür dilerim'),'change':('修改','xiūgǎi','düzeltmek / değiştirmek'),'immediately':('马上','mǎshàng','hemen'),
'bank':('银行','yínháng','banka'),'postoffice':('邮局','yóujú','postane'),'park':('公园','gōngyuán','park'),'center':('市中心','shì zhōngxīn','şehir merkezi'),'distance':('离','lí','-den uzaklık'),
'account':('账户','zhànghù','hesap'),'idcard':('身份证','shēnfènzhèng','kimlik kartı'),'form':('表格','biǎogé','form'),'sign':('签字','qiānzì','imza atmak'),'document':('材料','cáiliào','belge / evrak'),
'parcel':('包裹','bāoguǒ','paket'),'send':('寄','jì','göndermek'),'address':('地址','dìzhǐ','adres'),'arrive':('到','dào','ulaşmak'),'days':('几天','jǐ tiān','kaç gün'),
'help':('帮忙','bāngmáng','yardım etmek'),'meal':('饭','fàn','yemek'),'bringfood':('送饭','sòng fàn','yemek götürmek'),'family':('家人','jiārén','aile'),'thanks':('谢谢','xièxie','teşekkür'),
'clean':('打扫','dǎsǎo','temizlemek'),'trash':('垃圾','lājī','çöp'),'community':('社区','shèqū','mahalle / topluluk'),'volunteer':('志愿者','zhìyuànzhě','gönüllü'),'cleanliness':('干净','gānjìng','temiz'),
'snack':('点心','diǎnxin','atıştırmalık / hamur işi'),'sell':('卖','mài','satmak'),'buy':('买','mǎi','satın almak'),'delicious':('好吃','hǎochī','lezzetli'),'customer':('顾客','gùkè','müşteri'),
'newcolleague':('新同事','xīn tóngshì','yeni iş arkadaşı'),'attention':('注意','zhùyì','dikkat etmek'),'remember':('记得','jìde','hatırlamak'),'firststep':('第一步','dì yí bù','ilk adım'),'teach':('教','jiāo','öğretmek'),
'performance':('演出','yǎnchū','gösteri'),'nervous':('紧张','jǐnzhāng','gergin'),'again':('再一次','zài yí cì','bir kez daha'),'stage':('舞台','wǔtái','sahne'),'line':('台词','táicí','replik'),
'misunderstand':('误会','wùhuì','yanlış anlamak'),'meaning':('意思','yìsi','anlam / niyet'),'apologize':('道歉','dàoqiàn','özür dilemek'),'makeup':('和好','héhǎo','barışmak'),'talk':('谈一谈','tán yì tán','konuşmak'),
'fat':('胖','pàng','kilolu'),'less':('少一点','shǎo yìdiǎn','biraz daha az'),'exercise':('运动','yùndòng','egzersiz'),'weight':('体重','tǐzhòng','kilo'),'vet':('兽医','shòuyī','veteriner'),
'walk':('走路','zǒulù','yürümek'),'everyday':('每天','měitiān','her gün'),'everyweek':('每周','měizhōu','her hafta'),'continue':('坚持','jiānchí','devam etmek / sürdürmek'),'planword':('计划','jìhuà','plan'),
'festival':('节日','jiérì','bayram / festival'),'prepare':('准备','zhǔnbèi','hazırlamak'),'decorate':('装饰','zhuāngshì','süslemek'),'come':('来','lái','gelmek'),'stillneed':('还要','háiyào','ayrıca gerek'),
'video':('视频','shìpín','video'),'see':('看得见','kàn de jiàn','görebilmek'),'hear':('听得见','tīng de jiàn','duyabilmek'),'grandparents':('爷爷奶奶','yéye nǎinai','büyükanne ve büyükbaba'),'screen':('屏幕','píngmù','ekran'),
'farmveg':('蔬菜','shūcài','sebze'),'grow':('种','zhòng','yetiştirmek'),'box':('箱子','xiāngzi','kutu'),'many':('这么多','zhème duō','bu kadar çok'),'farm':('农场','nóngchǎng','çiftlik'),
'portion':('份','fèn','porsiyon / adet'),'enough':('够','gòu','yeterli'),'lack':('还差','hái chà','eksik kalmak'),'cook':('做饭','zuòfàn','yemek yapmak'),'event':('活动','huódòng','etkinlik'),
'review':('评价','píngjià','değerlendirme'),'improve':('提高','tígāo','geliştirmek'),'strength':('优点','yōudiǎn','güçlü yön'),'future':('以后','yǐhòu','bundan sonra'),'manager':('经理','jīnglǐ','müdür'),
'closefriend':('好朋友','hǎo péngyou','yakın arkadaş'),'same':('一样','yíyàng','aynı'),'often':('常常','chángcháng','sık sık'),'hobby':('爱好','àihào','hobi'),'together':('一起','yìqǐ','birlikte'),
'bicycle':('自行车','zìxíngchē','bisiklet'),'can':('会','huì','yapabilmek'),'notyet':('还不会','hái bú huì','henüz yapamamak'),'fall':('摔倒','shuāidǎo','düşmek'),'retry':('再试一次','zài shì yí cì','bir kez daha denemek'),
'spring':('春天','chūntiān','ilkbahar'),'warm':('暖和','nuǎnhuo','ılık / sıcak'),'flower':('花','huā','çiçek'),'bloom':('开了','kāi le','açtı'),'winter':('冬天','dōngtiān','kış'),
'photo':('照片','zhàopiàn','fotoğraf'),'year':('一年','yì nián','bir yıl'),'remember2':('记得','jìde','hatırlamak'),'went':('去过','qùguo','gitmiş olmak'),'that_time':('那时候','nà shíhou','o zaman'),
'oneyear':('这一年','zhè yì nián','bu bir yıl'),'hope':('希望','xīwàng','umut etmek'),'future2':('以后','yǐhòu','gelecekte'),'happy':('开心','kāixīn','mutlu'),'home':('家','jiā','ev')
}

# Scene vocabulary (first six active, remaining review/passive).
V = {
1:['routine','morning','bathroom','first','then','wait','hurry','home'],
2:['buscard','month','day','ticketoffice','price','choose','work','monthly'],
3:['vegetable','fruit','jin','price','fresh','buy','market' if False else 'vegetable','bag'],
4:['late','schoolbus','wait','neighbor','hurry','call','morning','help'],
5:['club','sport','music','because','therefore','choose','friend','schoolbus'],
6:['overtime','latehome','call','work','family','evening' if False else 'morning','manager','home'],
7:['birthday','gift','choose','pretty','useful','price','friend','buy'],
8:['upstairs','downstairs','doorway','cat','find','neighbor','call','home'],
9:['plan','data','minute','compare','monthly','price','month','choose'],
10:['picnic','food','forget','bag','luckily','park','family','bring'],
11:['parentmeeting','teacher','progress','need','study','child' if False else 'family','schoolbus','future'],
12:['guest','friend','sit','welcome','polite','tea' if False else 'food','home','family'],
13:['equipment','problem','step','check','fix','work','attention','firststep'],
14:['haircut','short','long','style','barber','pretty','choose','check'],
15:['recipe','salt','spice','salty','taste','food','first','then'],
16:['powercut','light','flashlight','candle','dark','home','find','wait'],
17:['wintercoat','size','tryon','bigger','smaller','choose','price','winter'],
18:['lostbag','lostfound','inside','color','describe','bag','find','call'],
19:['sick','rest','better','medicine','visit','work','friend','help'],
20:['movie','opinion','funny','interesting','decide','family','because','therefore'],
21:['librarycard','borrow','return','book','library','form','idcard','days'],
22:['match','win','lose','cheer','team','sport','hurry','friend'],
23:['order','cake','large','small','peoplecount','birthday','price','choose'],
24:['budget','spend','necessary','save','cost','family','month','planword'],
25:['past','now','already','life','city','friend','work','home'],
26:['raincoat','rain','umbrella','outside','bring','hurry','schoolbus','morning'],
27:['tooth','pain','fallout','scared','okay','family','doctor' if False else 'medicine','better'],
28:['wrongstop','direction','turn','straight','map','call','home','find'],
29:['wrongfile','file','sorry','change','immediately','work','manager','check'],
30:['bank','postoffice','park','center','distance','city','map','family'],
31:['account','idcard','form','sign','document','bank','need','check'],
32:['parcel','send','address','arrive','days','postoffice','grandparents','gift'],
33:['help','meal','bringfood','family','thanks','sick','friend','visit'],
34:['clean','trash','community','volunteer','cleanliness','together','help','event'],
35:['snack','sell','buy','delicious','customer','cake','neighbor','order'],
36:['newcolleague','attention','remember','firststep','teach','work','step','check'],
37:['performance','nervous','again','stage','line','schoolbus','teacher','cheer'],
38:['misunderstand','meaning','apologize','makeup','talk','friend','sorry','okay'],
39:['fat','less','exercise','weight','vet','cat','food','walk'],
40:['walk','everyday','everyweek','continue','planword','family','park','exercise'],
41:['festival','prepare','decorate','come','stillneed','family','gift','food'],
42:['video','see','hear','grandparents','screen','home','family','call'],
43:['farmveg','fresh','grow','box','many','farm','grandparents','food'],
44:['portion','enough','lack','cook','event','community','food','help'],
45:['review','improve','strength','future','manager','work','progress','need'],
46:['closefriend','same','often','hobby','together','music','sport','friend'],
47:['bicycle','can','notyet','fall','retry','park','child' if False else 'family','cheer'],
48:['spring','warm','flower','bloom','winter','park','weather' if False else 'outside','family'],
49:['photo','year','remember2','went','that_time','family','city','happy'],
50:['oneyear','already','hope','future2','happy','home','friend','life']
}

# Fix accidental unavailable keys by substituting safe ones.
for n, keys in list(V.items()):
    V[n] = [k for k in keys if k in W]
    while len(V[n]) < 8:
        V[n].append(['family','home','friend','work','city','happy','planword','help'][len(V[n]) % 8])

ROLES = {
1:['刘梅','张伟','张雨桐','张乐乐'],2:['张伟','工作人员','刘梅'],3:['刘梅','摊主','邻居'],4:['张乐乐','刘梅','邻居'],5:['张雨桐','同学','老师'],
6:['张伟','刘梅','同事'],7:['刘梅','张伟','张乐乐','店员'],8:['张乐乐','张雨桐','刘梅','邻居'],9:['张伟','刘梅','店员'],10:['张伟','刘梅','张雨桐','张乐乐'],
11:['刘梅','老师','张乐乐'],12:['张雨桐','同学','刘梅','张伟'],13:['张伟','同事','新同事'],14:['张伟','理发师','刘梅'],15:['刘梅','张伟','张雨桐'],
16:['张伟','刘梅','张乐乐','张雨桐'],17:['刘梅','张雨桐','张乐乐','店员'],18:['张雨桐','刘梅','工作人员'],19:['张伟','同事','刘梅'],20:['张伟','刘梅','张雨桐','张乐乐'],
21:['张乐乐','刘梅','图书管理员'],22:['张雨桐','张伟','刘梅','队友'],23:['刘梅','邻居','张伟'],24:['张伟','刘梅','张雨桐'],25:['张伟','李晨','刘梅'],
26:['刘梅','张乐乐','张雨桐','张伟'],27:['张乐乐','刘梅','张伟'],28:['张雨桐','刘梅','路人'],29:['张伟','同事','经理'],30:['张伟','刘梅','张乐乐','张雨桐'],
31:['张伟','银行工作人员','刘梅'],32:['张伟','刘梅','邮局工作人员'],33:['刘梅','张伟','李晨','李晨妻子'],34:['张伟','刘梅','社区工作人员','张乐乐'],35:['刘梅','邻居','张伟'],
36:['张伟','新同事','经理'],37:['张乐乐','老师','刘梅','张伟'],38:['张雨桐','同学','刘梅'],39:['刘梅','张乐乐','兽医','张伟'],40:['张伟','刘梅','张乐乐','张雨桐'],
41:['刘梅','张伟','张乐乐','张雨桐'],42:['张伟','刘梅','爷爷','奶奶'],43:['张伟','刘梅','张乐乐','爷爷'],44:['刘梅','社区工作人员','志愿者','张伟'],45:['张伟','经理','同事'],
46:['张雨桐','好朋友','刘梅'],47:['张乐乐','张伟','刘梅'],48:['张伟','刘梅','张雨桐','张乐乐'],49:['张伟','刘梅','张雨桐','张乐乐'],50:['张伟','刘梅','李晨','李晨妻子']
}

# Scene-specific setup / complication / resolution anchors.
B = {
1:[('大家都要用洗手间。','Dàjiā dōu yào yòng xǐshǒujiān.','Herkes banyoyu kullanmak istiyor.'),('时间不多了，我们来不及了。','Shíjiān bù duō le, wǒmen láibují le.','Fazla zaman kalmadı, yetişemeyeceğiz.'),('先乐乐，再雨桐，这样最快。','Xiān Lèlè, zài Yǔtóng, zhèyàng zuì kuài.','Önce Lele, sonra Yutong; en hızlısı böyle.')],
2:[('我想办公交卡。','Wǒ xiǎng bàn gōngjiāo kǎ.','Otobüs kartı almak istiyorum.'),('这个不是我要的卡。','Zhège bú shì wǒ yào de kǎ.','Bu istediğim kart değil.'),('我要一个月的，谢谢。','Wǒ yào yí ge yuè de, xièxie.','Bir aylık olanı istiyorum, teşekkürler.')],
3:[('今天的菜很新鲜。','Jīntiān de cài hěn xīnxiān.','Bugünkü sebzeler çok taze.'),('这个价格有点贵。','Zhège jiàgé yǒudiǎn guì.','Bu fiyat biraz pahalı.'),('好，那我买两斤。','Hǎo, nà wǒ mǎi liǎng jīn.','Tamam, o zaman bir kilo alayım.')],
4:[('校车已经走了。','Xiàochē yǐjīng zǒu le.','Okul servisi çoktan gitti.'),('乐乐今天要迟到了。','Lèlè jīntiān yào chídào le.','Lele bugün geç kalacak.'),('邻居可以开车送他。','Línjū kěyǐ kāichē sòng tā.','Komşu onu arabayla götürebilir.')],
5:[('雨桐想参加一个社团。','Yǔtóng xiǎng cānjiā yí ge shètuán.','Yutong bir kulübe katılmak istiyor.'),('运动和音乐，她都喜欢。','Yùndòng hé yīnyuè, tā dōu xǐhuan.','Hem sporu hem müziği seviyor.'),('她决定先去看看两个社团。','Tā juédìng xiān qù kànkan liǎng ge shètuán.','Önce iki kulübe de bakmaya karar veriyor.')],
6:[('今天我要加班。','Jīntiān wǒ yào jiābān.','Bugün fazla mesai yapacağım.'),('我可能晚一点回家。','Wǒ kěnéng wǎn yìdiǎn huí jiā.','Eve biraz geç dönebilirim.'),('你们先吃饭，不用等我。','Nǐmen xiān chīfàn, búyòng děng wǒ.','Siz önce yemek yiyin, beni beklemeyin.')],
7:[('邻居明天过生日。','Línjū míngtiān guò shēngrì.','Komşunun yarın doğum günü.'),('我们不知道送什么好。','Wǒmen bù zhīdào sòng shénme hǎo.','Ne hediye edeceğimizi bilmiyoruz.'),('这个礼物漂亮又有用。','Zhège lǐwù piàoliang yòu yǒuyòng.','Bu hediye hem güzel hem kullanışlı.')],
8:[('咪咪跑到楼上了。','Mīmī pǎo dào lóushàng le.','Mimi üst kata kaçtı.'),('我们找了半天还没找到。','Wǒmen zhǎo le bàntiān hái méi zhǎodào.','Uzun süre aradık ama hâlâ bulamadık.'),('它在邻居家门口。','Tā zài línjū jiā ménkǒu.','Komşunun kapısının önünde.')],
9:[('我们想换手机套餐。','Wǒmen xiǎng huàn shǒujī tàocān.','Telefon tarifesini değiştirmek istiyoruz.'),('这个流量多，但是更贵。','Zhège liúliàng duō, dànshì gèng guì.','Bunun interneti fazla ama daha pahalı.'),('这个套餐更适合我们。','Zhège tàocān gèng shìhé wǒmen.','Bu tarife bize daha uygun.')],
10:[('我们到公园了。','Wǒmen dào gōngyuán le.','Parka geldik.'),('糟了，我们拿错包了。','Zāo le, wǒmen ná cuò bāo le.','Eyvah, yanlış çantayı almışız.'),('还好这里可以买吃的。','Háihǎo zhèlǐ kěyǐ mǎi chī de.','Neyse ki burada yiyecek alabiliriz.')],
11:[('今天是第一次家长会。','Jīntiān shì dì yí cì jiāzhǎnghuì.','Bugün ilk veli toplantısı.'),('乐乐有一点不认真。','Lèlè yǒu yìdiǎn bù rènzhēn.','Lele biraz dikkatsiz.'),('他只需要每天多读一点。','Tā zhǐ xūyào měitiān duō dú yìdiǎn.','Sadece her gün biraz daha çok okuması gerekiyor.')],
12:[('雨桐的朋友第一次来家里。','Yǔtóng de péngyou dì yí cì lái jiālǐ.','Yutong’un arkadaşı ilk kez eve geliyor.'),('她有一点紧张。','Tā yǒu yìdiǎn jǐnzhāng.','Biraz gergin.'),('别客气，就像在自己家一样。','Bié kèqi, jiù xiàng zài zìjǐ jiā yíyàng.','Çekinme, kendi evindeymiş gibi rahat ol.')],
13:[('这个设备有一点问题。','Zhège shèbèi yǒu yìdiǎn wèntí.','Bu ekipmanda küçük bir sorun var.'),('我们先检查，再重新打开。','Wǒmen xiān jiǎnchá, zài chóngxīn dǎkāi.','Önce kontrol edip sonra yeniden açalım.'),('好了，现在可以用了。','Hǎo le, xiànzài kěyǐ yòng le.','Tamam, şimdi kullanılabilir.')],
14:[('我想把头发剪短一点。','Wǒ xiǎng bǎ tóufa jiǎn duǎn yìdiǎn.','Saçımı biraz daha kısa kestirmek istiyorum.'),('不是这么短。','Bú shì zhème duǎn.','Bu kadar kısa değil.'),('这样可以，正好。','Zhèyàng kěyǐ, zhènghǎo.','Böyle iyi, tam oldu.')],
15:[('刘梅今天试一个新菜谱。','Liú Méi jīntiān shì yí ge xīn càipǔ.','Liu Mei bugün yeni bir tarif deniyor.'),('盐放多了，有点咸。','Yán fàng duō le, yǒudiǎn xián.','Tuz fazla oldu, biraz tuzlu.'),('再加一点水，味道好多了。','Zài jiā yìdiǎn shuǐ, wèidào hǎo duō le.','Biraz daha su ekleyince tadı çok daha iyi oldu.')],
16:[('突然停电了。','Tūrán tíngdiàn le.','Birden elektrik kesildi.'),('屋里太黑，什么也看不见。','Wūli tài hēi, shénme yě kàn bú jiàn.','Ev çok karanlık, hiçbir şey görünmüyor.'),('我们找到了手电筒和蜡烛。','Wǒmen zhǎodào le shǒudiàntǒng hé làzhú.','El feneri ve mumları bulduk.')],
17:[('天气冷了，该买冬衣了。','Tiānqì lěng le, gāi mǎi dōngyī le.','Hava soğudu, kışlık kıyafet alma zamanı.'),('这个尺码太小。','Zhège chǐmǎ tài xiǎo.','Bu beden çok küçük.'),('换大一点的正好。','Huàn dà yìdiǎn de zhènghǎo.','Biraz daha büyüğü tam oldu.')],
18:[('我的包忘在公交车上了。','Wǒ de bāo wàng zài gōngjiāochē shàng le.','Çantamı otobüste unuttum.'),('里面有书和钥匙。','Lǐmiàn yǒu shū hé yàoshi.','İçinde kitap ve anahtar var.'),('工作人员找到了我的包。','Gōngzuò rényuán zhǎodào le wǒ de bāo.','Görevli çantamı buldu.')],
19:[('同事今天生病了。','Tóngshì jīntiān shēngbìng le.','İş arkadaşım bugün hasta.'),('你要多休息，按时吃药。','Nǐ yào duō xiūxi, ànshí chī yào.','Çok dinlenip ilacını zamanında almalısın.'),('谢谢，我已经好多了。','Xièxie, wǒ yǐjīng hǎo duō le.','Teşekkürler, artık çok daha iyiyim.')],
20:[('今晚我们一起看电影。','Jīnwǎn wǒmen yìqǐ kàn diànyǐng.','Bu akşam birlikte film izleyeceğiz.'),('大家想看的电影都不一样。','Dàjiā xiǎng kàn de diànyǐng dōu bù yíyàng.','Herkes farklı bir film izlemek istiyor.'),('那就选一个大家都觉得有意思的。','Nà jiù xuǎn yí ge dàjiā dōu juéde yǒuyìsi de.','O zaman herkesin ilginç bulduğu bir film seçelim.')],
21:[('乐乐今天要办借书证。','Lèlè jīntiān yào bàn jièshūzhèng.','Lele bugün kütüphane kartı çıkaracak.'),('第一次可以借几本书？','Dì yí cì kěyǐ jiè jǐ běn shū?','İlk seferde kaç kitap ödünç alınabilir?'),('记得两个星期以后还。','Jìde liǎng ge xīngqī yǐhòu huán.','İki hafta sonra iade etmeyi unutma.')],
22:[('雨桐的比赛快开始了。','Yǔtóng de bǐsài kuài kāishǐ le.','Yutong’un maçı başlamak üzere.'),('我们差一点来晚了。','Wǒmen chà yìdiǎn lái wǎn le.','Neredeyse geç kalıyorduk.'),('加油！不管输赢都要开心。','Jiāyóu! Bùguǎn shū yíng dōu yào kāixīn.','Haydi! Kazansan da kaybetsen de keyfini çıkar.')],
23:[('这是刘梅的第一个蛋糕订单。','Zhè shì Liú Méi de dì yí ge dàngāo dìngdān.','Bu Liu Mei’nin ilk pasta siparişi.'),('蛋糕要多大？几个人吃？','Dàngāo yào duō dà? Jǐ ge rén chī?','Pasta ne kadar büyük olsun? Kaç kişi yiyecek?'),('好的，星期六下午来拿。','Hǎo de, xīngqīliù xiàwǔ lái ná.','Tamam, cumartesi öğleden sonra almaya gelin.')],
24:[('我们来看看这个月的预算。','Wǒmen lái kànkan zhège yuè de yùsuàn.','Bu ayın bütçesine bakalım.'),('有些东西现在不一定要买。','Yǒuxiē dōngxi xiànzài bù yídìng yào mǎi.','Bazı şeyleri şimdi almak şart değil.'),('这样可以省一点钱。','Zhèyàng kěyǐ shěng yìdiǎn qián.','Böylece biraz para tasarruf edebiliriz.')],
25:[('我们来新城已经一年了。','Wǒmen lái Xīnchéng yǐjīng yì nián le.','Yeni şehre geleli bir yıl oldu.'),('以前我们一个朋友也没有。','Yǐqián wǒmen yí ge péngyou yě méiyǒu.','Önceden hiç arkadaşımız yoktu.'),('现在这里越来越像家了。','Xiànzài zhèlǐ yuèláiyuè xiàng jiā le.','Şimdi burası giderek daha çok evimiz gibi geliyor.')],
26:[('外面正在下雨。','Wàimiàn zhèngzài xiàyǔ.','Dışarıda yağmur yağıyor.'),('雨衣怎么找不到了？','Yǔyī zěnme zhǎo bú dào le?','Yağmurluklar nasıl oldu da bulunamıyor?'),('带上雨伞，快一点出发。','Dài shàng yǔsǎn, kuài yìdiǎn chūfā.','Şemsiyeyi alıp biraz hızlı çıkalım.')],
27:[('乐乐的牙掉了。','Lèlè de yá diào le.','Lele’nin dişi düştü.'),('疼不疼？别害怕。','Téng bu téng? Bié hàipà.','Acıyor mu? Korkma.'),('没关系，这是长大的事情。','Méi guānxi, zhè shì zhǎngdà de shìqing.','Sorun değil, bu büyümenin bir parçası.')],
28:[('我好像下错站了。','Wǒ hǎoxiàng xià cuò zhàn le.','Sanırım yanlış durakta indim.'),('你先看地图，然后一直走。','Nǐ xiān kàn dìtú, ránhòu yìzhí zǒu.','Önce haritaya bak, sonra dümdüz yürü.'),('我看到家附近的商店了。','Wǒ kàndào jiā fùjìn de shāngdiàn le.','Evin yakınındaki dükkânı gördüm.')],
29:[('我刚才发错文件了。','Wǒ gāngcái fā cuò wénjiàn le.','Az önce yanlış dosyayı gönderdim.'),('对不起，我马上修改。','Duìbuqǐ, wǒ mǎshàng xiūgǎi.','Özür dilerim, hemen düzelteceğim.'),('新文件已经发过去了。','Xīn wénjiàn yǐjīng fā guòqu le.','Yeni dosyayı çoktan gönderdim.')],
30:[('周末我们去市中心看看。','Zhōumò wǒmen qù shì zhōngxīn kànkan.','Hafta sonu şehir merkezini gezelim.'),('银行离邮局远不远？','Yínháng lí yóujú yuǎn bu yuǎn?','Banka postaneden uzak mı?'),('先去银行，再去公园。','Xiān qù yínháng, zài qù gōngyuán.','Önce bankaya, sonra parka gidelim.')],
31:[('我想开一个银行账户。','Wǒ xiǎng kāi yí ge yínháng zhànghù.','Bir banka hesabı açmak istiyorum.'),('还需要身份证和一份材料。','Hái xūyào shēnfènzhèng hé yí fèn cáiliào.','Kimlik ve bir evrak daha gerekiyor.'),('材料补齐以后就可以开户。','Cáiliào bǔqí yǐhòu jiù kěyǐ kāihù.','Evraklar tamamlanınca hesap açılabilir.')],
32:[('我们要给爷爷奶奶寄包裹。','Wǒmen yào gěi yéye nǎinai jì bāoguǒ.','Büyükanne ve büyükbabaya paket göndereceğiz.'),('这个地址写得对吗？','Zhège dìzhǐ xiě de duì ma?','Bu adres doğru yazılmış mı?'),('大概三天就能到。','Dàgài sān tiān jiù néng dào.','Yaklaşık üç günde ulaşır.')],
33:[('李晨家有人生病了。','Lǐ Chén jiā yǒu rén shēngbìng le.','Li Chen’in ailesinden biri hasta.'),('我们给他们送点饭吧。','Wǒmen gěi tāmen sòng diǎn fàn ba.','Onlara biraz yemek götürelim.'),('谢谢，你们真帮了大忙。','Xièxie, nǐmen zhēn bāng le dà máng.','Teşekkürler, bize gerçekten çok yardımcı oldunuz.')],
34:[('今天是社区清洁日。','Jīntiān shì shèqū qīngjié rì.','Bugün mahalle temizlik günü.'),('这里的垃圾比那边多。','Zhèlǐ de lājī bǐ nàbian duō.','Buradaki çöp oradakinden daha fazla.'),('大家一起打扫以后干净多了。','Dàjiā yìqǐ dǎsǎo yǐhòu gānjìng duō le.','Herkes birlikte temizleyince çok daha temiz oldu.')],
35:[('大家都喜欢刘梅做的点心。','Dàjiā dōu xǐhuan Liú Méi zuò de diǎnxin.','Herkes Liu Mei’nin yaptığı hamur işlerini seviyor.'),('已经有人问可不可以买了。','Yǐjīng yǒu rén wèn kě bu kěyǐ mǎi le.','Artık satın alıp alamayacaklarını soranlar var.'),('也许可以先接几个小订单。','Yěxǔ kěyǐ xiān jiē jǐ ge xiǎo dìngdān.','Belki önce birkaç küçük sipariş alınabilir.')],
36:[('今天我来带新同事。','Jīntiān wǒ lái dài xīn tóngshì.','Bugün yeni iş arkadaşına ben rehberlik edeceğim.'),('第一步要特别注意安全。','Dì yí bù yào tèbié zhùyì ānquán.','İlk adımda güvenliğe özellikle dikkat etmek gerekiyor.'),('你做得不错，记得按步骤来。','Nǐ zuò de búcuò, jìde àn bùzhòu lái.','İyi yaptın, adımlara göre ilerlemeyi unutma.')],
37:[('乐乐今天参加学校演出。','Lèlè jīntiān cānjiā xuéxiào yǎnchū.','Lele bugün okul gösterisine katılıyor.'),('他一紧张就忘了台词。','Tā yì jǐnzhāng jiù wàng le táicí.','Gerilince repliğini unuttu.'),('老师提醒以后，他又说下去了。','Lǎoshī tíxǐng yǐhòu, tā yòu shuō xiàqu le.','Öğretmen hatırlatınca devam etti.')],
38:[('雨桐和朋友有一点误会。','Yǔtóng hé péngyou yǒu yìdiǎn wùhuì.','Yutong ile arkadaşının küçük bir yanlış anlaşılması var.'),('我不是那个意思，对不起。','Wǒ bú shì nàge yìsi, duìbuqǐ.','Öyle demek istemedim, özür dilerim.'),('说开以后，她们又和好了。','Shuō kāi yǐhòu, tāmen yòu héhǎo le.','Konuşup açıklığa kavuşturunca barıştılar.')],
39:[('兽医说咪咪有点胖。','Shòuyī shuō Mīmī yǒudiǎn pàng.','Veteriner Mimi’nin biraz kilolu olduğunu söyledi.'),('以后要少吃一点，多运动。','Yǐhòu yào shǎo chī yìdiǎn, duō yùndòng.','Bundan sonra biraz daha az yiyip daha çok hareket etmeli.'),('我们每天陪它多走一走。','Wǒmen měitiān péi tā duō zǒu yì zǒu.','Her gün onunla biraz daha çok yürüyelim.')],
40:[('我们需要一个全家运动计划。','Wǒmen xūyào yí ge quánjiā yùndòng jìhuà.','Ailece bir egzersiz planına ihtiyacımız var.'),('只做一天没有用。','Zhǐ zuò yì tiān méiyǒu yòng.','Sadece bir gün yapmak işe yaramaz.'),('每周一起走三次，大家都要坚持。','Měizhōu yìqǐ zǒu sān cì, dàjiā dōu yào jiānchí.','Haftada üç kez birlikte yürüyüp herkes devam etmeli.')],
41:[('节日快到了，我们开始准备吧。','Jiérì kuài dào le, wǒmen kāishǐ zhǔnbèi ba.','Bayram yaklaşıyor, hazırlanmaya başlayalım.'),('客人几点来？我们还差什么？','Kèrén jǐ diǎn lái? Wǒmen hái chà shénme?','Misafirler saat kaçta gelecek? Daha ne eksik?'),('装饰和吃的都准备好了。','Zhuāngshì hé chī de dōu zhǔnbèi hǎo le.','Süslemeler ve yiyecekler hazır.')],
42:[('爷爷奶奶想看看新家。','Yéye nǎinai xiǎng kànkan xīn jiā.','Büyükanne ve büyükbaba yeni evi görmek istiyor.'),('你们看得见吗？听得见吗？','Nǐmen kàn de jiàn ma? Tīng de jiàn ma?','Bizi görebiliyor ve duyabiliyor musunuz?'),('现在很清楚，我们都看见了。','Xiànzài hěn qīngchu, wǒmen dōu kànjiàn le.','Şimdi çok net, hepimiz görüyoruz.')],
43:[('爷爷从农场寄来一箱蔬菜。','Yéye cóng nóngchǎng jì lái yì xiāng shūcài.','Büyükbaba çiftlikten bir kutu sebze gönderdi.'),('这么多，而且特别新鲜。','Zhème duō, érqiě tèbié xīnxiān.','Bu kadar çok ve üstelik çok taze.'),('这些都是他自己种的。','Zhèxiē dōu shì tā zìjǐ zhòng de.','Bunların hepsini kendisi yetiştirmiş.')],
44:[('社区活动需要很多份饭。','Shèqū huódòng xūyào hěn duō fèn fàn.','Mahalle etkinliği için çok sayıda porsiyon yemek gerekiyor.'),('现在还差十份，够不够时间？','Xiànzài hái chà shí fèn, gòu bu gòu shíjiān?','Şimdi on porsiyon eksik, zaman yeter mi?'),('大家一起帮忙，最后都做好了。','Dàjiā yìqǐ bāngmáng, zuìhòu dōu zuò hǎo le.','Herkes yardım edince sonunda hepsi hazırlandı.')],
45:[('今天是第一次工作评价。','Jīntiān shì dì yí cì gōngzuò píngjià.','Bugün ilk performans değerlendirmesi.'),('你做得不错，但是沟通还可以提高。','Nǐ zuò de búcuò, dànshì gōutōng hái kěyǐ tígāo.','İyi gidiyorsun ama iletişimini daha da geliştirebilirsin.'),('以后我会更主动一点。','Yǐhòu wǒ huì gèng zhǔdòng yìdiǎn.','Bundan sonra biraz daha girişken olacağım.')],
46:[('雨桐有了一个很合得来的朋友。','Yǔtóng yǒu le yí ge hěn hé de lái de péngyou.','Yutong çok iyi anlaştığı bir arkadaş edindi.'),('她们有很多一样的爱好。','Tāmen yǒu hěn duō yíyàng de àihào.','Birçok ortak hobileri var.'),('以后她们常常一起学习和运动。','Yǐhòu tāmen chángcháng yìqǐ xuéxí hé yùndòng.','Bundan sonra sık sık birlikte ders çalışıp spor yapıyorlar.')],
47:[('乐乐今天学骑自行车。','Lèlè jīntiān xué qí zìxíngchē.','Lele bugün bisiklet sürmeyi öğreniyor.'),('他摔倒了一次，有点怕。','Tā shuāidǎo le yí cì, yǒudiǎn pà.','Bir kez düştü ve biraz korktu.'),('再试一次，他终于会了。','Zài shì yí cì, tā zhōngyú huì le.','Bir kez daha deneyince sonunda öğrendi.')],
48:[('新城的春天来了。','Xīnchéng de chūntiān lái le.','Yeni şehirde ilkbahar geldi.'),('天气比冬天暖和多了。','Tiānqì bǐ dōngtiān nuǎnhuo duō le.','Hava kışa göre çok daha sıcak.'),('公园里的花都开了。','Gōngyuán lǐ de huā dōu kāi le.','Parktaki çiçeklerin hepsi açtı.')],
49:[('我们来看看这一年的照片。','Wǒmen lái kànkan zhè yì nián de zhàopiàn.','Bu yılın fotoğraflarına bakalım.'),('这张是我们第一次去公园的时候。','Zhè zhāng shì wǒmen dì yí cì qù gōngyuán de shíhou.','Bu, parka ilk gittiğimiz zamanki fotoğraf.'),('这些照片让我们想起很多事情。','Zhèxiē zhàopiàn ràng wǒmen xiǎngqǐ hěn duō shìqing.','Bu fotoğraflar bize birçok şeyi hatırlatıyor.')],
50:[('我们在新城已经一年了。','Wǒmen zài Xīnchéng yǐjīng yì nián le.','Yeni şehirde bir yılı tamamladık.'),('这一年发生了很多事情。','Zhè yì nián fāshēng le hěn duō shìqing.','Bu yıl birçok şey oldu.'),('希望以后我们的生活越来越好。','Xīwàng yǐhòu wǒmen de shēnghuó yuèláiyuè hǎo.','Umarım bundan sonra hayatımız giderek daha güzel olur.')]
}

COMMON = [
('你觉得怎么样？','Nǐ juéde zěnmeyàng?','Sence nasıl?'),('我觉得不错。','Wǒ juéde búcuò.','Bence fena değil.'),('我也是这么想的。','Wǒ yě shì zhème xiǎng de.','Ben de böyle düşünüyorum.'),
('先别着急。','Xiān bié zháojí.','Önce telaşlanma.'),('我们想个办法。','Wǒmen xiǎng ge bànfǎ.','Bir çözüm düşünelim.'),('这样可以吗？','Zhèyàng kěyǐ ma?','Böyle olur mu?'),
('可以，没问题。','Kěyǐ, méi wèntí.','Olur, sorun değil.'),('还需要什么？','Hái xūyào shénme?','Başka ne gerekiyor?'),('应该够了。','Yīnggāi gòu le.','Yeterli olmalı.'),
('等一下，我再看看。','Děng yíxià, wǒ zài kànkan.','Bir dakika, bir kez daha bakayım.'),('我明白你的意思了。','Wǒ míngbai nǐ de yìsi le.','Ne demek istediğini anladım.'),('那我们就这样做。','Nà wǒmen jiù zhèyàng zuò.','O zaman böyle yapalım.'),
('比刚才好多了。','Bǐ gāngcái hǎo duō le.','Az öncekinden çok daha iyi.'),('已经准备好了。','Yǐjīng zhǔnbèi hǎo le.','Çoktan hazırlandı.'),('还没有完全好。','Hái méiyǒu wánquán hǎo.','Henüz tamamen hazır değil.'),
('因为时间不多，所以我们快一点。','Yīnwèi shíjiān bù duō, suǒyǐ wǒmen kuài yìdiǎn.','Zaman az olduğu için biraz hızlı olalım.'),('不用担心。','Búyòng dānxīn.','Endişelenmene gerek yok.'),('我来帮你吧。','Wǒ lái bāng nǐ ba.','Sana yardım edeyim.'),
('谢谢，帮大忙了。','Xièxie, bāng dà máng le.','Teşekkürler, çok yardımcı oldun.'),('没关系，大家互相帮忙。','Méi guānxi, dàjiā hùxiāng bāngmáng.','Sorun değil, birbirimize yardım ederiz.'),('现在怎么办？','Xiànzài zěnme bàn?','Şimdi ne yapacağız?'),
('先做这个，再做那个。','Xiān zuò zhège, zài zuò nàge.','Önce bunu, sonra şunu yapalım.'),('我已经试过了。','Wǒ yǐjīng shìguo le.','Bunu zaten denedim.'),('那再试一次吧。','Nà zài shì yí cì ba.','O zaman bir kez daha deneyelim.'),
('这个办法更好。','Zhège bànfǎ gèng hǎo.','Bu yöntem daha iyi.'),('终于好了。','Zhōngyú hǎo le.','Sonunda oldu.'),('今天学到了不少东西。','Jīntiān xuédào le bù shǎo dōngxi.','Bugün epey şey öğrendik.'),
('下次我们会更有经验。','Xià cì wǒmen huì gèng yǒu jīngyàn.','Bir dahaki sefere daha deneyimli olacağız.'),('好，那就这么决定。','Hǎo, nà jiù zhème juédìng.','Tamam, o halde kararımız bu.'),('走吧，我们继续。','Zǒu ba, wǒmen jìxù.','Hadi, devam edelim.')
]

PLACE_KEYS={'bathroom','ticketoffice','library','bank','postoffice','park','center','community','farm'}
PERSON_KEYS={'neighbor','teacher','friend','guest','barber','vet','manager','customer','volunteer','grandparents','closefriend','newcolleague','family'}
ACTION_KEYS={'choose','wait','call','compare','forget','study','check','fix','tryon','describe','rest','visit','decide','borrow','return','spend','save','bring','turn','change','sign','send','help','clean','sell','buy','teach','apologize','talk','exercise','walk','continue','prepare','decorate','see','hear','grow','cook','improve','retry','remember2'}
STATE_KEYS={'fresh','late','pretty','useful','short','long','salty','dark','bigger','smaller','sick','better','funny','interesting','necessary','scared','okay','fat','warm','happy','cleanliness','nervous'}
ABSTRACT_KEYS={'routine','price','club','plan','progress','problem','step','style','taste','opinion','budget','cost','life','direction','review','strength','hobby','weight','planword','event','meaning','performance','year','hope'}
TIME_FUNCTION_KEYS={'morning','first','then','because','therefore','month','day','monthly','past','now','already','outside','everyday','everyweek','future','future2','immediately','luckily','hurry','notyet','can','less','straight','that_time','oneyear','stillneed','many','days'}


def cap(s): return s[:1].upper()+s[1:] if s else s

# Natural, scene-safe usage lines. These are intentionally semantic rather than
# generated by a single noun template, which avoids nonsense such as comparing
# "morning" or "already" by price.
SPECIAL_USAGE={
 'routine':('今天的日常安排有一点乱。','Jīntiān de rìcháng ānpái yǒu yìdiǎn luàn.','Bugünkü günlük düzen biraz karışık.'),
 'morning':('今天早上大家都很忙。','Jīntiān zǎoshang dàjiā dōu hěn máng.','Bu sabah herkes çok meşgul.'),
 'first':('我们先做最重要的事。','Wǒmen xiān zuò zuì zhòngyào de shì.','Önce en önemli işi yapalım.'),
 'then':('做完这个再做别的。','Zuò wán zhège zài zuò bié de.','Bunu bitirdikten sonra diğer işi yapalım.'),
 'because':('因为时间不多，我们得快一点。','Yīnwèi shíjiān bù duō, wǒmen děi kuài yìdiǎn.','Zaman az olduğu için biraz hızlı olmalıyız.'),
 'therefore':('所以我们先解决这个问题。','Suǒyǐ wǒmen xiān jiějué zhège wèntí.','Bu yüzden önce bu sorunu çözelim.'),
 'month':('一个月的时间过得很快。','Yí ge yuè de shíjiān guò de hěn kuài.','Bir aylık süre çok hızlı geçiyor.'),
 'day':('一天用这个就够了。','Yì tiān yòng zhège jiù gòu le.','Bir gün için bunu kullanmak yeterli.'),
 'monthly':('这个套餐每月多少钱？','Zhège tàocān měiyuè duōshao qián?','Bu tarife ayda ne kadar?'),
 'past':('以前我们还不太习惯这里。','Yǐqián wǒmen hái bú tài xíguàn zhèlǐ.','Eskiden buraya pek alışık değildik.'),
 'now':('现在我们已经习惯多了。','Xiànzài wǒmen yǐjīng xíguàn duō le.','Şimdi buraya çok daha fazla alıştık.'),
 'already':('这个已经准备好了。','Zhège yǐjīng zhǔnbèi hǎo le.','Bu çoktan hazırlandı.'),
 'outside':('外面正在下雨。','Wàimiàn zhèngzài xiàyǔ.','Dışarıda yağmur yağıyor.'),
 'everyday':('我们每天都走一走。','Wǒmen měitiān dōu zǒu yì zǒu.','Her gün biraz yürüyoruz.'),
 'everyweek':('我们每周运动三次。','Wǒmen měizhōu yùndòng sān cì.','Haftada üç kez egzersiz yapıyoruz.'),
 'future':('以后我会更注意。','Yǐhòu wǒ huì gèng zhùyì.','Bundan sonra daha dikkatli olacağım.'),
 'future2':('希望以后越来越好。','Xīwàng yǐhòu yuèláiyuè hǎo.','Umarım gelecekte giderek daha iyi olur.'),
 'immediately':('我马上改。','Wǒ mǎshàng gǎi.','Hemen düzelteceğim.'),
 'luckily':('还好我们有别的办法。','Háihǎo wǒmen yǒu bié de bànfǎ.','Neyse ki başka bir çözümümüz var.'),
 'hurry':('快一点，不然来不及了。','Kuài yìdiǎn, bùrán láibují le.','Biraz hızlı ol, yoksa yetişemeyeceğiz.'),
 'notyet':('我还不会，但是我想再试。','Wǒ hái bú huì, dànshì wǒ xiǎng zài shì.','Henüz yapamıyorum ama tekrar denemek istiyorum.'),
 'can':('我现在会了。','Wǒ xiànzài huì le.','Artık yapabiliyorum.'),
 'less':('以后要少一点。','Yǐhòu yào shǎo yìdiǎn.','Bundan sonra biraz daha az olmalı.'),
 'straight':('从这里一直走就到了。','Cóng zhèlǐ yìzhí zǒu jiù dào le.','Buradan dümdüz gidince ulaşırsın.'),
 'that_time':('那时候我们刚来这里。','Nà shíhou wǒmen gāng lái zhèlǐ.','O zaman buraya yeni gelmiştik.'),
 'oneyear':('这一年过得很快。','Zhè yì nián guò de hěn kuài.','Bu bir yıl çok hızlı geçti.'),
 'stillneed':('我们还要准备一些东西。','Wǒmen hái yào zhǔnbèi yìxiē dōngxi.','Daha bazı şeyler hazırlamamız gerekiyor.'),
 'many':('怎么会有这么多？','Zěnme huì yǒu zhème duō?','Nasıl bu kadar çok olabilir?'),
 'days':('大概几天能到？','Dàgài jǐ tiān néng dào?','Yaklaşık kaç günde ulaşır?'),
 'price':('这个价格可以接受。','Zhège jiàgé kěyǐ jiēshòu.','Bu fiyat kabul edilebilir.'),
 'progress':('老师说他进步很大。','Lǎoshī shuō tā jìnbù hěn dà.','Öğretmen onun çok ilerlediğini söyledi.'),
 'problem':('这个问题不难解决。','Zhège wèntí bù nán jiějué.','Bu sorunu çözmek zor değil.'),
 'step':('我们一步一步来。','Wǒmen yí bù yí bù lái.','Adım adım ilerleyelim.'),
 'style':('这个样子更适合你。','Zhège yàngzi gèng shìhé nǐ.','Bu görünüm sana daha uygun.'),
 'taste':('现在味道好多了。','Xiànzài wèidào hǎo duō le.','Şimdi tadı çok daha iyi.'),
 'opinion':('我想听听你的意见。','Wǒ xiǎng tīngting nǐ de yìjiàn.','Fikrini duymak istiyorum.'),
 'budget':('这个月的预算有点紧。','Zhège yuè de yùsuàn yǒudiǎn jǐn.','Bu ayın bütçesi biraz sıkışık.'),
 'cost':('这个费用比我想的高。','Zhège fèiyòng bǐ wǒ xiǎng de gāo.','Bu masraf düşündüğümden daha yüksek.'),
 'life':('现在的生活越来越稳定了。','Xiànzài de shēnghuó yuèláiyuè wěndìng le.','Şimdiki hayat giderek daha düzenli oluyor.'),
 'direction':('我不太确定方向。','Wǒ bú tài quèdìng fāngxiàng.','Yönden pek emin değilim.'),
 'review':('今天经理要做工作评价。','Jīntiān jīnglǐ yào zuò gōngzuò píngjià.','Bugün müdür iş değerlendirmesi yapacak.'),
 'strength':('这是你的一个优点。','Zhè shì nǐ de yí ge yōudiǎn.','Bu senin güçlü yönlerinden biri.'),
 'hobby':('我们有一样的爱好。','Wǒmen yǒu yíyàng de àihào.','Aynı hobilere sahibiz.'),
 'weight':('咪咪的体重有点高。','Mīmī de tǐzhòng yǒudiǎn gāo.','Mimi’nin kilosu biraz yüksek.'),
 'planword':('这个计划很实际。','Zhège jìhuà hěn shíjì.','Bu plan oldukça gerçekçi.'),
 'event':('今天社区有一个活动。','Jīntiān shèqū yǒu yí ge huódòng.','Bugün mahallede bir etkinlik var.'),
 'meaning':('我明白你的意思了。','Wǒ míngbai nǐ de yìsi le.','Ne demek istediğini anladım.'),
 'performance':('学校的演出快开始了。','Xuéxiào de yǎnchū kuài kāishǐ le.','Okul gösterisi başlamak üzere.'),
 'year':('这一年我们经历了很多事。','Zhè yì nián wǒmen jīnglì le hěn duō shì.','Bu yıl birçok şey yaşadık.'),
 'hope':('我希望大家都越来越好。','Wǒ xīwàng dàjiā dōu yuèláiyuè hǎo.','Umarım herkes giderek daha iyi olur.'),
 'fresh':('这些菜特别新鲜。','Zhèxiē cài tèbié xīnxiān.','Bu sebzeler çok taze.'),
 'late':('今天差一点迟到。','Jīntiān chà yìdiǎn chídào.','Bugün neredeyse geç kalıyordum.'),
 'pretty':('这个礼物很漂亮。','Zhège lǐwù hěn piàoliang.','Bu hediye çok güzel.'),
 'useful':('这个东西很有用。','Zhège dōngxi hěn yǒuyòng.','Bu şey çok kullanışlı.'),
 'short':('我想再短一点。','Wǒ xiǎng zài duǎn yìdiǎn.','Biraz daha kısa istiyorum.'),
 'long':('这个有点长。','Zhège yǒudiǎn cháng.','Bu biraz uzun.'),
 'salty':('这个菜有点咸。','Zhège cài yǒudiǎn xián.','Bu yemek biraz tuzlu.'),
 'dark':('屋里太黑了。','Wūli tài hēi le.','Evin içi çok karanlık.'),
 'bigger':('我想试大一点的。','Wǒ xiǎng shì dà yìdiǎn de.','Biraz daha büyüğünü denemek istiyorum.'),
 'smaller':('有没有小一点的？','Yǒu méiyǒu xiǎo yìdiǎn de?','Biraz daha küçüğü var mı?'),
 'sick':('他今天生病了。','Tā jīntiān shēngbìng le.','O bugün hasta.'),
 'better':('今天感觉好一点了吗？','Jīntiān gǎnjué hǎo yìdiǎn le ma?','Bugün biraz daha iyi hissediyor musun?'),
 'funny':('这个电影真的很好笑。','Zhège diànyǐng zhēn de hěn hǎoxiào.','Bu film gerçekten çok komik.'),
 'interesting':('这个故事很有意思。','Zhège gùshi hěn yǒuyìsi.','Bu hikâye çok ilginç.'),
 'necessary':('这个现在不是很必要。','Zhège xiànzài bú shì hěn bìyào.','Bu şu anda çok gerekli değil.'),
 'scared':('别害怕，我在这里。','Bié hàipà, wǒ zài zhèlǐ.','Korkma, ben buradayım.'),
 'okay':('没关系，我们再试一次。','Méi guānxi, wǒmen zài shì yí cì.','Sorun değil, tekrar deneyelim.'),
 'fat':('咪咪最近有点胖。','Mīmī zuìjìn yǒudiǎn pàng.','Mimi son zamanlarda biraz kilolu.'),
 'warm':('春天的天气很暖和。','Chūntiān de tiānqì hěn nuǎnhuo.','İlkbaharda hava çok ılık.'),
 'happy':('大家今天都很开心。','Dàjiā jīntiān dōu hěn kāixīn.','Bugün herkes çok mutlu.'),
 'cleanliness':('这里现在很干净。','Zhèlǐ xiànzài hěn gānjìng.','Burası şimdi çok temiz.'),
 'nervous':('别紧张，慢慢说。','Bié jǐnzhāng, mànmàn shuō.','Gerilme, yavaşça konuş.'),
 'jin':('这个我要两斤。','Zhège wǒ yào liǎng jīn.','Bundan bir kilo istiyorum.'),
 'minute':('还要十分钟。','Hái yào shí fēnzhōng.','On dakika daha gerekiyor.'),
 'peoplecount':('一共几个人？','Yígòng jǐ ge rén?','Toplam kaç kişi?'),
 'portion':('我们要准备二十份。','Wǒmen yào zhǔnbèi èrshí fèn.','Yirmi porsiyon hazırlamamız gerekiyor.'),
 'size':('这个尺码不太合适。','Zhège chǐmǎ bú tài héshì.','Bu beden pek uygun değil.'),
 'distance':('这个距离不算远。','Zhège jùlí bú suàn yuǎn.','Bu mesafe çok uzak sayılmaz.'),
 'color':('你喜欢什么颜色？','Nǐ xǐhuan shénme yánsè?','Hangi rengi seviyorsun?'),
 'inside':('里面还有东西。','Lǐmiàn hái yǒu dōngxi.','İçinde hâlâ bir şeyler var.'),
 'upstairs':('它跑到楼上了。','Tā pǎo dào lóushàng le.','O üst kata kaçtı.'),
 'downstairs':('我们去楼下看看。','Wǒmen qù lóuxià kànkan.','Alt kata gidip bakalım.'),
 'large':('我要大一点的。','Wǒ yào dà yìdiǎn de.','Biraz daha büyüğünü istiyorum.'),
 'small':('有没有小一点的？','Yǒu méiyǒu xiǎo yìdiǎn de?','Biraz daha küçüğü var mı?'),
 'enough':('这些已经够了。','Zhèxiē yǐjīng gòu le.','Bunlar artık yeterli.'),
 'lack':('现在还差一点。','Xiànzài hái chà yìdiǎn.','Şimdi hâlâ biraz eksik var.'),
 'firststep':('第一步先检查这里。','Dì yí bù xiān jiǎnchá zhèlǐ.','İlk adımda önce burayı kontrol edelim.'),
 'same':('我们的爱好很像。','Wǒmen de àihào hěn xiàng.','Hobilerimiz birbirine çok benziyor.'),
 'often':('我们常常一起学习。','Wǒmen chángcháng yìqǐ xuéxí.','Sık sık birlikte ders çalışıyoruz.'),
 'polite':('别客气，随便坐。','Bié kèqi, suíbiàn zuò.','Çekinme, rahatça otur.'),
 'sorry':('对不起，是我弄错了。','Duìbuqǐ, shì wǒ nòng cuò le.','Özür dilerim, ben yanlış yaptım.'),
 'thanks':('谢谢你来帮忙。','Xièxie nǐ lái bāngmáng.','Yardıma geldiğin için teşekkürler.'),
 'welcome':('欢迎来我们家。','Huānyíng lái wǒmen jiā.','Evimize hoş geldin.'),
 'together':('我们一起做吧。','Wǒmen yìqǐ zuò ba.','Birlikte yapalım.'),
 'again':('请再说一次。','Qǐng zài shuō yí cì.','Lütfen bir kez daha söyle.'),
 'attention':('这个地方要特别注意。','Zhège dìfang yào tèbié zhùyì.','Bu noktaya özellikle dikkat etmek gerekiyor.'),
 'remember':('记得把东西带上。','Jìde bǎ dōngxi dài shàng.','Eşyaları yanına almayı unutma.'),
 'cheer':('加油，你可以的！','Jiāyóu, nǐ kěyǐ de!','Haydi, yapabilirsin!'),
 'delicious':('这个真的很好吃。','Zhège zhēn de hěn hǎochī.','Bu gerçekten çok lezzetli.'),
 'come':('他们马上就来。','Tāmen mǎshàng jiù lái.','Birazdan geliyorlar.'),
 'find':('我终于找到了。','Wǒ zhōngyú zhǎodào le.','Sonunda buldum.'),
 'arrive':('大概三天能到。','Dàgài sān tiān néng dào.','Yaklaşık üç günde ulaşır.'),
 'win':('我们今天赢了比赛。','Wǒmen jīntiān yíng le bǐsài.','Bugünkü maçı kazandık.'),
 'lose':('输了也没关系。','Shū le yě méi guānxi.','Kaybetsek de sorun değil.'),
 'need':('这个我们确实需要。','Zhège wǒmen quèshí xūyào.','Buna gerçekten ihtiyacımız var.'),
 'bloom':('公园里的花都开了。','Gōngyuán lǐ de huā dōu kāi le.','Parktaki çiçeklerin hepsi açtı.'),
 'fall':('他刚才摔倒了。','Tā gāngcái shuāidǎo le.','Az önce düştü.'),
 'fallout':('他的牙刚刚掉了。','Tā de yá gānggāng diào le.','Dişi az önce düştü.'),
 'misunderstand':('我们之间有一点误会。','Wǒmen zhījiān yǒu yìdiǎn wùhuì.','Aramızda küçük bir yanlış anlaşılma var.'),
 'makeup':('说清楚以后就和好了。','Shuō qīngchu yǐhòu jiù héhǎo le.','Açıklığa kavuşturunca barıştılar.'),
 'went':('这个地方我们以前去过。','Zhège dìfang wǒmen yǐqián qùguo.','Bu yere daha önce gitmiştik.'),
 'rain':('外面正在下雨。','Wàimiàn zhèngzài xiàyǔ.','Dışarıda yağmur yağıyor.'),
 'sport':('我最近常常运动。','Wǒ zuìjìn chángcháng yùndòng.','Son zamanlarda sık sık spor yapıyorum.'),
 'music':('雨桐很喜欢音乐。','Yǔtóng hěn xǐhuan yīnyuè.','Yutong müziği çok seviyor.'),
 'birthday':('明天是邻居的生日。','Míngtiān shì línjū de shēngrì.','Yarın komşunun doğum günü.'),
 'match':('比赛马上开始了。','Bǐsài mǎshàng kāishǐ le.','Maç birazdan başlayacak.'),
 'festival':('节日快到了。','Jiérì kuài dào le.','Bayram yaklaşıyor.'),
 'parentmeeting':('今天学校开家长会。','Jīntiān xuéxiào kāi jiāzhǎnghuì.','Bugün okulda veli toplantısı var.'),
 'picnic':('周末我们去公园野餐。','Zhōumò wǒmen qù gōngyuán yěcān.','Hafta sonu parkta piknik yapacağız.'),
 'powercut':('刚才突然停电了。','Gāngcái tūrán tíngdiàn le.','Az önce birden elektrik kesildi.'),
 'overtime':('张伟今天要加班。','Zhāng Wěi jīntiān yào jiābān.','Zhang Wei bugün fazla mesai yapacak.'),
 'video':('我们晚上视频吧。','Wǒmen wǎnshang shìpín ba.','Akşam görüntülü konuşalım.'),
 'haircut':('我今天去理发。','Wǒ jīntiān qù lǐfà.','Bugün saçımı kestirmeye gidiyorum.'),
 'wrongstop':('我刚才下错站了。','Wǒ gāngcái xià cuò zhàn le.','Az önce yanlış durakta indim.'),
 'wrongfile':('我刚才发错文件了。','Wǒ gāngcái fā cuò wénjiàn le.','Az önce yanlış dosyayı gönderdim.'),
 'latehome':('我今天会晚一点回家。','Wǒ jīntiān huì wǎn yìdiǎn huí jiā.','Bugün eve biraz geç döneceğim.'),
 'bringfood':('我们给他们送点饭。','Wǒmen gěi tāmen sòng diǎn fàn.','Onlara biraz yemek götürelim.'),
 'lostbag':('我的包好像丢了。','Wǒ de bāo hǎoxiàng diū le.','Sanırım çantam kayboldu.'),
 'lostfound':('我们去失物招领处问问。','Wǒmen qù shīwù zhāolǐng chù wènwen.','Kayıp eşya bürosuna gidip soralım.')
}


SPECIAL_USAGE.update({
 'forget':('我们忘了带吃的。','Wǒmen wàng le dài chī de.','Yiyecek getirmeyi unuttuk.'),
 'see':('你们看得见吗？','Nǐmen kàn de jiàn ma?','Görebiliyor musunuz?'),
 'hear':('你们听得见吗？','Nǐmen tīng de jiàn ma?','Duyabiliyor musunuz?'),
 'remember2':('你还记得这张照片吗？','Nǐ hái jìde zhè zhāng zhàopiàn ma?','Bu fotoğrafı hâlâ hatırlıyor musun?'),
 'improve':('这个地方以后还可以提高。','Zhège dìfang yǐhòu hái kěyǐ tígāo.','Bu alan ileride daha da geliştirilebilir.'),
 'retry':('我们再试一次。','Wǒmen zài shì yí cì.','Bir kez daha deneyelim.'),
 'cook':('我们先把饭做好。','Wǒmen xiān bǎ fàn zuò hǎo.','Önce yemeği hazırlayalım.'),
})


def usage_line(key):
    if key in SPECIAL_USAGE:
        return SPECIAL_USAGE[key]
    zh,py,tr=W[key]
    if key in ACTION_KEYS:
        return (f'我们先{zh}。',f'Wǒmen xiān {py}.',f'Önce {tr}.')
    if key in PLACE_KEYS:
        return (f'{zh}离这里不远。',f'{py.capitalize()} lí zhèlǐ bù yuǎn.',f'{cap(tr)} buradan uzak değil.')
    if key in PERSON_KEYS:
        return (f'{zh}今天也来了。',f'{py.capitalize()} jīntiān yě lái le.',f'{cap(tr)} bugün de geldi.')
    if key in STATE_KEYS:
        return (f'现在感觉{zh}多了。',f'Xiànzài gǎnjué {py} duō le.',f'Şimdi çok daha {tr} hissediliyor.')
    if key in ABSTRACT_KEYS:
        return (f'我们来谈谈{zh}。',f'Wǒmen lái tántan {py}.',f'{cap(tr)} hakkında konuşalım.')
    # Concrete noun / item.
    return (f'这个{zh}在这里。',f'Zhège {py} zài zhèlǐ.',f'Bu {tr} burada.')


def make_dialogues(n):
    roles=ROLES[n]
    setup,problem,resolution=B[n]
    keys=V[n]
    lines=[]
    # Setup and vocabulary introduction.
    lines += [setup,('今天事情不少。','Jīntiān shìqing bù shǎo.','Bugün yapılacak epey iş var.'),('我们先看看最重要的。','Wǒmen xiān kànkan zuì zhòngyào de.','Önce en önemli olana bakalım.'),('好，慢慢来。','Hǎo, mànmàn lái.','Tamam, sakin sakin ilerleyelim.')]
    early_responses=[
      (('我明白了。','Wǒ míngbai le.','Anladım.'),('原来是这样。','Yuánlái shì zhèyàng.','Demek böyleymiş.')),
      (('这个我记住了。','Zhège wǒ jìzhù le.','Bunu aklımda tutacağım.'),('听起来很清楚。','Tīng qǐlái hěn qīngchu.','Oldukça net görünüyor.')),
      (('好，那就按这个来。','Hǎo, nà jiù àn zhège lái.','Tamam, o zaman buna göre ilerleyelim.'),('我觉得可以。','Wǒ juéde kěyǐ.','Bence olur.')),
      (('对，这个很重要。','Duì, zhège hěn zhòngyào.','Evet, bu önemli.'),('我们别忘了。','Wǒmen bié wàng le.','Bunu unutmayalım.'))]
    for idx,k in enumerate(keys[:4]):
        lines += [usage_line(k), early_responses[idx][0], early_responses[idx][1]]
    # Complication.
    lines += [problem,('那现在怎么办？','Nà xiànzài zěnme bàn?','Peki şimdi ne yapacağız?'),('先别着急，我们想个办法。','Xiān bié zháojí, wǒmen xiǎng ge bànfǎ.','Önce telaşlanmayalım, bir çözüm düşünelim.'),('我觉得可以先做最简单的。','Wǒ juéde kěyǐ xiān zuò zuì jiǎndān de.','Bence önce en kolay kısmı yapabiliriz.'),('这样比较快。','Zhèyàng bǐjiào kuài.','Böyle daha hızlı olur.')]
    late_responses=[
      (('对，这个也要注意。','Duì, zhège yě yào zhùyì.','Evet, buna da dikkat etmek gerekiyor.'),('那我们把它记下来。','Nà wǒmen bǎ tā jìxiàlái.','O zaman bunu not edelim.')),
      (('这个办法不错。','Zhège bànfǎ búcuò.','Bu yöntem fena değil.'),('我们可以试试。','Wǒmen kěyǐ shìshi.','Deneyebiliriz.')),
      (('我以前没注意到。','Wǒ yǐqián méi zhùyì dào.','Daha önce dikkat etmemiştim.'),('现在知道了。','Xiànzài zhīdào le.','Şimdi öğrendim.')),
      (('说得对。','Shuō de duì.','Doğru söylüyorsun.'),('这样更方便。','Zhèyàng gèng fāngbiàn.','Böyle daha kullanışlı.'))]
    for idx,k in enumerate(keys[4:8]):
        lines += [usage_line(k), late_responses[idx][0], late_responses[idx][1]]
    # HSK2 connective language and problem solving.
    bridge=[
      ('因为时间不多，所以我们快一点。','Yīnwèi shíjiān bù duō, suǒyǐ wǒmen kuài yìdiǎn.','Zaman az olduğu için biraz hızlı olalım.'),
      ('先做这个，再做下一个。','Xiān zuò zhège, zài zuò xià yí ge.','Önce bunu, sonra sıradakini yapalım.'),
      ('这个办法比刚才的好。','Zhège bànfǎ bǐ gāngcái de hǎo.','Bu yöntem az öncekinden daha iyi.'),
      ('我已经试过一次了。','Wǒ yǐjīng shìguo yí cì le.','Bir kez denedim bile.'),
      ('那我们换一个办法。','Nà wǒmen huàn yí ge bànfǎ.','O zaman başka bir yöntem deneyelim.'),
      ('可以，你先来。','Kěyǐ, nǐ xiān lái.','Olur, önce sen yap.'),
      ('做完以后告诉我。','Zuò wán yǐhòu gàosu wǒ.','Bitirince bana söyle.'),
      ('没问题，我记得。','Méi wèntí, wǒ jìde.','Sorun yok, hatırlıyorum.'),
      ('现在好多了。','Xiànzài hǎo duō le.','Şimdi çok daha iyi.'),
      ('还差一点。','Hái chà yìdiǎn.','Biraz daha eksik var.'),
      ('我来帮你吧。','Wǒ lái bāng nǐ ba.','Sana yardım edeyim.'),
      ('谢谢，这样快多了。','Xièxie, zhèyàng kuài duō le.','Teşekkürler, böyle çok daha hızlı.'),
      ('我们再检查一次。','Wǒmen zài jiǎnchá yí cì.','Bir kez daha kontrol edelim.'),
      ('这次没有问题了。','Zhè cì méiyǒu wèntí le.','Bu kez sorun kalmadı.'),
      ('太好了，终于解决了。','Tài hǎo le, zhōngyú jiějué le.','Harika, sonunda çözüldü.'),
      ('今天又学到一件事。','Jīntiān yòu xuédào yí jiàn shì.','Bugün yine bir şey öğrendik.'),
      ('下次我们会更有经验。','Xià cì wǒmen huì gèng yǒu jīngyàn.','Bir dahaki sefere daha deneyimli olacağız.'),
      ('我也是这么想的。','Wǒ yě shì zhème xiǎng de.','Ben de böyle düşünüyorum.'),
      ('那就这么决定吧。','Nà jiù zhème juédìng ba.','O zaman böyle karar verelim.'),
      ('好，我们继续。','Hǎo, wǒmen jìxù.','Tamam, devam edelim.')
    ]
    lines += bridge
    # Recycle vocabulary with the natural usage lines and varied responses.
    responses=[('对，我记住了。','Duì, wǒ jìzhù le.','Evet, aklımda.'),('这个很实用。','Zhège hěn shíyòng.','Bu çok kullanışlı.'),('以后还会用到。','Yǐhòu hái huì yòngdào.','Bunu ileride yine kullanacağız.'),('我再说一次。','Wǒ zài shuō yí cì.','Bir kez daha söyleyeyim.'),('现在更清楚了。','Xiànzài gèng qīngchu le.','Şimdi daha net.')]
    cycle=0
    while len(lines)<94:
        k=keys[cycle % len(keys)]
        lines += [usage_line(k), responses[cycle % len(responses)]]
        cycle += 1
    lines=lines[:94]
    lines += [resolution,('问题解决了。','Wèntí jiějué le.','Sorun çözüldü.'),('大家都轻松多了。','Dàjiā dōu qīngsōng duō le.','Herkes çok daha rahatladı.'),('今天很顺利。','Jīntiān hěn shùnlì.','Bugün işler yolunda gitti.'),('下次会更容易。','Xià cì huì gèng róngyì.','Bir dahaki sefere daha kolay olacak.'),('好，我们回去吧。','Hǎo, wǒmen huíqù ba.','Tamam, geri dönelim.')]
    return [{'id':f'DLG_ZH_HSK2_SC{n:03d}_{i:03d}','speaker':roles[(i-1)%len(roles)],'zh':zh,'pinyin':py,'tr':tr} for i,(zh,py,tr) in enumerate(lines[:100],1)]


def card_example(key):
    return usage_line(key)

def make_cards(n):
    cards=[]
    for i,key in enumerate(V[n],1):
        zh,py,tr=W[key]; ezh,epy,etr=card_example(key)
        cards.append({'id':f'VOC_ZH_HSK2_SC{n:03d}_{i:03d}','zh':zh,'pinyin':py,'tr':tr,'exampleZh':ezh,'examplePinyin':epy,'exampleTr':etr,'kind':'active' if i<=6 else 'review'})
    return cards

def grammar_pack(n, keys):
    a,b,c=[W[k] for k in keys[:3]]
    mode=(n-1)%5
    if mode==0:
        return [
          {'type':'word_order','tokens':['我们','先',a[0],'再',b[0]],'answerTokens':['我们','先',a[0],'再',b[0]]},
          {'type':'fill_blank','blankSentenceZh':'我们先___，再继续。','options':[a[0],b[0],c[0]],'answer':a[0]},
          {'type':'sentence_repair','tokens':['再',b[0],'先',a[0]],'answerTokens':['先',a[0],'再',b[0]]}]
    if mode==1:
        return [
          {'type':'word_order','tokens':['因为',a[0],'所以',b[0]],'answerTokens':['因为',a[0],'所以',b[0]]},
          {'type':'fill_blank','blankSentenceZh':'因为时间不多，___我们快一点。','options':['所以','但是','还是'],'answer':'所以'},
          {'type':'sentence_repair','tokens':['所以','我们','因为','要准备'], 'answerTokens':['因为','要准备','所以','我们']}]
    if mode==2:
        return [
          {'type':'word_order','tokens':[a[0],'比',b[0],'更好'], 'answerTokens':[a[0],'比',b[0],'更好']},
          {'type':'fill_blank','blankSentenceZh':f'{a[0]}比{b[0]}___一点。','options':['好','先','已经'],'answer':'好'},
          {'type':'sentence_repair','tokens':['更好',b[0],'比',a[0]],'answerTokens':[a[0],'比',b[0],'更好']}]
    if mode==3:
        return [
          {'type':'word_order','tokens':['我','已经',a[0],'了'], 'answerTokens':['我','已经',a[0],'了']},
          {'type':'fill_blank','blankSentenceZh':'我___准备好了。','options':['已经','因为','再'],'answer':'已经'},
          {'type':'sentence_repair','tokens':['了','已经','我们','准备好'], 'answerTokens':['我们','已经','准备好','了']}]
    return [
      {'type':'word_order','tokens':['可以',a[0],'吗'], 'answerTokens':['可以',a[0],'吗']},
      {'type':'fill_blank','blankSentenceZh':f'我们需要___{a[0]}。','options':['先','比','已经'],'answer':'先'},
      {'type':'sentence_repair','tokens':['吗',a[0],'可以'], 'answerTokens':['可以',a[0],'吗']}]

def make_exercises(n):
    base=grammar_pack(n,V[n])
    out=[]
    for i in range(9):
        item=dict(base[i%3]); item['id']=f'SENT_ZH_HSK2_SC{n:03d}_{i+1:03d}'; item['promptTr']={'word_order':'Kelimeleri doğru sıraya koy.','fill_blank':'Boşluğu doğru kelimeyle doldur.','sentence_repair':'Yanlış sıradaki cümleyi düzelt.'}[item['type']]
        out.append(item)
    return out

def make_comprehension(n,scene):
    return [
      {'id':f'COMP_ZH_HSK2_SC{n:03d}_001','questionTr':'Sahnenin ana olayı hangisidir?','optionsTr':[scene['titleTr'],'Bir havaalanı yolculuğu','Bir tarih dersi'],'correctIndex':0},
      {'id':f'COMP_ZH_HSK2_SC{n:03d}_002','questionTr':'Karakterler sahnede günlük bir problemi çözmeye çalışıyor mu?','optionsTr':['Evet','Hayır','Belli değil'],'correctIndex':0},
      {'id':f'COMP_ZH_HSK2_SC{n:03d}_003','questionTr':'Sahne sonunda ana sorun çözülüyor mu?','optionsTr':['Evet','Hayır','Sahne yarım kalıyor'],'correctIndex':0},
      {'id':f'COMP_ZH_HSK2_SC{n:03d}_004','questionTr':'Bu sahne hangi büyük hikâyenin parçasıdır?','optionsTr':['Zhang ailesinin yeni kasabadaki ilk yılı','Bir bilim kurgu macerası','Bir spor ligi'],'correctIndex':0},
      {'id':f'COMP_ZH_HSK2_SC{n:03d}_005','questionTr':'Sahnede neden-sonuç veya sıralama dili kullanılıyor mu?','optionsTr':['Evet','Hayır','Sadece sayılar var'],'correctIndex':0}
    ]

def make_pron(n,cards):
    return [{'id':f'PRON_ZH_HSK2_SC{n:03d}_{i:03d}','zh':c['exampleZh'],'pinyin':c['examplePinyin'],'tr':c['exampleTr'],'scoring':['pronunciation','toneAccuracy','fluency','timing','completeness']} for i,c in enumerate(cards[:5],1)]

def make_interactive(n):
    a,b,c=[W[k] for k in V[n][:3]]
    return [
      {'id':f'INT_ZH_HSK2_SC{n:03d}_001','promptZh':'现在怎么办？','promptPinyin':'Xiànzài zěnme bàn?','promptTr':'Şimdi ne yapacağız?','options':[{'zh':'我们先想个办法。','tr':'Önce bir çözüm düşünelim.','correct':True},{'zh':'昨天是星期三。','tr':'Dün çarşambaydı.','correct':False},{'zh':'我有两本书。','tr':'İki kitabım var.','correct':False}]},
      {'id':f'INT_ZH_HSK2_SC{n:03d}_002','promptZh':f'这个{a[0]}怎么样？','promptPinyin':f'Zhège {a[1]} zěnmeyàng?','promptTr':f'Bu {a[2]} nasıl?','options':[{'zh':'我觉得不错。','tr':'Bence fena değil.','correct':True},{'zh':'我叫张伟。','tr':'Benim adım Zhang Wei.','correct':False},{'zh':'在二楼。','tr':'İkinci katta.','correct':False}]},
      {'id':f'INT_ZH_HSK2_SC{n:03d}_003','promptZh':'为什么？','promptPinyin':'Wèishénme?','promptTr':'Neden?','options':[{'zh':'因为这样更方便。','tr':'Çünkü böyle daha kullanışlı.','correct':True},{'zh':'三个人。','tr':'Üç kişi.','correct':False},{'zh':'红色的。','tr':'Kırmızı olan.','correct':False}]},
      {'id':f'INT_ZH_HSK2_SC{n:03d}_004','promptZh':'准备好了吗？','promptPinyin':'Zhǔnbèi hǎo le ma?','promptTr':'Hazır mısın?','options':[{'zh':'已经准备好了。','tr':'Çoktan hazırım.','correct':True},{'zh':'比昨天。','tr':'Dünden daha.','correct':False},{'zh':'在银行。','tr':'Bankada.','correct':False}]}
    ]

def make_production(n,scene):
    return {'scenePurposeTr':scene.get('miniAdventureTr',''),'timeOfDay':'day' if n not in (6,16,20,41,42,50) else 'evening','atmosphere':'sıcak, doğal, gündelik ve HSK2 seviyesine uygun','characters':ROLES[n],'locationId':scene.get('locationId',''),'visual':{'reuseLocation':True,'newVisualRequired':False,'style':'visual_novel_theatre'},'audio':{'voiceLanguage':'zh-CN','narratorProfile':'NARRATOR_ZH_001','defaultSpeechSpeed':0.85},'animation':{'level':'minimal','mouthMode':'AUTO_SIMPLE','blink':True,'speakerFocus':True},'continuityNoteTr':f"{scene['titleTr']} olayı Zhang ailesinin yeni kasabadaki ilk yılı içinde HSK2 sahne {n} olarak kaydedilir."}

def main():
    data=json.loads(PATH.read_text(encoding='utf-8'))
    assert len(data['scenes'])==50
    for scene in data['scenes']:
        n=scene['number']; cards=make_cards(n); learning=dict(scene.get('learning') or {})
        learning.update({'vocabularyCards':cards,'sentenceExercises':make_exercises(n),'comprehensionQuestions':make_comprehension(n,scene),'pronunciationItems':make_pron(n,cards),'interactiveDialogue':make_interactive(n),'examRules':{'vocabularyPassPercent':90,'sentencePassPercent':85,'lockNextSceneUntilPassed':True},'examStages':[{'stage':1,'type':'vocabulary','passPercent':90},{'stage':2,'type':'sentence','passPercent':85,'requiresStage':1}],'flashCardPolicy':{'allowPrevious':True,'allowNext':True,'allowFavorite':True,'favoritesStudyMode':True}})
        scene['learning']=learning; scene['dialogues']=make_dialogues(n); scene['production']=make_production(n,scene); scene['complete']=True; scene['productionStatus']='complete'; scene['editorialStatus']='generated_full_v1_requires_native_review'; scene['dialogueCount']=len(scene['dialogues'])
    data['schemaVersion']=3; data['completeSceneCount']=50; data['editorialNoteTr']='HSK2 50 sahne veri olarak tamdır; yayın/ticari kullanım öncesi ana dili Mandarin olan editör kontrolü önerilir.'
    PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('HSK2 authoring completed:',len(data['scenes']),'scenes,',sum(len(s['dialogues']) for s in data['scenes']),'dialogues')
if __name__=='__main__': main()
