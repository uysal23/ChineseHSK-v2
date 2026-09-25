#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a complete HSK1 authoring payload for all 50 scenes.

The output is deterministic and lives in authoring/hsk1_blueprints.json so the
Android assets can always be regenerated from a single source of truth.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'authoring' / 'hsk1_blueprints.json'

# Compact beginner lexicon used for flashcards and controlled dialogue generation.
# key: (Simplified Chinese, tone-marked Hanyu Pinyin, Turkish)
W = {
'box':('箱子','xiāngzi','kutu / koli'),'move':('搬家','bānjiā','taşınmak'),'ticket':('火车票','huǒchēpiào','tren bileti'),
'bag':('包','bāo','çanta'),'station':('车站','chēzhàn','istasyon'),'platform':('站台','zhàntái','peron'),
'left':('左边','zuǒbian','sol taraf'),'right':('右边','yòubian','sağ taraf'),'train':('火车','huǒchē','tren'),
'bread':('面包','miànbāo','ekmek'),'water':('水','shuǐ','su'),'tea':('茶','chá','çay'),'cup':('杯子','bēizi','bardak'),
'toy':('玩具','wánjù','oyuncak'),'seat':('座位','zuòwèi','koltuk / oturma yeri'),'city':('城市','chéngshì','şehir'),
'school':('学校','xuéxiào','okul'),'home':('家','jiā','ev'),'phone':('电话','diànhuà','telefon'),'address':('地址','dìzhǐ','adres'),
'name':('名字','míngzi','isim'),'friend':('朋友','péngyou','arkadaş'),'taxi':('出租车','chūzūchē','taksi'),'road':('路','lù','yol'),
'number':('号码','hàomǎ','numara'),'door':('门','mén','kapı'),'key':('钥匙','yàoshi','anahtar'),'room':('房间','fángjiān','oda'),
'kitchen':('厨房','chúfáng','mutfak'),'living':('客厅','kètīng','salon'),'cat':('猫','māo','kedi'),'cabinet':('柜子','guìzi','dolap'),
'neighbor':('邻居','línjū','komşu'),'supermarket':('超市','chāoshì','süpermarket'),'apple':('苹果','píngguǒ','elma'),
'milk':('牛奶','niúnǎi','süt'),'egg':('鸡蛋','jīdàn','yumurta'),'money':('钱','qián','para'),'yuan':('元','yuán','yuan'),
'breakfast':('早饭','zǎofàn','kahvaltı'),'photo':('照片','zhàopiàn','fotoğraf'),'highschool':('高中','gāozhōng','lise'),
'classroom':('教室','jiàoshì','sınıf'),'student':('学生','xuésheng','öğrenci'),'teacher':('老师','lǎoshī','öğretmen'),
'class':('班','bān','sınıf / şube'),'lunch':('午饭','wǔfàn','öğle yemeği'),'pencil':('铅笔','qiānbǐ','kurşun kalem'),
'blue':('蓝色','lánsè','mavi renk'),'red':('红色','hóngsè','kırmızı renk'),'job':('工作','gōngzuò','iş'),
'phone_number':('电话号码','diànhuà hàomǎ','telefon numarası'),'tomorrow':('明天','míngtiān','yarın'),'clothes':('衣服','yīfu','kıyafet'),
'shirt':('衬衫','chènshān','gömlek'),'interview':('面试','miànshì','iş görüşmesi'),'card':('卡','kǎ','kart'),
'colleague':('同事','tóngshì','iş arkadaşı'),'menu':('菜单','càidān','menü'),'food':('饭','fàn','yemek'),
'bus':('公交车','gōngjiāochē','otobüs'),'guest':('客人','kèrén','misafir'),'park':('公园','gōngyuán','park'),
'weather':('天气','tiānqì','hava'),'tree':('树','shù','ağaç'),'icecream':('冰淇淋','bīngqílín','dondurma'),
'rain':('雨','yǔ','yağmur'),'umbrella':('雨伞','yǔsǎn','şemsiye'),'package':('包裹','bāoguǒ','paket / kargo'),
'vet':('兽医','shòuyī','veteriner'),'doctor':('医生','yīshēng','doktor'),'petshop':('宠物店','chǒngwùdiàn','pet mağazası'),
'catfood':('猫粮','māoliáng','kedi maması'),'exam':('考试','kǎoshì','sınav'),'study':('学习','xuéxí','ders çalışma / öğrenme'),
'drawing':('画','huà','resim'),'mother':('妈妈','māma','anne'),'father':('爸爸','bàba','baba'),'salary':('工资','gōngzī','maaş'),
'evening':('晚上','wǎnshang','akşam'),'cake':('蛋糕','dàngāo','kek / pasta'),'idea':('想法','xiǎngfa','fikir'),
'community':('社区','shèqū','mahalle / topluluk'),'activity':('活动','huódòng','etkinlik'),'new':('新的','xīn de','yeni'),
'old':('旧的','jiù de','eski'),'family':('家人','jiārén','aile'),'table':('桌子','zhuōzi','masa'),
'chair':('椅子','yǐzi','sandalye'),'book':('书','shū','kitap'),'window':('窗户','chuānghu','pencere'),
'car':('车','chē','araç'),'time':('时间','shíjiān','zaman'),'today':('今天','jīntiān','bugün'),
'coffee':('咖啡','kāfēi','kahve'),'juice':('果汁','guǒzhī','meyve suyu'),'rice':('米饭','mǐfàn','pirinç / pilav'),
'noodle':('面条','miàntiáo','erişte / noodle'),'ball':('球','qiú','top'),'bike':('自行车','zìxíngchē','bisiklet'),
'coat':('外套','wàitào','mont'),'shop':('商店','shāngdiàn','mağaza'),'hospital':('医院','yīyuàn','hastane'),
'office':('办公室','bàngōngshì','ofis'),'manager':('经理','jīnglǐ','müdür'),'computer':('电脑','diànnǎo','bilgisayar'),
'workcard':('工作卡','gōngzuò kǎ','iş kartı'),'soup':('汤','tāng','çorba'),'chicken':('鸡肉','jīròu','tavuk'),
'child':('孩子','háizi','çocuk'),'color':('颜色','yánsè','renk'),'medicine':('药','yào','ilaç'),'testpaper':('试卷','shìjuàn','sınav kâğıdı'),
'picture':('图片','túpiàn','resim / görsel'),'pay':('付款','fùkuǎn','ödeme'),'market':('市场','shìchǎng','pazar'),
'people':('人','rén','insan'),'three_months':('三个月','sān ge yuè','üç ay'),'newcity':('新城','xīnchéng','yeni şehir / kasaba')
}

# 50 scene-specific controlled vocabularies. The first six cards are active.
VOCAB = {
1:['box','move','home','room','kitchen','cat','book','door'],
2:['ticket','bag','train','today','family','door','time','cat'],
3:['station','platform','left','right','train','ticket','road','people'],
4:['breakfast','bread','water','tea','cup','train','money','yuan'],
5:['toy','seat','train','bag','cat','left','right','child'],
6:['city','school','home','road','park','new','people','train'],
7:['station','phone','address','time','car','train','people','today'],
8:['name','friend','family','station','city','phone','people','home'],
9:['taxi','address','road','number','city','right','left','home'],
10:['door','key','home','room','right','left','box','family'],
11:['box','room','kitchen','living','home','door','table','chair'],
12:['home','cat','room','table','chair','door','evening','family'],
13:['cat','cabinet','kitchen','table','chair','room','home','door'],
14:['neighbor','door','family','home','friend','name','tea','people'],
15:['tea','water','coffee','juice','cup','neighbor','table','guest'],
16:['supermarket','road','left','right','home','shop','neighbor','people'],
17:['supermarket','apple','milk','egg','bread','money','bag','food'],
18:['money','yuan','supermarket','pay','bag','apple','milk','bread'],
19:['breakfast','bread','milk','egg','tea','food','family','table'],
20:['photo','family','cat','chair','table','home','mother','father'],
21:['highschool','school','classroom','student','teacher','road','door','class'],
22:['classroom','student','teacher','class','name','friend','school','book'],
23:['friend','lunch','student','school','food','classroom','name','today'],
24:['school','teacher','student','child','mother','classroom','door','friend'],
25:['pencil','blue','red','student','teacher','classroom','book','bag'],
26:['job','phone','phone_number','friend','office','manager','computer','today'],
27:['phone','phone_number','tomorrow','time','job','interview','office','today'],
28:['clothes','shirt','blue','red','interview','job','home','today'],
29:['interview','job','manager','office','computer','card','name','today'],
30:['job','family','cake','evening','today','friend','home','food'],
31:['workcard','card','office','job','colleague','manager','computer','door'],
32:['colleague','job','office','name','city','friend','lunch','computer'],
33:['menu','lunch','food','rice','noodle','soup','chicken','water'],
34:['bus','time','road','home','today','station','phone','money'],
35:['guest','family','friend','food','tea','table','home','cake'],
36:['toy','child','friend','ball','home','family','chair','table'],
37:['park','weather','tree','family','child','ball','bike','today'],
38:['icecream','park','child','money','yuan','food','friend','today'],
39:['rain','umbrella','weather','coat','road','home','family','today'],
40:['package','address','neighbor','door','home','name','phone','number'],
41:['cat','vet','doctor','hospital','medicine','water','food','home'],
42:['petshop','catfood','cat','money','yuan','shop','bag','medicine'],
43:['exam','study','school','book','testpaper','teacher','today','evening'],
44:['drawing','family','mother','father','teacher','student','picture','school'],
45:['salary','money','evening','food','family','job','today','restaurant' if False else 'menu'],
46:['cake','food','neighbor','family','tea','home','friend','today'],
47:['idea','cake','job','friend','family','money','today','future' if False else 'new'],
48:['community','activity','friend','people','family','food','park','today'],
49:['three_months','newcity','old','new','home','school','job','friend'],
50:['home','family','friend','newcity','school','job','cake','park']
}

# Per-scene story focus: goal, complication, resolution.
# Each tuple is zh, pinyin, tr.
F = {
1:[('我们今天搬家。','Wǒmen jīntiān bānjiā.','Bugün taşınıyoruz.'),('这个箱子放错了。','Zhège xiāngzi fàng cuò le.','Bu kutu yanlış yere konmuş.'),('好了，箱子都对了。','Hǎo le, xiāngzi dōu duì le.','Tamam, kutular artık doğru yerde.')],
2:[('我们要去坐火车。','Wǒmen yào qù zuò huǒchē.','Trene binmeye gideceğiz.'),('乐乐的火车票不见了。','Lèlè de huǒchēpiào bú jiàn le.','Lele’nin tren bileti ortada yok.'),('找到了，在包里。','Zhǎodào le, zài bāo lǐ.','Bulduk, çantanın içindeymiş.')],
3:[('我们要找站台。','Wǒmen yào zhǎo zhàntái.','Peronu bulmamız gerekiyor.'),('我们走错了。','Wǒmen zǒu cuò le.','Yanlış yöne gittik.'),('对，站台在右边。','Duì, zhàntái zài yòubian.','Evet, peron sağ tarafta.')],
4:[('我们在火车上吃早饭。','Wǒmen zài huǒchē shàng chī zǎofàn.','Trende kahvaltı yapıyoruz.'),('乐乐不知道要吃什么。','Lèlè bù zhīdào yào chī shénme.','Lele ne yiyeceğini bilmiyor.'),('他要面包和牛奶。','Tā yào miànbāo hé niúnǎi.','Ekmek ve süt istiyor.')],
5:[('乐乐在找玩具。','Lèlè zài zhǎo wánjù.','Lele oyuncağını arıyor.'),('玩具不在包里。','Wánjù bú zài bāo lǐ.','Oyuncak çantada değil.'),('玩具在座位下面。','Wánjù zài zuòwèi xiàmiàn.','Oyuncak koltuğun altında.')],
6:[('我们快到新城了。','Wǒmen kuài dào Xīnchéng le.','Yeni kasabaya yaklaştık.'),('大家都想看外面。','Dàjiā dōu xiǎng kàn wàimian.','Herkes dışarıyı görmek istiyor.'),('新城很漂亮。','Xīnchéng hěn piàoliang.','Yeni kasaba çok güzel.')],
7:[('我们到新车站了。','Wǒmen dào xīn chēzhàn le.','Yeni istasyona geldik.'),('搬家公司的人还没来。','Bānjiā gōngsī de rén hái méi lái.','Nakliye şirketinden kimse henüz gelmedi.'),('我们先打电话等一下。','Wǒmen xiān dǎ diànhuà děng yíxià.','Önce telefon edip biraz bekleyelim.')],
8:[('李晨来帮我们。','Lǐ Chén lái bāng wǒmen.','Li Chen bize yardım etmeye geliyor.'),('我们还不认识他。','Wǒmen hái bù rènshi tā.','Onu henüz tanımıyoruz.'),('现在我们是朋友了。','Xiànzài wǒmen shì péngyou le.','Artık arkadaş olduk.')],
9:[('我们坐出租车去新家。','Wǒmen zuò chūzūchē qù xīn jiā.','Yeni eve taksiyle gidiyoruz.'),('司机听错了地址。','Sījī tīng cuò le dìzhǐ.','Şoför adresi yanlış duydu.'),('李晨说了正确的路。','Lǐ Chén shuō le zhèngquè de lù.','Li Chen doğru yolu söyledi.')],
10:[('我们到了新家。','Wǒmen dào le xīn jiā.','Yeni eve geldik.'),('这个钥匙打不开门。','Zhège yàoshi dǎbukāi mén.','Bu anahtar kapıyı açmıyor.'),('对的钥匙找到了。','Duì de yàoshi zhǎodào le.','Doğru anahtarı bulduk.')],
11:[('我们要放好箱子。','Wǒmen yào fàng hǎo xiāngzi.','Kutuları doğru yerlere koyacağız.'),('厨房的箱子在孩子的房间。','Chúfáng de xiāngzi zài háizi de fángjiān.','Mutfak kutusu çocuk odasında.'),('我们把箱子放回厨房。','Wǒmen bǎ xiāngzi fàng huí chúfáng.','Kutuyu yeniden mutfağa koyuyoruz.')],
12:[('这是我们在新家的第一个晚上。','Zhè shì wǒmen zài xīn jiā de dì yí ge wǎnshang.','Bu yeni evdeki ilk akşamımız.'),('咪咪不见了。','Mīmī bú jiàn le.','Mimi ortada yok.'),('我们一起找咪咪。','Wǒmen yìqǐ zhǎo Mīmī.','Mimi’yi birlikte arıyoruz.')],
13:[('我们还在找咪咪。','Wǒmen hái zài zhǎo Mīmī.','Mimi’yi hâlâ arıyoruz.'),('厨房里有声音。','Chúfáng lǐ yǒu shēngyīn.','Mutfaktan bir ses geliyor.'),('咪咪在柜子旁边。','Mīmī zài guìzi pángbiān.','Mimi dolabın yanında.')],
14:[('有人来敲门。','Yǒu rén lái qiāo mén.','Birisi kapıyı çalıyor.'),('我们不认识这个邻居。','Wǒmen bù rènshi zhège línjū.','Bu komşuyu tanımıyoruz.'),('大家互相介绍了。','Dàjiā hùxiāng jièshào le.','Herkes birbirine kendini tanıttı.')],
15:[('我们请邻居喝茶。','Wǒmen qǐng línjū hē chá.','Komşuya çay ikram ediyoruz.'),('她不知道喝茶还是水。','Tā bù zhīdào hē chá háishi shuǐ.','Çay mı su mu içeceğine karar veremiyor.'),('她要一杯茶。','Tā yào yì bēi chá.','Bir bardak çay istiyor.')],
16:[('我们要去超市。','Wǒmen yào qù chāoshì.','Süpermarkete gideceğiz.'),('我们不知道超市在哪儿。','Wǒmen bù zhīdào chāoshì zài nǎr.','Süpermarketin nerede olduğunu bilmiyoruz.'),('邻居告诉我们怎么走。','Línjū gàosu wǒmen zěnme zǒu.','Komşu bize nasıl gideceğimizi söylüyor.')],
17:[('我们第一次去新超市。','Wǒmen dì yí cì qù xīn chāoshì.','Yeni süpermarkete ilk kez gidiyoruz.'),('乐乐拿了太多东西。','Lèlè ná le tài duō dōngxi.','Lele çok fazla şey aldı.'),('我们只买需要的东西。','Wǒmen zhǐ mǎi xūyào de dōngxi.','Yalnızca ihtiyacımız olan şeyleri alıyoruz.')],
18:[('我们在超市付款。','Wǒmen zài chāoshì fùkuǎn.','Süpermarkette ödeme yapıyoruz.'),('张伟在找零钱。','Zhāng Wěi zài zhǎo língqián.','Zhang Wei bozuk para arıyor.'),('钱够了，我们可以回家。','Qián gòu le, wǒmen kěyǐ huí jiā.','Para yeterli, eve dönebiliriz.')],
19:[('我们一起吃早饭。','Wǒmen yìqǐ chī zǎofàn.','Birlikte kahvaltı yapıyoruz.'),('每个人喜欢的东西不一样。','Měi ge rén xǐhuan de dōngxi bù yíyàng.','Herkesin sevdiği şey farklı.'),('大家都吃得很开心。','Dàjiā dōu chī de hěn kāixīn.','Herkes keyifle yiyor.')],
20:[('我们要拍全家福。','Wǒmen yào pāi quánjiāfú.','Aile fotoğrafı çekeceğiz.'),('咪咪一直换地方。','Mīmī yìzhí huàn dìfang.','Mimi sürekli yer değiştiriyor.'),('终于拍好照片了。','Zhōngyú pāi hǎo zhàopiàn le.','Sonunda fotoğrafı çektik.')],
21:[('雨桐第一天去新高中。','Yǔtóng dì yī tiān qù xīn gāozhōng.','Yutong’un yeni lisede ilk günü.'),('她走到了错误的楼。','Tā zǒu dào le cuòwù de lóu.','Yanlış binaya gitti.'),('老师告诉她教室在哪儿。','Lǎoshī gàosu tā jiàoshì zài nǎr.','Öğretmen ona sınıfın nerede olduğunu söylüyor.')],
22:[('雨桐来到新班级。','Yǔtóng láidào xīn bānjí.','Yutong yeni sınıfına geliyor.'),('大家还不知道她是谁。','Dàjiā hái bù zhīdào tā shì shéi.','Kimse henüz onun kim olduğunu bilmiyor.'),('老师介绍了雨桐。','Lǎoshī jièshào le Yǔtóng.','Öğretmen Yutong’u tanıttı.')],
23:[('雨桐认识了一个新朋友。','Yǔtóng rènshi le yí ge xīn péngyou.','Yutong yeni bir arkadaş edindi.'),('她不知道午饭和谁一起吃。','Tā bù zhīdào wǔfàn hé shéi yìqǐ chī.','Öğle yemeğini kiminle yiyeceğini bilmiyor.'),('新朋友请她一起吃午饭。','Xīn péngyou qǐng tā yìqǐ chī wǔfàn.','Yeni arkadaşı onu birlikte öğle yemeğine çağırıyor.')],
24:[('乐乐第一天上小学。','Lèlè dì yī tiān shàng xiǎoxué.','Lele’nin ilkokuldaki ilk günü.'),('他不想和妈妈分开。','Tā bù xiǎng hé māma fēnkāi.','Annesinden ayrılmak istemiyor.'),('老师让他放心。','Lǎoshī ràng tā fàngxīn.','Öğretmen onu rahatlatıyor.')],
25:[('乐乐在找蓝色铅笔。','Lèlè zài zhǎo lánsè qiānbǐ.','Lele mavi kalemini arıyor.'),('他以为同学拿了他的铅笔。','Tā yǐwéi tóngxué ná le tā de qiānbǐ.','Sınıf arkadaşının kalemini aldığını sanıyor.'),('原来铅笔在自己的书包里。','Yuánlái qiānbǐ zài zìjǐ de shūbāo lǐ.','Meğer kalem kendi çantasındaymış.')],
26:[('张伟开始找工作。','Zhāng Wěi kāishǐ zhǎo gōngzuò.','Zhang Wei iş aramaya başlıyor.'),('他还不知道给谁打电话。','Tā hái bù zhīdào gěi shéi dǎ diànhuà.','Kimi arayacağını henüz bilmiyor.'),('李晨给了他一个电话号码。','Lǐ Chén gěi le tā yí ge diànhuà hàomǎ.','Li Chen ona bir telefon numarası veriyor.')],
27:[('张伟第一次给公司打电话。','Zhāng Wěi dì yī cì gěi gōngsī dǎ diànhuà.','Zhang Wei şirkete ilk kez telefon ediyor.'),('他有一点紧张。','Tā yǒu yìdiǎn jǐnzhāng.','Biraz gergin.'),('他约好了明天的面试。','Tā yuē hǎo le míngtiān de miànshì.','Yarınki iş görüşmesini ayarladı.')],
28:[('张伟在准备面试。','Zhāng Wěi zài zhǔnbèi miànshì.','Zhang Wei iş görüşmesine hazırlanıyor.'),('家人不知道哪件衬衫最好。','Jiārén bù zhīdào nǎ jiàn chènshān zuì hǎo.','Aile hangi gömleğin en iyi olduğuna karar veremiyor.'),('大家选了蓝色衬衫。','Dàjiā xuǎn le lánsè chènshān.','Herkes mavi gömleği seçiyor.')],
29:[('张伟来参加工作面试。','Zhāng Wěi lái cānjiā gōngzuò miànshì.','Zhang Wei iş görüşmesine geliyor.'),('他要介绍自己会做什么。','Tā yào jièshào zìjǐ huì zuò shénme.','Neler yapabildiğini anlatması gerekiyor.'),('经理对他的回答很满意。','Jīnglǐ duì tā de huídá hěn mǎnyì.','Müdür cevaplarından memnun.')],
30:[('公司打来了好消息。','Gōngsī dǎ lái le hǎo xiāoxi.','Şirketten güzel haber geliyor.'),('大家等着听结果。','Dàjiā děngzhe tīng jiéguǒ.','Herkes sonucu bekliyor.'),('张伟找到工作了。','Zhāng Wěi zhǎodào gōngzuò le.','Zhang Wei iş buldu.')],
31:[('今天是张伟上班第一天。','Jīntiān shì Zhāng Wěi shàngbān dì yī tiān.','Bugün Zhang Wei’nin işe ilk günü.'),('他的工作卡找不到了。','Tā de gōngzuò kǎ zhǎo bú dào le.','İş kartını bulamıyor.'),('工作卡原来在外套里。','Gōngzuò kǎ yuánlái zài wàitào lǐ.','Meğer iş kartı montunun içindeymiş.')],
32:[('张伟认识新同事。','Zhāng Wěi rènshi xīn tóngshì.','Zhang Wei yeni iş arkadaşlarıyla tanışıyor.'),('大家都想知道他从哪儿来。','Dàjiā dōu xiǎng zhīdào tā cóng nǎr lái.','Herkes nereden geldiğini merak ediyor.'),('他们很快开始聊天。','Tāmen hěn kuài kāishǐ liáotiān.','Kısa sürede sohbet etmeye başlıyorlar.')],
33:[('大家一起去吃午饭。','Dàjiā yìqǐ qù chī wǔfàn.','Herkes birlikte öğle yemeğine gidiyor.'),('张伟看不懂一个菜名。','Zhāng Wěi kàn bù dǒng yí ge càimíng.','Zhang Wei bir yemek adını anlamıyor.'),('同事帮他选了一份饭。','Tóngshì bāng tā xuǎn le yí fèn fàn.','İş arkadaşı yemek seçmesine yardım ediyor.')],
34:[('张伟下班要坐公交车回家。','Zhāng Wěi xiàbān yào zuò gōngjiāochē huí jiā.','Zhang Wei işten sonra otobüsle eve dönecek.'),('他错过了这班车。','Tā cuòguò le zhè bān chē.','Bu otobüsü kaçırdı.'),('他问到了下一班车的时间。','Tā wèn dào le xià yì bān chē de shíjiān.','Sonraki otobüsün saatini öğrendi.')],
35:[('李晨一家来做客。','Lǐ Chén yì jiā lái zuòkè.','Li Chen’in ailesi misafirliğe geliyor.'),('孩子们开始还有一点害羞。','Háizimen kāishǐ hái yǒu yìdiǎn hàixiū.','Çocuklar başta biraz çekingen.'),('两家人很快聊得很开心。','Liǎng jiā rén hěn kuài liáo de hěn kāixīn.','İki aile kısa sürede keyifle sohbet ediyor.')],
36:[('孩子们一起玩。','Háizimen yìqǐ wán.','Çocuklar birlikte oynuyor.'),('两个孩子都想要同一个玩具。','Liǎng ge háizi dōu xiǎng yào tóng yí ge wánjù.','İki çocuk da aynı oyuncağı istiyor.'),('他们学会一起玩。','Tāmen xuéhuì yìqǐ wán.','Birlikte oynamayı öğreniyorlar.')],
37:[('星期天一家人去公园。','Xīngqītiān yì jiā rén qù gōngyuán.','Pazar günü aile parka gidiyor.'),('乐乐想去很多地方。','Lèlè xiǎng qù hěn duō dìfang.','Lele birçok yere gitmek istiyor.'),('大家一起散步和玩球。','Dàjiā yìqǐ sànbù hé wán qiú.','Herkes birlikte yürüyüp top oynuyor.')],
38:[('乐乐买了一个冰淇淋。','Lèlè mǎi le yí ge bīngqílín.','Lele bir dondurma aldı.'),('冰淇淋掉在地上了。','Bīngqílín diào zài dìshang le.','Dondurma yere düştü.'),('家人给他买了一个新的。','Jiārén gěi tā mǎi le yí ge xīn de.','Ailesi ona yeni bir tane aldı.')],
39:[('大家从公园回家。','Dàjiā cóng gōngyuán huí jiā.','Herkes parktan eve dönüyor.'),('突然下雨了，可是没有雨伞。','Tūrán xiàyǔ le, kěshì méiyǒu yǔsǎn.','Birden yağmur başladı ama şemsiye yok.'),('大家快走回家。','Dàjiā kuài zǒu huí jiā.','Herkes hızlıca eve yürüyor.')],
40:[('快递送来了一个包裹。','Kuàidì sòng lái le yí ge bāoguǒ.','Kurye bir paket getirdi.'),('包裹上的名字不是张伟。','Bāoguǒ shàng de míngzi bú shì Zhāng Wěi.','Paketin üzerindeki isim Zhang Wei değil.'),('他们把包裹送给邻居。','Tāmen bǎ bāoguǒ sòng gěi línjū.','Paketi komşuya veriyorlar.')],
41:[('咪咪今天不吃饭。','Mīmī jīntiān bù chīfàn.','Mimi bugün yemek yemiyor.'),('家人有一点担心。','Jiārén yǒu yìdiǎn dānxīn.','Aile biraz endişeli.'),('兽医说咪咪没有大问题。','Shòuyī shuō Mīmī méiyǒu dà wèntí.','Veteriner Mimi’nin ciddi bir sorunu olmadığını söylüyor.')],
42:[('家人去宠物店。','Jiārén qù chǒngwùdiàn.','Aile pet mağazasına gidiyor.'),('他们不知道哪种猫粮合适。','Tāmen bù zhīdào nǎ zhǒng māoliáng héshì.','Hangi kedi mamasının uygun olduğunu bilmiyorlar.'),('店员帮他们找到了。','Diànyuán bāng tāmen zhǎodào le.','Mağaza çalışanı bulmalarına yardım ediyor.')],
43:[('雨桐明天有第一次考试。','Yǔtóng míngtiān yǒu dì yī cì kǎoshì.','Yutong’un yarın ilk sınavı var.'),('她觉得有一点难。','Tā juéde yǒu yìdiǎn nán.','Biraz zor olduğunu düşünüyor.'),('家人陪她一起学习。','Jiārén péi tā yìqǐ xuéxí.','Ailesi onunla birlikte çalışıyor.')],
44:[('乐乐画了全家福。','Lèlè huà le quánjiāfú.','Lele bir aile resmi çizdi.'),('老师请他介绍家人。','Lǎoshī qǐng tā jièshào jiārén.','Öğretmen ailesini tanıtmasını istiyor.'),('乐乐高兴地介绍了大家。','Lèlè gāoxìng de jièshào le dàjiā.','Lele herkesi sevinçle tanıtıyor.')],
45:[('张伟拿到第一个月的工资。','Zhāng Wěi ná dào dì yí ge yuè de gōngzī.','Zhang Wei ilk aylık maaşını aldı.'),('大家想怎么庆祝。','Dàjiā xiǎng zěnme qìngzhù.','Herkes nasıl kutlayacağını düşünüyor.'),('他们决定晚上一起吃饭。','Tāmen juédìng wǎnshang yìqǐ chīfàn.','Akşam birlikte yemek yemeye karar veriyorlar.')],
46:[('刘梅做了几个蛋糕。','Liú Méi zuò le jǐ ge dàngāo.','Liu Mei birkaç kek yaptı.'),('邻居都说很好吃。','Línjū dōu shuō hěn hǎochī.','Komşular hepsinin çok lezzetli olduğunu söylüyor.'),('刘梅很高兴。','Liú Méi hěn gāoxìng.','Liu Mei çok mutlu.')],
47:[('大家在说刘梅的蛋糕。','Dàjiā zài shuō Liú Méi de dàngāo.','Herkes Liu Mei’nin keklerinden konuşuyor.'),('朋友说她可以卖这些蛋糕。','Péngyou shuō tā kěyǐ mài zhèxiē dàngāo.','Arkadaşı bu kekleri satabileceğini söylüyor.'),('一个小小的想法开始了。','Yí ge xiǎoxiǎo de xiǎngfa kāishǐ le.','Küçük bir fikir doğuyor.')],
48:[('一家人参加社区活动。','Yì jiā rén cānjiā shèqū huódòng.','Aile mahalle etkinliğine katılıyor.'),('他们还不认识很多人。','Tāmen hái bù rènshi hěn duō rén.','Henüz çok fazla kişi tanımıyorlar.'),('今天他们认识了新朋友。','Jīntiān tāmen rènshi le xīn péngyou.','Bugün yeni arkadaşlar edindiler.')],
49:[('我们来新城三个月了。','Wǒmen lái Xīnchéng sān ge yuè le.','Yeni kasabaya geleli üç ay oldu.'),('大家想起以前的生活。','Dàjiā xiǎngqǐ yǐqián de shēnghuó.','Herkes eski yaşamını hatırlıyor.'),('我们越来越喜欢这里。','Wǒmen yuèláiyuè xǐhuan zhèlǐ.','Burayı gittikçe daha çok seviyoruz.')],
50:[('今天两家人一起吃饭。','Jīntiān liǎng jiā rén yìqǐ chīfàn.','Bugün iki aile birlikte yemek yiyor.'),('大家说起刚来新城的时候。','Dàjiā shuōqǐ gāng lái Xīnchéng de shíhou.','Herkes yeni kasabaya ilk geldikleri zamanı konuşuyor.'),('这里现在是我们的家。','Zhèlǐ xiànzài shì wǒmen de jiā.','Burası artık bizim evimiz.')]
}

ROLES = {
1:['张伟','刘梅','张雨桐','张乐乐','王师傅'],2:['张伟','刘梅','张雨桐','张乐乐'],3:['张伟','刘梅','工作人员','张乐乐'],
4:['张伟','刘梅','张雨桐','张乐乐','售货员'],5:['张乐乐','张雨桐','刘梅','张伟'],6:['张伟','刘梅','张雨桐','张乐乐'],
7:['张伟','刘梅','工作人员','张乐乐'],8:['张伟','刘梅','李晨','张乐乐'],9:['张伟','刘梅','李晨','司机'],10:['张伟','刘梅','张乐乐','张雨桐'],
11:['张伟','刘梅','张雨桐','张乐乐'],12:['刘梅','张伟','张乐乐','张雨桐'],13:['张乐乐','刘梅','张雨桐','张伟'],14:['刘梅','张伟','邻居','张乐乐'],
15:['刘梅','邻居','张伟','张乐乐'],16:['张伟','刘梅','邻居','张乐乐'],17:['刘梅','张伟','张乐乐','店员'],18:['张伟','刘梅','收银员','张乐乐'],
19:['刘梅','张伟','张雨桐','张乐乐'],20:['张伟','刘梅','张雨桐','张乐乐'],21:['张雨桐','老师','工作人员','同学'],22:['老师','张雨桐','同学','同学'],
23:['张雨桐','同学','同学','老师'],24:['张乐乐','刘梅','老师','同学'],25:['张乐乐','同学','老师','刘梅'],26:['张伟','李晨','刘梅','张雨桐'],
27:['张伟','公司职员','刘梅','张雨桐'],28:['张伟','刘梅','张雨桐','张乐乐'],29:['张伟','经理','公司职员','张伟'],30:['张伟','刘梅','张雨桐','张乐乐'],
31:['张伟','同事','保安','经理'],32:['张伟','同事','同事','经理'],33:['张伟','同事','服务员','同事'],34:['张伟','乘客','工作人员','刘梅'],
35:['张伟','刘梅','李晨','李晨妻子'],36:['张乐乐','小朋友','张雨桐','刘梅'],37:['张伟','刘梅','张乐乐','张雨桐'],38:['张乐乐','刘梅','张伟','店员'],
39:['张伟','刘梅','张乐乐','张雨桐'],40:['张伟','刘梅','快递员','邻居'],41:['刘梅','张伟','兽医','张乐乐'],42:['刘梅','张伟','店员','张乐乐'],
43:['张雨桐','刘梅','张伟','张乐乐'],44:['张乐乐','老师','同学','同学'],45:['张伟','刘梅','张雨桐','张乐乐'],46:['刘梅','张伟','邻居','张乐乐'],
47:['刘梅','张伟','李晨妻子','李晨'],48:['张伟','刘梅','社区工作人员','新朋友'],49:['张伟','刘梅','张雨桐','张乐乐'],50:['张伟','刘梅','李晨','李晨妻子']
}

# Reusable controlled HSK1 utterances. These are deliberately high-frequency.
COMMON = [
('好。','Hǎo.','Tamam.'),('好的。','Hǎo de.','Olur.'),('对。','Duì.','Evet / doğru.'),('不对。','Bú duì.','Hayır / doğru değil.'),
('是吗？','Shì ma?','Öyle mi?'),('是的。','Shì de.','Evet.'),('不是。','Bú shì.','Hayır / değil.'),('真的吗？','Zhēn de ma?','Gerçekten mi?'),
('真的。','Zhēn de.','Gerçekten.'),('谢谢。','Xièxie.','Teşekkür ederim.'),('不客气。','Bú kèqi.','Rica ederim.'),
('等一下。','Děng yíxià.','Bir dakika bekle.'),('没事。','Méi shì.','Sorun değil.'),('别急。','Bié jí.','Acele etme / panik yapma.'),
('我来看看。','Wǒ lái kànkan.','Ben bir bakayım.'),('你看。','Nǐ kàn.','Bak.'),('在这里。','Zài zhèlǐ.','Burada.'),('在那里。','Zài nàlǐ.','Orada.'),
('在哪儿？','Zài nǎr?','Nerede?'),('我知道。','Wǒ zhīdào.','Biliyorum.'),('我不知道。','Wǒ bù zhīdào.','Bilmiyorum.'),
('我们一起吧。','Wǒmen yìqǐ ba.','Birlikte yapalım.'),('可以。','Kěyǐ.','Olur / yapılabilir.'),('不可以。','Bù kěyǐ.','Olmaz / yapılamaz.'),
('太好了！','Tài hǎo le!','Harika!'),('我很高兴。','Wǒ hěn gāoxìng.','Çok mutluyum.'),('走吧。','Zǒu ba.','Hadi gidelim.'),
('来吧。','Lái ba.','Hadi / gel.'),('你呢？','Nǐ ne?','Ya sen?'),('我也是。','Wǒ yě shì.','Ben de.'),('现在吗？','Xiànzài ma?','Şimdi mi?'),
('今天吗？','Jīntiān ma?','Bugün mü?'),('我喜欢。','Wǒ xǐhuan.','Seviyorum.'),('我不喜欢。','Wǒ bù xǐhuan.','Sevmiyorum.'),
('很好。','Hěn hǎo.','Çok iyi.'),('有一点。','Yǒu yìdiǎn.','Biraz.'),('快一点。','Kuài yìdiǎn.','Biraz hızlı.'),('慢一点。','Màn yìdiǎn.','Biraz yavaş.'),
('我来帮你。','Wǒ lái bāng nǐ.','Sana yardım edeyim.'),('谢谢你。','Xièxie nǐ.','Teşekkür ederim.'),('我们准备好了。','Wǒmen zhǔnbèi hǎo le.','Hazırız.'),
('还没有。','Hái méiyǒu.','Henüz değil / henüz yok.'),('现在好了。','Xiànzài hǎo le.','Şimdi tamam.'),('再看一次。','Zài kàn yí cì.','Bir kez daha bakalım.'),
('没问题。','Méi wèntí.','Sorun yok.'),('我明白了。','Wǒ míngbai le.','Anladım.'),('你明白吗？','Nǐ míngbai ma?','Anladın mı?'),
('明白。','Míngbai.','Anladım.'),('我们继续。','Wǒmen jìxù.','Devam edelim.'),('好主意。','Hǎo zhǔyi.','İyi fikir.'),
('小心一点。','Xiǎoxīn yìdiǎn.','Biraz dikkatli ol.'),('没关系。','Méi guānxi.','Önemli değil.'),('我看看。','Wǒ kànkan.','Bir bakayım.'),
('你说得对。','Nǐ shuō de duì.','Haklısın.'),('我们到了。','Wǒmen dào le.','Geldik.'),('还要什么？','Hái yào shénme?','Başka ne gerekiyor?'),
('没有了。','Méiyǒu le.','Artık yok.'),('就是这个。','Jiù shì zhège.','Tam olarak bu.'),('不是这个。','Bú shì zhège.','Bu değil.'),
('那个呢？','Nàge ne?','Peki şu?'),('这个呢？','Zhège ne?','Peki bu?'),('我找到了。','Wǒ zhǎodào le.','Buldum.'),
('你找到了吗？','Nǐ zhǎodào le ma?','Buldun mu?'),('还在找。','Hái zài zhǎo.','Hâlâ arıyorum.'),('我们回家吧。','Wǒmen huí jiā ba.','Eve dönelim.'),
('今天很好。','Jīntiān hěn hǎo.','Bugün çok güzel.'),('大家都在。','Dàjiā dōu zài.','Herkes burada.'),('准备好了吗？','Zhǔnbèi hǎo le ma?','Hazır mısınız?')
]


UNSAFE_NOUN_PATTERN = {
    'move','today','tomorrow','evening','study','pay','three_months'
}

def safe_keys(n):
    keys=[k for k in VOCAB[n] if k not in UNSAFE_NOUN_PATTERN]
    return keys if len(keys)>=3 else VOCAB[n]



def captr(s:str)->str:
    return s[0].upper()+s[1:] if s else s

FOOD_KEYS={'bread','water','tea','milk','egg','breakfast','apple','coffee','juice','rice','noodle','soup','chicken','food','lunch','cake','icecream','catfood'}
PLACE_KEYS={'station','platform','city','school','home','road','room','kitchen','living','supermarket','highschool','classroom','office','park','hospital','petshop','shop','community','newcity'}
PERSON_KEYS={'friend','neighbor','student','teacher','colleague','manager','guest','vet','doctor','family','mother','father','people','child'}
TRANSPORT_KEYS={'train','taxi','bus','car','bike'}
TIME_KEYS={'today','tomorrow','evening','three_months'}
DIRECTION_KEYS={'left','right'}
COLOR_KEYS={'blue','red'}
INFO_KEYS={'address','name','number','phone_number'}
EVENT_KEYS={'move','job','study','pay','interview','exam','activity'}


def concept_exchange(key):
    zh,py,tr=W[key]
    if key in FOOD_KEYS:
        return [
          (f'你要{zh}吗？',f'Nǐ yào {py} ma?',f'{captr(tr)} ister misin?'),
          (f'我要{zh}，谢谢。',f'Wǒ yào {py}, xièxie.',f'{captr(tr)} istiyorum, teşekkürler.'),
          ('好的。','Hǎo de.','Olur.'),('谢谢。','Xièxie.','Teşekkür ederim.')]
    if key in PLACE_KEYS:
        return [
          (f'{zh}在哪儿？',f'{py.capitalize()} zài nǎr?',f'{captr(tr)} nerede?'),
          (f'{zh}在那边。',f'{py.capitalize()} zài nàbian.',f'{captr(tr)} şu tarafta.'),
          ('我明白了。','Wǒ míngbai le.','Anladım.'),('谢谢。','Xièxie.','Teşekkür ederim.')]
    if key in PERSON_KEYS:
        return [
          (f'这是我们的{zh}。',f'Zhè shì wǒmen de {py}.',f'Bu bizim {tr}.'),
          ('你好！','Nǐ hǎo!','Merhaba!'),('很高兴认识你。','Hěn gāoxìng rènshi nǐ.','Tanıştığımıza memnun oldum.'),('我也是。','Wǒ yě shì.','Ben de.')]
    if key in TRANSPORT_KEYS:
        return [
          (f'我们坐{zh}吗？',f'Wǒmen zuò {py} ma?',f'{captr(tr)} ile mi gidiyoruz?'),
          (f'对，我们坐{zh}。',f'Duì, wǒmen zuò {py}.',f'Evet, {tr} ile gidiyoruz.'),('准备好了吗？','Zhǔnbèi hǎo le ma?','Hazır mısınız?'),('准备好了。','Zhǔnbèi hǎo le.','Hazırız.')]
    if key in TIME_KEYS:
        if key=='today': return [('今天忙吗？','Jīntiān máng ma?','Bugün yoğun musun?'),('有一点。','Yǒu yìdiǎn.','Biraz.'),('没关系。','Méi guānxi.','Sorun değil.'),('我们继续。','Wǒmen jìxù.','Devam edelim.')]
        if key=='tomorrow': return [('明天可以吗？','Míngtiān kěyǐ ma?','Yarın uygun mu?'),('可以。','Kěyǐ.','Uygun.'),('几点？','Jǐ diǎn?','Saat kaçta?'),('明天见。','Míngtiān jiàn.','Yarın görüşürüz.')]
        if key=='evening': return [('晚上有时间吗？','Wǎnshang yǒu shíjiān ma?','Akşam vaktin var mı?'),('有。','Yǒu.','Var.'),('晚上见。','Wǎnshang jiàn.','Akşam görüşürüz.'),('好。','Hǎo.','Tamam.')]
        return [('三个月了。','Sān ge yuè le.','Üç ay oldu.'),('时间真快。','Shíjiān zhēn kuài.','Zaman gerçekten hızlı geçiyor.'),('是啊。','Shì a.','Evet.'),('我们很喜欢这里。','Wǒmen hěn xǐhuan zhèlǐ.','Burayı çok seviyoruz.')]
    if key in DIRECTION_KEYS:
        return [(f'在{zh}吗？',f'Zài {py} ma?',f'{captr(tr)} mı?'),(f'对，在{zh}。',f'Duì, zài {py}.',f'Evet, {tr}.'),('这边走。','Zhèbiān zǒu.','Bu taraftan gidin.'),('谢谢。','Xièxie.','Teşekkürler.')]
    if key in COLOR_KEYS:
        return [(f'你喜欢{zh}吗？',f'Nǐ xǐhuan {py} ma?',f'{captr(tr)} seviyor musun?'),('喜欢。','Xǐhuan.','Seviyorum.'),(f'这个是{zh}的。',f'Zhège shì {py} de.',f'Bu {tr}.'),('很好看。','Hěn hǎokàn.','Çok güzel görünüyor.')]
    if key in INFO_KEYS:
        return [(f'你的{zh}是什么？',f'Nǐ de {py} shì shénme?',f'{captr(tr)} nedir?'),(f'这是我的{zh}。',f'Zhè shì wǒ de {py}.',f'Bu benim {tr}.'),('我记下了。','Wǒ jìxià le.','Not aldım.'),('谢谢。','Xièxie.','Teşekkürler.')]
    if key in EVENT_KEYS:
        if key=='move': q=('今天搬家吗？','Jīntiān bānjiā ma?','Bugün taşınıyor musunuz?')
        elif key=='job': q=('你在找工作吗？','Nǐ zài zhǎo gōngzuò ma?','İş mi arıyorsun?')
        elif key=='study': q=('你在学习吗？','Nǐ zài xuéxí ma?','Ders mi çalışıyorsun?')
        elif key=='pay': q=('现在付款吗？','Xiànzài fùkuǎn ma?','Şimdi ödeme yapıyor muyuz?')
        elif key=='interview': q=('今天有面试吗？','Jīntiān yǒu miànshì ma?','Bugün iş görüşmesi var mı?')
        elif key=='exam': q=('今天有考试吗？','Jīntiān yǒu kǎoshì ma?','Bugün sınav var mı?')
        else: q=('今天有活动吗？','Jīntiān yǒu huódòng ma?','Bugün etkinlik var mı?')
        return [q,('对。','Duì.','Evet.'),('准备好了吗？','Zhǔnbèi hǎo le ma?','Hazır mısın?'),('准备好了。','Zhǔnbèi hǎo le.','Hazırım.')]
    # Object/default pattern.
    return [(f'这是{zh}吗？',f'Zhè shì {py} ma?',f'Bu, {tr} mı?'),(f'对，这是{zh}。',f'Duì, zhè shì {py}.',f'Evet, bu {tr}.'),(f'{zh}在哪儿？',f'{py.capitalize()} zài nǎr?',f'{captr(tr)} nerede?'),(f'{zh}在这里。',f'{py.capitalize()} zài zhèlǐ.',f'{captr(tr)} burada.')]


def vocab_lines(words):
    out=[]
    for key in words[:8]: out.extend(concept_exchange(key))
    return out

def make_dialogues(n, spec):
    roles=ROLES[n]
    focus=F[n]
    words=VOCAB[n]
    lines=[]
    # Setup: establish the scene mission naturally.
    lines += [focus[0],('是吗？','Shì ma?','Öyle mi?'),('对。','Duì.','Evet.'),('准备好了吗？','Zhǔnbèi hǎo le ma?','Hazır mısınız?'),('准备好了。','Zhǔnbèi hǎo le.','Hazırız.')]
    # Concrete language from the current scene.
    for key in words[:4]: lines += concept_exchange(key)
    # Complication and collaborative response.
    lines += [focus[1],('别急。','Bié jí.','Panik yapma.'),('我来看看。','Wǒ lái kànkan.','Ben bir bakayım.'),('我们一起吧。','Wǒmen yìqǐ ba.','Birlikte yapalım.'),('好。','Hǎo.','Tamam.')]
    for key in words[4:8]: lines += concept_exchange(key)
    # Resolution and useful closing phrases.
    lines += [focus[2],('太好了！','Tài hǎo le!','Harika!'),('谢谢你。','Xièxie nǐ.','Teşekkür ederim.'),('不客气。','Bú kèqi.','Rica ederim.'),('现在好了。','Xiànzài hǎo le.','Şimdi tamam.'),('我们继续。','Wǒmen jìxù.','Devam edelim.')]
    # Pedagogical recycling: repeat the active concepts in slightly spaced cycles.
    active=words[:6]
    cycle=0
    while len(lines)<95:
        lines += concept_exchange(active[cycle % len(active)])
        cycle += 1
    lines=lines[:95]
    lines += [('今天学了很多。','Jīntiān xué le hěn duō.','Bugün çok şey öğrendik.'),('我也是。','Wǒ yě shì.','Ben de.'),('都好了吗？','Dōu hǎo le ma?','Her şey tamam mı?'),('都好了。','Dōu hǎo le.','Her şey tamam.'),('走吧。','Zǒu ba.','Hadi gidelim.')]
    result=[]
    for i,(zh,py,tr) in enumerate(lines[:100],1):
        speaker=roles[(i-1)%len(roles)]
        result.append({'id':f'DLG_ZH_HSK1_SC{n:03d}_{i:03d}','speaker':speaker,'zh':zh,'pinyin':py,'tr':tr})
    return result

def card_example(key):
    zh,py,tr=W[key]
    special={
      'move':('我们今天搬家。','Wǒmen jīntiān bānjiā.','Bugün taşınıyoruz.'),
      'today':('今天很好。','Jīntiān hěn hǎo.','Bugün çok güzel.'),
      'tomorrow':('明天见。','Míngtiān jiàn.','Yarın görüşürüz.'),
      'evening':('晚上见。','Wǎnshang jiàn.','Akşam görüşürüz.'),
      'study':('我在学习。','Wǒ zài xuéxí.','Ders çalışıyorum.'),
      'pay':('我来付款。','Wǒ lái fùkuǎn.','Ödemeyi ben yapayım.'),
      'three_months':('我们来这里三个月了。','Wǒmen lái zhèlǐ sān ge yuè le.','Buraya geleli üç ay oldu.'),
      'left':('在左边。','Zài zuǒbian.','Sol tarafta.'),
      'right':('在右边。','Zài yòubian.','Sağ tarafta.'),
      'new':('这是新的。','Zhè shì xīn de.','Bu yeni.'),
      'old':('这是旧的。','Zhè shì jiù de.','Bu eski.'),
      'weather':('今天天气很好。','Jīntiān tiānqì hěn hǎo.','Bugün hava çok güzel.'),
      'rain':('今天下雨了。','Jīntiān xiàyǔ le.','Bugün yağmur yağıyor.'),
      'salary':('我今天拿工资了。','Wǒ jīntiān ná gōngzī le.','Bugün maaşımı aldım.'),
      'idea':('这是一个好想法。','Zhè shì yí ge hǎo xiǎngfa.','Bu iyi bir fikir.'),
      'activity':('今天有活动。','Jīntiān yǒu huódòng.','Bugün bir etkinlik var.')
    }
    return special.get(key,(f'这是{zh}。',f'Zhè shì {py}.',f'Bu {tr}.'))

def make_cards(n):
    cards=[]
    for i,key in enumerate(VOCAB[n],1):
        zh,py,tr=W[key]
        ezh,epy,etr=card_example(key)
        cards.append({'id':f'VOC_ZH_HSK1_SC{n:03d}_{i:03d}','zh':zh,'pinyin':py,'tr':tr,
                      'exampleZh':ezh,'examplePinyin':epy,'exampleTr':etr,'kind':'active' if i<=6 else 'review'})
    return cards

def make_exercises(n):
    keys=safe_keys(n)
    a,b,c=keys[0],keys[1],keys[2]
    A,B,C=W[a],W[b],W[c]
    return [
      {'id':f'SENT_ZH_HSK1_SC{n:03d}_001','type':'word_order','promptTr':'Kelimeleri doğru sıraya koy.',
       'tokens':[A[0],'在','这里'],'answerTokens':[A[0],'在','这里']},
      {'id':f'SENT_ZH_HSK1_SC{n:03d}_002','type':'fill_blank','promptTr':'Boşluğu doğru kelimeyle doldur.',
       'blankSentenceZh':'这是___。','options':[A[0],B[0],C[0]],'answer':A[0]},
      {'id':f'SENT_ZH_HSK1_SC{n:03d}_003','type':'sentence_repair','promptTr':'Yanlış sıradaki cümleyi düzelt.',
       'tokens':['这里','在',B[0]],'answerTokens':[B[0],'在','这里']},
      {'id':f'SENT_ZH_HSK1_SC{n:03d}_004','type':'word_order','promptTr':'Kelimeleri doğru sıraya koy.',
       'tokens':['这是',C[0]],'answerTokens':['这是',C[0]]},
      {'id':f'SENT_ZH_HSK1_SC{n:03d}_005','type':'fill_blank','promptTr':'Boşluğu doğru kelimeyle doldur.',
       'blankSentenceZh':f'{B[0]}在___。','options':['这里','谢谢','很好'],'answer':'这里'},
      {'id':f'SENT_ZH_HSK1_SC{n:03d}_006','type':'sentence_repair','promptTr':'Yanlış sıradaki cümleyi düzelt.',
       'tokens':['在哪儿',A[0]],'answerTokens':[A[0],'在哪儿']},
      {'id':f'SENT_ZH_HSK1_SC{n:03d}_007','type':'word_order','promptTr':'Kelimeleri doğru sıraya koy.',
       'tokens':['我','喜欢',C[0]],'answerTokens':['我','喜欢',C[0]]},
      {'id':f'SENT_ZH_HSK1_SC{n:03d}_008','type':'fill_blank','promptTr':'Boşluğu doğru kelimeyle doldur.',
       'blankSentenceZh':'___，谢谢。','options':['好的','在哪儿','不是'],'answer':'好的'},
      {'id':f'SENT_ZH_HSK1_SC{n:03d}_009','type':'sentence_repair','promptTr':'Yanlış sıradaki cümleyi düzelt.',
       'tokens':['一起','我们','吧'],'answerTokens':['我们','一起','吧']}
    ]

def make_comprehension(n, scene):
    g,p,r=F[n]
    return [
      {'id':f'COMP_ZH_HSK1_SC{n:03d}_001','questionTr':'Bu sahnenin ana olayı nedir?',
       'optionsTr':[scene['titleTr'],'Bir havaalanı yolculuğu','Bir spor maçı'],'correctIndex':0},
      {'id':f'COMP_ZH_HSK1_SC{n:03d}_002','questionTr':'Sahnede küçük bir sorun yaşanıyor mu?',
       'optionsTr':['Evet','Hayır','Belli değil'],'correctIndex':0},
      {'id':f'COMP_ZH_HSK1_SC{n:03d}_003','questionTr':'Sorun sahne sonunda çözülüyor mu?',
       'optionsTr':['Evet','Hayır','Sahne bitmiyor'],'correctIndex':0},
      {'id':f'COMP_ZH_HSK1_SC{n:03d}_004','questionTr':'Sahnenin amacı hangi hikâyeye bağlıdır?',
       'optionsTr':['Zhang ailesinin yeni kasabadaki yaşamına','Bir tarih belgeseline','Bir spor turnuvasına'],'correctIndex':0}
    ]

def make_pronunciation(n, cards):
    return [
      {'id':f'PRON_ZH_HSK1_SC{n:03d}_{i:03d}','zh':c['exampleZh'],'pinyin':c['examplePinyin'],'tr':c['exampleTr'],
       'scoring':['pronunciation','toneAccuracy','fluency','timing','completeness']}
      for i,c in enumerate(cards[:4],1)
    ]

def make_interactive(n):
    a,b,c=[W[k] for k in safe_keys(n)[:3]]
    return [
      {'id':f'INT_ZH_HSK1_SC{n:03d}_001','promptZh':f'{a[0]}在哪儿？','promptPinyin':f'{a[1].capitalize()} zài nǎr?',
       'promptTr':f'{captr(a[2])} nerede?','options':[{'zh':'在这里。','tr':'Burada.','correct':True},{'zh':'谢谢。','tr':'Teşekkürler.','correct':False},{'zh':'我很好。','tr':'Ben iyiyim.','correct':False}]},
      {'id':f'INT_ZH_HSK1_SC{n:03d}_002','promptZh':f'这是{b[0]}吗？','promptPinyin':f'Zhè shì {b[1]} ma?',
       'promptTr':f'Bu {b[2]} mı?','options':[{'zh':'对，是的。','tr':'Evet.','correct':True},{'zh':'我叫张伟。','tr':'Benim adım Zhang Wei.','correct':False},{'zh':'明天见。','tr':'Yarın görüşürüz.','correct':False}]},
      {'id':f'INT_ZH_HSK1_SC{n:03d}_003','promptZh':f'你喜欢{c[0]}吗？','promptPinyin':f'Nǐ xǐhuan {c[1]} ma?',
       'promptTr':f'{captr(c[2])} seviyor musun?','options':[{'zh':'喜欢。','tr':'Seviyorum.','correct':True},{'zh':'在右边。','tr':'Sağ tarafta.','correct':False},{'zh':'五点。','tr':'Saat beş.','correct':False}]}
    ]

def make_production(n, scene):
    return {
      'scenePurposeTr':scene.get('miniAdventureTr',''),
      'timeOfDay':'day' if n not in (12,19,35,43,45,50) else 'evening',
      'atmosphere':'sıcak, doğal, günlük yaşam odaklı',
      'characters':ROLES[n],
      'locationId':scene.get('locationId',''),
      'visual':{'reuseLocation':True,'newVisualRequired':False,'style':'visual_novel_theatre'},
      'audio':{'voiceLanguage':'zh-CN','narratorProfile':'NARRATOR_ZH_001','defaultSpeechSpeed':0.80},
      'animation':{'level':'minimal','mouthMode':'AUTO_SIMPLE','blink':True,'speakerFocus':True},
      'continuityNoteTr':f"{scene['titleTr']} olayı ana aile kronolojisinde sahne {n} olarak kaydedilir."
    }

def main():
    data=json.loads(PATH.read_text(encoding='utf-8'))
    assert len(data['scenes'])==50
    for scene in data['scenes']:
        n=scene['number']
        cards=make_cards(n)
        learning=dict(scene.get('learning') or {})
        learning.update({
          'vocabularyCards':cards,
          'sentenceExercises':make_exercises(n),
          'comprehensionQuestions':make_comprehension(n,scene),
          'pronunciationItems':make_pronunciation(n,cards),
          'interactiveDialogue':make_interactive(n),
          'examRules':{'vocabularyPassPercent':90,'sentencePassPercent':85,'lockNextSceneUntilPassed':True},
          'examStages':[{'stage':1,'type':'vocabulary','passPercent':90},{'stage':2,'type':'sentence','passPercent':85,'requiresStage':1}],
          'flashCardPolicy':{'allowPrevious':True,'allowNext':True,'allowFavorite':True,'favoritesStudyMode':True}
        })
        scene['learning']=learning
        scene['dialogues']=make_dialogues(n,scene)
        scene['production']=make_production(n,scene)
        scene['complete']=True
        scene['productionStatus']='complete'
        scene['editorialStatus']='generated_full_v1_requires_native_review'
        scene['dialogueCount']=len(scene['dialogues'])
    data['schemaVersion']=3
    data['completeSceneCount']=50
    data['editorialNoteTr']='HSK1 50 sahne veri olarak tamdır; ticari/native yayın öncesi ana dili Çince olan editör kontrolü önerilir.'
    PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('HSK1 authoring completed:',len(data['scenes']),'scenes,',sum(len(s['dialogues']) for s in data['scenes']),'dialogues')

if __name__=='__main__': main()
