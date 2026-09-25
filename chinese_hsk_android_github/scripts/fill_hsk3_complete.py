#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the HSK3 production payload for all 50 scenes.

The generator is deterministic and offline. It intentionally keeps an editorial/native-review
flag separate from technical completeness. The dialogue bank is HSK3-oriented: connected
speech, cause/effect, comparison, planning, clarification, and problem solving.
"""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'authoring' / 'hsk3_blueprints.json'

# Reuse the verified vocabulary/pinyin base from HSK2 without executing its main().
spec = importlib.util.spec_from_file_location('hsk2gen', ROOT/'scripts'/'fill_hsk2_complete.py')
h2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(h2)
W = dict(h2.W)

# HSK3-specific vocabulary. Values: simplified Chinese, tone-marked pinyin, Turkish.
W.update({
'order_list':('订单表','dìngdān biǎo','sipariş listesi'), 'complaint':('投诉','tóusù','şikâyet'),
'replace':('换一个','huàn yí ge','yenisiyle değiştirmek'), 'project':('项目','xiàngmù','proje'),
'project_team':('项目组','xiàngmù zǔ','proje ekibi'), 'task':('任务','rènwu','görev'),
'schooltrip':('学校旅行','xuéxiào lǚxíng','okul gezisi'), 'permission':('同意书','tóngyìshū','izin formu'),
'rule':('规定','guīdìng','kural'), 'newteacher':('新老师','xīn lǎoshī','yeni öğretmen'),
'cafeidea':('咖啡馆的想法','kāfēiguǎn de xiǎngfa','kafe fikri'), 'business':('生意','shēngyi','iş / ticaret'),
'futureplan':('未来计划','wèilái jìhuà','gelecek planı'), 'premises':('店面','diànmiàn','dükkân / iş yeri'),
'advantage':('优点','yōudiǎn','avantaj'), 'disadvantage':('缺点','quēdiǎn','dezavantaj'),
'rent':('房租','fángzū','kira'), 'location':('位置','wèizhi','konum'), 'corner_shop':('街角店铺','jiējiǎo diànpù','köşe dükkânı'),
'potential':('潜力','qiánlì','potansiyel'), 'familymeeting':('家庭会议','jiātíng huìyì','aile toplantısı'),
'risk':('风险','fēngxiǎn','risk'), 'benefit':('好处','hǎochu','fayda'), 'cafename':('店名','diànmíng','kafe adı'),
'memorable':('好记','hǎojì','akılda kalıcı'), 'permit':('许可证','xǔkězhèng','ruhsat / izin belgesi'),
'officialdoc':('证件','zhèngjiàn','resmî belge'), 'renovation':('装修','zhuāngxiū','tadilat'),
'wall':('墙','qiáng','duvar'), 'measure':('尺寸','chǐcùn','ölçü'), 'secondhand':('二手','èrshǒu','ikinci el'),
'oldtable':('老桌子','lǎo zhuōzi','eski masa'), 'menu':('菜单','càidān','menü'), 'score':('打分','dǎfēn','puan vermek'),
'cost':('成本','chéngběn','maliyet'), 'pricing':('定价','dìngjià','fiyat belirleme'), 'applicant':('应聘者','yìngpìnzhě','iş başvurusu yapan kişi'),
'experience':('经验','jīngyàn','deneyim'), 'workhours':('工作时间','gōngzuò shíjiān','çalışma saatleri'), 'signboard':('招牌','zhāopai','tabela'),
'horserror':('错字','cuòzì','yazım hatası'), 'correct_word':('改正','gǎizhèng','düzeltmek'), 'trialopen':('试营业','shì yíngyè','deneme açılışı'),
'service':('服务','fúwù','hizmet'), 'realcustomer':('正式顾客','zhèngshì gùkè','gerçek/normal müşteri'), 'detailedorder':('详细订单','xiángxì dìngdān','ayrıntılı sipariş'),
'coffeemachine':('咖啡机','kāfēijī','kahve makinesi'), 'broken':('坏了','huài le','bozuldu'), 'repair':('维修','wéixiū','tamir'),
'responsibility':('责任','zérèn','sorumluluk'), 'paidshift':('打工','dǎgōng','ücretli çalışmak'), 'homeworkcorner':('作业角','zuòyè jiǎo','ödev köşesi'),
'regular':('常客','chángkè','düzenli müşteri'), 'smalltalk':('聊天','liáotiān','sohbet etmek'), 'discount':('优惠','yōuhuì','indirim / kampanya'),
'promotion':('促销','cùxiāo','promosyon'), 'businesstrip':('出差','chūchāi','iş seyahati'), 'reservation':('预订','yùdìng','rezervasyon'),
'roomtype':('房型','fángxíng','oda tipi'), 'presentation':('汇报','huìbào','sunum / raporlama'), 'result':('结果','jiéguǒ','sonuç'),
'examstress':('考试压力','kǎoshì yālì','sınav stresi'), 'studyplan':('学习计划','xuéxí jìhuà','çalışma planı'), 'tryout':('选拔','xuǎnbá','seçme / eleme'),
'disappointed':('失望','shīwàng','hayal kırıklığı'), 'argument':('争执','zhēngzhí','tartışma'), 'mediate':('调解','tiáojiě','arabuluculuk yapmak'),
'festivalstall':('节日摊位','jiérì tānwèi','festival standı'), 'bulkorder':('大订单','dà dìngdān','büyük sipariş'), 'deliverytime':('交货时间','jiāohuò shíjiān','teslim zamanı'),
'flour':('面粉','miànfěn','un'), 'supplier':('供应商','gōngyìngshāng','tedarikçi'), 'promotion_job':('升职','shēngzhí','terfi'),
'career':('职业发展','zhíyè fāzhǎn','kariyer gelişimi'), 'dream':('梦想','mèngxiǎng','hayal'), 'regret':('遗憾','yíhàn','pişmanlık / ukde'),
'earlyretire':('提前退休','tíqián tuìxiū','erken emeklilik'), 'longterm':('长期目标','chángqī mùbiāo','uzun vadeli hedef'), 'accountbook':('账本','zhàngběn','hesap defteri'),
'income':('收入','shōurù','gelir'), 'expense':('支出','zhīchū','gider'), 'countryside':('农村','nóngcūn','kırsal bölge'),
'citylife':('城市生活','chéngshì shēnghuó','şehir hayatı'), 'familyrecipe':('家传菜','jiāchuán cài','aile tarifi'), 'tradition':('传统','chuántǒng','gelenek'),
'major':('专业','zhuānyè','üniversite alanı / bölüm'), 'choice':('选择','xuǎnzé','seçim'), 'sciencefair':('科学展','kēxué zhǎn','bilim fuarı'),
'experiment':('实验','shíyàn','deney'), 'donation':('募捐','mùjuān','bağış kampanyası'), 'donate':('捐款','juānkuǎn','bağış yapmak'),
'anniversary':('周年','zhōunián','yıldönümü'), 'memory':('回忆','huíyì','anı'), 'familyfuture':('全家的未来','quánjiā de wèilái','ailenin geleceği'),
'movingidea':('搬来的想法','bān lái de xiǎngfa','buraya taşınma fikri'), 'grandparents':('爷爷奶奶','yéye nǎinai','büyükanne ve büyükbaba'),
'clarify':('说明清楚','shuōmíng qīngchu','açıklığa kavuşturmak'), 'confirm':('确认','quèrèn','teyit etmek'),
'solution':('解决办法','jiějué bànfǎ','çözüm yolu'), 'schedule':('安排','ānpái','planlama / düzenleme'),
'compare2':('比较','bǐjiào','karşılaştırmak'), 'decide2':('决定','juédìng','karar vermek')
})

# Eight scene-appropriate cards per scene (first six are active, last two review/passive).
V = {
1:['order','order_list','call','schedule','confirm','customer','planword','work'],
2:['complaint','cake','large','small','replace','sorry','solution','confirm'],
3:['project','project_team','task','work','schedule','responsibility','colleague','planword'],
4:['schooltrip','permission','prepare','document','remember','need','school','bag'],
5:['newteacher','rule','study','progress','need','change','teacher','school'],
6:['cafeidea','business','futureplan','planword','customer','dream','benefit','risk'],
7:['premises','advantage','disadvantage','location','compare2','need','rent','budget'],
8:['premises','rent','small','disadvantage','advantage','need','measure','decide2'],
9:['location','rent','budget','pricing','compare2','advantage','cost','decide2'],
10:['corner_shop','potential','premises','renovation','wall','measure','location','futureplan'],
11:['familymeeting','risk','benefit','business','budget','decide2','futureplan','opinion'],
12:['cafename','memorable','choose','meaning','idea','decide2','family','cafeidea'],
13:['permit','officialdoc','document','form','sign','need','government','confirm'],
14:['renovation','wall','color','measure','table','choose','style','correct_word'],
15:['secondhand','oldtable','past','story','buy','price','memory','useful'],
16:['menu','taste','score','delicious','choose','compare2','recipe','customer'],
17:['cost','pricing','budget','price','customer','necessary','save','decide2'],
18:['applicant','experience','workhours','interview','work','responsibility','schedule','customer'],
19:['signboard','horserror','correct_word','check','immediately','sorry','cafename','renovation'],
20:['trialopen','service','guest','customer','menu','check','schedule','welcome'],
21:['realcustomer','detailedorder','order','confirm','menu','customer','service','peoplecount'],
22:['coffeemachine','broken','repair','problem','check','step','immediately','customer'],
23:['repair','step','check','fix','coffeemachine','help','firststep','work'],
24:['paidshift','responsibility','customer','service','workhours','order','money','experience'],
25:['homeworkcorner','study','table','children','purpose','cafeidea','community','school'],
26:['regular','smalltalk','morning','customer','routine','welcome','coffee','friend'],
27:['discount','promotion','rain','customer','business','offer','price','planword'],
28:['businesstrip','schedule','ticket','hotel','call','family','travel','prepare'],
29:['reservation','roomtype','hotel','wrong','complaint','replace','confirm','solution'],
30:['presentation','project','result','step','explain','meeting','work','confirm'],
31:['examstress','studyplan','study','schedule','advice','need','rest','progress'],
32:['tryout','team','disappointed','cheer','exercise','retry','sport','futureplan'],
33:['argument','mediate','customer','table','solution','polite','clarify','service'],
34:['festivalstall','festival','customer','sell','promotion','community','food','busy'],
35:['bulkorder','deliverytime','portion','schedule','order','customer','enough','cost'],
36:['flour','supplier','lack','immediately','order','solution','call','cook'],
37:['promotion_job','career','responsibility','work','futureplan','family','risk','benefit'],
38:['dream','regret','futureplan','friend','walk','life','hope','decide2'],
39:['earlyretire','longterm','dream','cafeidea','futureplan','because','family','life'],
40:['accountbook','income','expense','cost','budget','money','business','month'],
41:['countryside','citylife','grandparents','compare2','farm','life','fresh','family'],
42:['familyrecipe','recipe','step','cook','tradition','taste','grandparents','remember'],
43:['familyrecipe','menu','tradition','customer','taste','score','cafeidea','memory'],
44:['major','choice','futureplan','study','career','interest','school','decide2'],
45:['sciencefair','experiment','problem','result','because','solution','school','retry'],
46:['donation','donate','volunteer','community','help','customer','event','together'],
47:['promotion_job','responsibility','career','work','manager','futureplan','project','team'],
48:['anniversary','memory','customer','thanks','cafeidea','friend','year','happy'],
49:['familyfuture','futureplan','career','cafeidea','study','dream','family','decide2'],
50:['movingidea','grandparents','futureplan','farm','citylife','family','decide2','hope']
}

# Aliases to existing vocabulary keys where helpful.
ALIASES = {
'colleague':'newcolleague','school':'teacher','idea':'planword','government':'center','table':'oldtable','story':'past',
'interview':'review','money':'budget','children':'family','purpose':'planword','routine':'routine','coffee':'coffeemachine',
'offer':'discount','ticket':'buscard','hotel':'reservation','travel':'businesstrip','wrong':'wrongfile','explain':'clarify',
'meeting':'familymeeting','advice':'help','busy':'work','because':'because','team':'project_team','walk':'walk','life':'life',
'month':'month','interest':'hobby','manager':'manager','year':'year','happy':'happy'
}
for k,v in list(ALIASES.items()):
    if k not in W and v in W: W[k]=W[v]

# Grammatical behavior classes for natural template insertion.
ACTION3=set(getattr(h2,'ACTION_KEYS',set())) | {
 'replace','confirm','clarify','compare2','decide2','renovation','score','pricing','correct_word','repair','paidshift','smalltalk','promotion','businesstrip','presentation','mediate','donate'
}
PERSON3=set(getattr(h2,'PERSON_KEYS',set())) | {'applicant','realcustomer','project_team','supplier'}
PLACE3=set(getattr(h2,'PLACE_KEYS',set())) | {'premises','location','corner_shop'}
STATE3=set(getattr(h2,'STATE_KEYS',set())) | {'memorable','broken','disappointed'}
ABSTRACT3=set(getattr(h2,'ABSTRACT_KEYS',set())) | {
 'order','order_list','complaint','project','task','schooltrip','permission','rule','cafeidea','business','futureplan','advantage','disadvantage','rent','potential','familymeeting','risk','benefit','cafename','permit','officialdoc','measure','experience','workhours','trialopen','service','detailedorder','responsibility','homeworkcorner','regular','discount','reservation','roomtype','result','examstress','studyplan','tryout','argument','festivalstall','bulkorder','deliverytime','promotion_job','career','dream','regret','earlyretire','longterm','accountbook','income','expense','countryside','citylife','familyrecipe','tradition','major','choice','sciencefair','experiment','donation','anniversary','memory','familyfuture','movingidea','solution','schedule'
}
SPECIAL3={
 'because':('因为我们想把事情做好，所以要多准备一点。','Yīnwèi wǒmen xiǎng bǎ shìqing zuò hǎo, suǒyǐ yào duō zhǔnbèi yìdiǎn.','İşi iyi yapmak istediğimiz için biraz daha hazırlık yapmalıyız.'),
 'coffeemachine':('咖啡机刚才突然停了。','Kāfēijī gāngcái tūrán tíng le.','Kahve makinesi az önce aniden durdu.'),
 'flour':('面粉快用完了。','Miànfěn kuài yòng wán le.','Un neredeyse bitti.'),
 'grandparents':('也要听听爷爷奶奶的想法。','Yě yào tīngting yéye nǎinai de xiǎngfa.','Büyükanne ve büyükbabanın fikrini de dinlemeliyiz.'),
 'earlyretire':('张伟开始认真考虑提前退休。','Zhāng Wěi kāishǐ rènzhēn kǎolǜ tíqián tuìxiū.','Zhang Wei erken emekliliği ciddi biçimde düşünmeye başladı.'),
 'movingidea':('爷爷奶奶开始认真考虑搬到这里来。','Yéye nǎinai kāishǐ rènzhēn kǎolǜ bān dào zhèlǐ lái.','Büyükanne ve büyükbaba buraya taşınmayı ciddi biçimde düşünmeye başladı.'),
 'realcustomer':('今天终于来了一位正式顾客。','Jīntiān zhōngyú lái le yí wèi zhèngshì gùkè.','Bugün sonunda gerçek bir müşteri geldi.'),
 'order':('今天的订单比昨天多。','Jīntiān de dìngdān bǐ zuótiān duō.','Bugünkü siparişler dünkünden daha fazla.'),
 'complaint':('有一位顾客打电话来投诉。','Yǒu yí wèi gùkè dǎ diànhuà lái tóusù.','Bir müşteri şikâyet etmek için telefon etti.'),
 'project':('张伟今天开始参加一个新项目。','Zhāng Wěi jīntiān kāishǐ cānjiā yí ge xīn xiàngmù.','Zhang Wei bugün yeni bir projeye katılmaya başladı.'),
 'schooltrip':('雨桐正在准备学校旅行。','Yǔtóng zhèngzài zhǔnbèi xuéxiào lǚxíng.','Yutong okul gezisine hazırlanıyor.'),
 'newteacher':('乐乐今天见到了新老师。','Lèlè jīntiān jiàndào le xīn lǎoshī.','Lele bugün yeni öğretmeniyle tanıştı.'),
 'cafeidea':('大家开始认真谈咖啡馆的想法。','Dàjiā kāishǐ rènzhēn tán kāfēiguǎn de xiǎngfa.','Herkes kafe fikrini ciddi biçimde konuşmaya başladı.'),
 'premises':('他们今天要去看几个店面。','Tāmen jīntiān yào qù kàn jǐ ge diànmiàn.','Bugün birkaç dükkâna bakacaklar.'),
 'rent':('这个地方很好，可是房租太高。','Zhège dìfang hěn hǎo, kěshì fángzū tài gāo.','Burası çok iyi ama kira fazla yüksek.'),
 'corner_shop':('刘梅很喜欢这个老街角店铺。','Liú Méi hěn xǐhuan zhège lǎo jiējiǎo diànpù.','Liu Mei bu eski köşe dükkânını çok sevdi.'),
 'familymeeting':('晚上全家坐下来开了一个家庭会议。','Wǎnshang quánjiā zuò xiàlái kāi le yí ge jiātíng huìyì.','Akşam bütün aile oturup bir aile toplantısı yaptı.'),
 'cafename':('大家正在给咖啡馆想名字。','Dàjiā zhèngzài gěi kāfēiguǎn xiǎng míngzi.','Herkes kafeye isim düşünüyor.'),
 'permit':('刘梅今天要去办许可证。','Liú Méi jīntiān yào qù bàn xǔkězhèng.','Liu Mei bugün ruhsat işlemlerini yapacak.'),
 'renovation':('店里的装修今天正式开始。','Diàn lǐ de zhuāngxiū jīntiān zhèngshì kāishǐ.','Dükkânın tadilatı bugün resmen başladı.'),
 'secondhand':('他们看中了一张二手老桌子。','Tāmen kànzhòng le yì zhāng èrshǒu lǎo zhuōzi.','İkinci el eski bir masayı beğendiler.'),
 'menu':('今晚全家一起试菜单。','Jīnwǎn quánjiā yìqǐ shì càidān.','Bu akşam bütün aile menüyü birlikte deniyor.'),
 'cost':('刘梅和张伟正在算每样东西的成本。','Liú Méi hé Zhāng Wěi zhèngzài suàn měi yàng dōngxi de chéngběn.','Liu Mei ile Zhang Wei her ürünün maliyetini hesaplıyor.'),
 'applicant':('今天第一位应聘者来面试。','Jīntiān dì yí wèi yìngpìnzhě lái miànshì.','Bugün ilk iş adayı görüşmeye geldi.'),
 'signboard':('新招牌上有一个小错字。','Xīn zhāopai shàng yǒu yí ge xiǎo cuòzì.','Yeni tabelada küçük bir yazım hatası var.'),
 'trialopen':('今天咖啡馆第一次试营业。','Jīntiān kāfēiguǎn dì yí cì shì yíngyè.','Bugün kafenin ilk deneme açılışı.'),
 'repair':('张伟下班以后来帮忙维修。','Zhāng Wěi xiàbān yǐhòu lái bāngmáng wéixiū.','Zhang Wei işten sonra tamire yardım etmeye geldi.'),
 'paidshift':('雨桐今天第一次在咖啡馆打工。','Yǔtóng jīntiān dì yí cì zài kāfēiguǎn dǎgōng.','Yutong bugün ilk kez kafede ücretli çalışıyor.'),
 'homeworkcorner':('乐乐想在咖啡馆里留一个作业角。','Lèlè xiǎng zài kāfēiguǎn lǐ liú yí ge zuòyè jiǎo.','Lele kafede bir ödev köşesi ayırmak istiyor.'),
 'regular':('咖啡馆终于有了第一个常客。','Kāfēiguǎn zhōngyú yǒu le dì yí ge chángkè.','Kafenin sonunda ilk düzenli müşterisi oldu.'),
 'discount':('下雨天客人少，刘梅想做一个小优惠。','Xiàyǔ tiān kèrén shǎo, Liú Méi xiǎng zuò yí ge xiǎo yōuhuì.','Yağmurlu günde müşteri az olduğu için Liu Mei küçük bir kampanya yapmak istiyor.'),
 'businesstrip':('张伟要出差几天。','Zhāng Wěi yào chūchāi jǐ tiān.','Zhang Wei birkaç günlüğüne iş seyahatine çıkacak.'),
 'reservation':('到了酒店以后，张伟发现预订出了问题。','Dào le jiǔdiàn yǐhòu, Zhāng Wěi fāxiàn yùdìng chū le wèntí.','Otele varınca Zhang Wei rezervasyonda sorun olduğunu fark etti.'),
 'presentation':('张伟今天要在会上做工作汇报。','Zhāng Wěi jīntiān yào zài huì shàng zuò gōngzuò huìbào.','Zhang Wei bugün toplantıda iş sunumu yapacak.'),
 'examstress':('雨桐最近的考试压力越来越大。','Yǔtóng zuìjìn de kǎoshì yālì yuèláiyuè dà.','Yutong’un sınav stresi son günlerde giderek artıyor.'),
 'tryout':('乐乐这次没有通过球队选拔。','Lèlè zhè cì méiyǒu tōngguò qiúduì xuǎnbá.','Lele bu kez takım seçmelerini geçemedi.'),
 'argument':('咖啡馆里两个顾客因为桌子发生了小争执。','Kāfēiguǎn lǐ liǎng ge gùkè yīnwèi zhuōzi fāshēng le xiǎo zhēngzhí.','Kafede iki müşteri masa yüzünden küçük bir tartışma yaşadı.'),
 'festivalstall':('咖啡馆今天在街区节日摆摊。','Kāfēiguǎn jīntiān zài jiēqū jiérì bǎi tān.','Kafe bugün mahalle festivalinde stant açıyor.'),
 'bulkorder':('学校给咖啡馆下了第一个大订单。','Xuéxiào gěi kāfēiguǎn xià le dì yí ge dà dìngdān.','Okul kafeye ilk büyük siparişini verdi.'),
 'flour':('准备大订单的时候，面粉突然不够了。','Zhǔnbèi dà dìngdān de shíhou, miànfěn tūrán bú gòu le.','Büyük sipariş hazırlanırken un birden yetersiz kaldı.'),
 'promotion_job':('张伟听说自己可能要升职。','Zhāng Wěi tīngshuō zìjǐ kěnéng yào shēngzhí.','Zhang Wei terfi edebileceğini duydu.'),
 'dream':('张伟和李晨晚上边走边谈自己的梦想。','Zhāng Wěi hé Lǐ Chén wǎnshang biān zǒu biān tán zìjǐ de mèngxiǎng.','Zhang Wei ile Li Chen akşam yürürken hayallerini konuşuyor.'),
 'accountbook':('刘梅第一次认真整理咖啡馆的账本。','Liú Méi dì yí cì rènzhēn zhěnglǐ kāfēiguǎn de zhàngběn.','Liu Mei ilk kez kafenin hesap defterini ciddi biçimde düzenliyor.'),
 'countryside':('爷爷来住一段时间，也开始比较农村和城市生活。','Yéye lái zhù yí duàn shíjiān, yě kāishǐ bǐjiào nóngcūn hé chéngshì shēnghuó.','Büyükbaba bir süreliğine kalmaya geldi ve kırsal yaşamla şehir yaşamını karşılaştırmaya başladı.'),
 'familyrecipe':('奶奶今天教大家一道家传菜。','Nǎinai jīntiān jiāo dàjiā yí dào jiāchuán cài.','Büyükanne bugün herkese bir aile tarifini öğretiyor.'),
 'major':('雨桐开始认真考虑以后学什么专业。','Yǔtóng kāishǐ rènzhēn kǎolǜ yǐhòu xué shénme zhuānyè.','Yutong gelecekte hangi alanda okuyacağını ciddi biçimde düşünmeye başladı.'),
 'sciencefair':('乐乐的科学展项目突然不工作了。','Lèlè de kēxué zhǎn xiàngmù tūrán bù gōngzuò le.','Lele’nin bilim fuarı projesi birden çalışmamaya başladı.'),
 'donation':('咖啡馆今天成了社区募捐点。','Kāfēiguǎn jīntiān chéng le shèqū mùjuān diǎn.','Kafe bugün mahalle bağış noktası oldu.'),
 'anniversary':('大家正在准备咖啡馆一周年的小惊喜。','Dàjiā zhèngzài zhǔnbèi kāfēiguǎn yì zhōunián de xiǎo jīngxǐ.','Herkes kafenin birinci yılı için küçük bir sürpriz hazırlıyor.'),
 'familyfuture':('今晚全家坐下来谈未来。','Jīnwǎn quánjiā zuò xiàlái tán wèilái.','Bu akşam bütün aile oturup geleceği konuşuyor.'),
}

# Main recurring cast per scene.
ROLES = {}
for n in range(1,51):
    ROLES[n]=['刘梅','张伟','张雨桐','张乐乐']
for n in [1,2,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,33,34,35,36,40,43,46,48,49]:
    ROLES[n]=['刘梅','张伟','顾客','张雨桐']
for n in [3,30,37,47]: ROLES[n]=['张伟','经理','同事','刘梅']
for n in [4,31,44]: ROLES[n]=['张雨桐','老师','刘梅','张伟']
for n in [5,32,45]: ROLES[n]=['张乐乐','老师','张伟','刘梅']
for n in [28,29]: ROLES[n]=['张伟','工作人员','刘梅','同事']
for n in [38,39]: ROLES[n]=['张伟','李晨','刘梅']
for n in [41,42,43,50]: ROLES[n]=['张伟','刘梅','爷爷','奶奶']

COMMON = [
('我们先把情况说清楚。','Wǒmen xiān bǎ qíngkuàng shuō qīngchu.','Önce durumu netleştirelim.'),
('你的意思是这样，对吗？','Nǐ de yìsi shì zhèyàng, duì ma?','Demek istediğin bu, değil mi?'),
('对，我就是这个意思。','Duì, wǒ jiù shì zhège yìsi.','Evet, tam olarak bunu demek istiyorum.'),
('这件事比我想的复杂一点。','Zhè jiàn shì bǐ wǒ xiǎng de fùzá yìdiǎn.','Bu iş düşündüğümden biraz daha karmaşık.'),
('先别着急，我们一步一步来。','Xiān bié zháojí, wǒmen yí bù yí bù lái.','Önce telaşlanmayalım, adım adım ilerleyelim.'),
('我觉得这个办法比较合适。','Wǒ juéde zhège bànfǎ bǐjiào héshì.','Bence bu yöntem daha uygun.'),
('为什么你这么想？','Wèishénme nǐ zhème xiǎng?','Neden böyle düşünüyorsun?'),
('因为这样更方便，也更清楚。','Yīnwèi zhèyàng gèng fāngbiàn, yě gèng qīngchu.','Çünkü böyle hem daha kullanışlı hem de daha net.'),
('如果这样做，我们就能省一点时间。','Rúguǒ zhèyàng zuò, wǒmen jiù néng shěng yìdiǎn shíjiān.','Böyle yaparsak biraz zaman kazanabiliriz.'),
('虽然有点麻烦，但是可以解决。','Suīrán yǒudiǎn máfan, dànshì kěyǐ jiějué.','Biraz zahmetli olsa da çözülebilir.'),
('那我们先试试看。','Nà wǒmen xiān shìshikan.','O zaman önce deneyelim.'),
('好，有问题我们再调整。','Hǎo, yǒu wèntí wǒmen zài tiáozhěng.','Tamam, sorun olursa yeniden ayarlarız.'),
('我先确认一下细节。','Wǒ xiān quèrèn yíxià xìjié.','Önce ayrıntıları teyit edeyim.'),
('你说得对，这个细节很重要。','Nǐ shuō de duì, zhège xìjié hěn zhòngyào.','Haklısın, bu ayrıntı önemli.'),
('我们最好把时间也安排好。','Wǒmen zuìhǎo bǎ shíjiān yě ānpái hǎo.','Zamanı da iyi planlasak iyi olur.'),
('我已经写下来了。','Wǒ yǐjīng xiě xiàlái le.','Not aldım bile.'),
('那就不会忘了。','Nà jiù bú huì wàng le.','O zaman unutmayız.'),
('现在最重要的问题是什么？','Xiànzài zuì zhòngyào de wèntí shì shénme?','Şimdi en önemli sorun ne?'),
('关键是先找到原因。','Guānjiàn shì xiān zhǎodào yuányīn.','Önemli olan önce nedeni bulmak.'),
('我同意，不过我们还要考虑别的情况。','Wǒ tóngyì, búguò wǒmen hái yào kǎolǜ bié de qíngkuàng.','Katılıyorum ama başka durumları da düşünmeliyiz.'),
('这样说更有道理。','Zhèyàng shuō gèng yǒu dàolǐ.','Böyle söyleyince daha mantıklı.'),
('我们需要一个更实际的办法。','Wǒmen xūyào yí ge gèng shíjì de bànfǎ.','Daha uygulanabilir bir çözüme ihtiyacımız var.'),
('可以先做一部分，看看效果。','Kěyǐ xiān zuò yí bùfen, kànkan xiàoguǒ.','Önce bir kısmını yapıp sonucu görebiliriz.'),
('这个主意不错。','Zhège zhǔyi búcuò.','Bu fikir fena değil.'),
('那我负责这一部分。','Nà wǒ fùzé zhè yí bùfen.','O zaman bu kısmı ben üstleneyim.'),
('剩下的我来处理。','Shèngxià de wǒ lái chǔlǐ.','Kalanını ben hallederim.'),
('需要我帮忙的时候告诉我。','Xūyào wǒ bāngmáng de shíhou gàosu wǒ.','Yardıma ihtiyacın olduğunda bana söyle.'),
('好，我们保持联系。','Hǎo, wǒmen bǎochí liánxì.','Tamam, iletişimde kalalım.'),
('事情越来越清楚了。','Shìqing yuèláiyuè qīngchu le.','Durum giderek netleşiyor.'),
('我也放心多了。','Wǒ yě fàngxīn duō le.','Ben de çok daha rahatladım.'),
('还有一个小问题。','Hái yǒu yí ge xiǎo wèntí.','Bir küçük sorun daha var.'),
('你说吧，我们一起想办法。','Nǐ shuō ba, wǒmen yìqǐ xiǎng bànfǎ.','Söyle, birlikte çözüm düşünelim.'),
('这个问题其实不难。','Zhège wèntí qíshí bù nán.','Bu sorun aslında zor değil.'),
('只要准备好，就可以开始。','Zhǐyào zhǔnbèi hǎo, jiù kěyǐ kāishǐ.','Hazırlık tamam olursa başlayabiliriz.'),
('那我们现在开始吧。','Nà wǒmen xiànzài kāishǐ ba.','O zaman şimdi başlayalım.'),
('进行得比想象中顺利。','Jìnxíng de bǐ xiǎngxiàng zhōng shùnlì.','Düşündüğümüzden daha sorunsuz ilerliyor.'),
('中间还是出了一个小问题。','Zhōngjiān háishi chū le yí ge xiǎo wèntí.','Arada yine küçük bir sorun çıktı.'),
('没关系，先看看能不能调整。','Méi guānxi, xiān kànkan néng bu néng tiáozhěng.','Sorun değil, önce ayarlayıp ayarlayamayacağımıza bakalım.'),
('我有一个新的办法。','Wǒ yǒu yí ge xīn de bànfǎ.','Yeni bir çözümüm var.'),
('说来听听。','Shuō lái tīngting.','Anlat bakalım.'),
('我们可以一边做，一边检查。','Wǒmen kěyǐ yìbiān zuò, yìbiān jiǎnchá.','Yaparken aynı anda kontrol edebiliriz.'),
('这样发现问题会更早。','Zhèyàng fāxiàn wèntí huì gèng zǎo.','Böylece sorunları daha erken fark ederiz.'),
('好，就按这个办法来。','Hǎo, jiù àn zhège bànfǎ lái.','Tamam, bu yönteme göre ilerleyelim.'),
('你看，现在好多了。','Nǐ kàn, xiànzài hǎo duō le.','Bak, şimdi çok daha iyi.'),
('确实，比刚才顺利。','Quèshí, bǐ gāngcái shùnlì.','Gerçekten, az öncekinden daha iyi gidiyor.'),
('看来我们的方向是对的。','Kànlái wǒmen de fāngxiàng shì duì de.','Görünüşe göre doğru yöndeyiz.'),
('最后再检查一遍吧。','Zuìhòu zài jiǎnchá yí biàn ba.','Son olarak bir kez daha kontrol edelim.'),
('好的，我来检查第一部分。','Hǎo de, wǒ lái jiǎnchá dì yí bùfen.','Tamam, ilk kısmı ben kontrol edeyim.'),
('我负责后面的部分。','Wǒ fùzé hòumiàn de bùfen.','Ben sonraki kısmı kontrol ederim.'),
('现在没有发现新的问题。','Xiànzài méiyǒu fāxiàn xīn de wèntí.','Şu anda yeni bir sorun görünmüyor.'),
('太好了，终于可以放心了。','Tài hǎo le, zhōngyú kěyǐ fàngxīn le.','Harika, sonunda rahatlayabiliriz.'),
('今天我们学到不少东西。','Jīntiān wǒmen xuédào bù shǎo dōngxi.','Bugün epey şey öğrendik.'),
('下次处理起来会更快。','Xià cì chǔlǐ qǐlái huì gèng kuài.','Bir dahaki sefere daha hızlı hallederiz.'),
('我觉得今天的结果不错。','Wǒ juéde jīntiān de jiéguǒ búcuò.','Bence bugünkü sonuç iyi.'),
('我也是这么想的。','Wǒ yě shì zhème xiǎng de.','Ben de öyle düşünüyorum.'),
('那就这么决定吧。','Nà jiù zhème juédìng ba.','O zaman böyle karar verelim.'),
('好，接下来按计划继续。','Hǎo, jiēxiàlái àn jìhuà jìxù.','Tamam, bundan sonra plana göre devam edelim.'),
]

# Scene-specific opening/problem/resolution lines using each blueprint title and Turkish mini-adventure.
def natural_intro(key):
    if key in SPECIAL3: return SPECIAL3[key]
    zh,py,tr=W[key]
    if key in ACTION3:
        return (f'今天我们先{zh}。',f'Jīntiān wǒmen xiān {py}.',f'Bugün önce {tr}.')
    if key in PERSON3:
        return (f'今天要先跟{zh}谈一谈。',f'Jīntiān yào xiān gēn {py} tán yì tán.',f'Bugün önce {tr} ile konuşmamız gerekiyor.')
    if key in PLACE3:
        return (f'今天我们要先看看{zh}。',f'Jīntiān wǒmen yào xiān kànkan {py}.',f'Bugün önce {tr} konusuna bakalım.')
    if key in STATE3:
        return (f'现在的情况有点{zh}。',f'Xiànzài de qíngkuàng yǒudiǎn {py}.',f'Şu anki durum biraz {tr}.')
    if key in ABSTRACT3:
        return (f'今天我们先谈谈{zh}。',f'Jīntiān wǒmen xiān tántan {py}.',f'Bugün önce {tr} hakkında konuşalım.')
    return (f'今天先确认一下{zh}。',f'Jīntiān xiān quèrèn yíxià {py}.',f'Bugün önce {tr} konusunu teyit edelim.')


def context_lines(scene, keys):
    # First line is deliberately scene-specific. The next lines establish a natural HSK3 problem-solving arc.
    first=natural_intro(keys[0])
    second=natural_intro(keys[1])
    return [
      first,
      second,
      ('情况跟我们开始想的不完全一样。','Qíngkuàng gēn wǒmen kāishǐ xiǎng de bù wánquán yíyàng.','Durum başta düşündüğümüzle tamamen aynı değil.'),
      ('那我们先听听大家的意见。','Nà wǒmen xiān tīngting dàjiā de yìjiàn.','O zaman önce herkesin fikrini dinleyelim.'),
      ('我觉得先把重点找出来比较好。','Wǒ juéde xiān bǎ zhòngdiǎn zhǎo chūlái bǐjiào hǎo.','Bence önce ana noktayı belirlemek daha iyi.'),
      ('好，先把最需要处理的事情解决。','Hǎo, xiān bǎ zuì xūyào chǔlǐ de shìqing jiějué.','Tamam, önce en çok çözülmesi gereken işi halledelim.'),
    ]


def usage_line(key, variant=0):
    if key in SPECIAL3 and variant % 5 == 0:
        return SPECIAL3[key]
    zh,py,tr=W[key]
    if key in ACTION3:
        pats=[
          (f'我们先{zh}，然后再看下一步。',f'Wǒmen xiān {py}, ránhòu zài kàn xià yí bù.',f'Önce {tr}, sonra sonraki adıma bakarız.'),
          (f'这个时候最好先{zh}。',f'Zhège shíhou zuìhǎo xiān {py}.',f'Bu durumda önce {tr} en iyisi.'),
          (f'如果现在{zh}，会更方便。',f'Rúguǒ xiànzài {py}, huì gèng fāngbiàn.',f'Şimdi {tr} daha kullanışlı olur.'),
          (f'我已经准备好{zh}了。',f'Wǒ yǐjīng zhǔnbèi hǎo {py} le.',f'{tr.capitalize()} için hazırım.'),
          (f'这一步需要认真{zh}。',f'Zhè yí bù xūyào rènzhēn {py}.',f'Bu adımda dikkatlice {tr} gerekiyor.'),
        ]
    elif key in PERSON3:
        pats=[
          (f'我们先听听{zh}怎么说。',f'Wǒmen xiān tīngting {py} zěnme shuō.',f'Önce {tr} ne diyor dinleyelim.'),
          (f'这件事还要跟{zh}确认。',f'Zhè jiàn shì hái yào gēn {py} quèrèn.',f'Bu konuyu {tr} ile de teyit etmek gerekiyor.'),
          (f'{zh}的意见也很重要。',f'{py.capitalize()} de yìjiàn yě hěn zhòngyào.',f'{tr.capitalize()} görüşü de önemli.'),
          (f'等{zh}来了以后再决定。',f'Děng {py} lái le yǐhòu zài juédìng.',f'{tr.capitalize()} geldikten sonra karar verelim.'),
          (f'我已经跟{zh}说过了。',f'Wǒ yǐjīng gēn {py} shuōguo le.',f'{tr.capitalize()} ile zaten konuştum.'),
        ]
    elif key in PLACE3:
        pats=[
          (f'这个{zh}看起来比较合适。',f'Zhège {py} kàn qǐlái bǐjiào héshì.',f'Bu {tr} oldukça uygun görünüyor.'),
          (f'我们再看看{zh}的情况。',f'Wǒmen zài kànkan {py} de qíngkuàng.',f'{tr.capitalize()} durumuna bir kez daha bakalım.'),
          (f'{zh}的位置很重要。',f'{py.capitalize()} de wèizhi hěn zhòngyào.',f'{tr.capitalize()} konumu önemli.'),
          (f'如果选这个{zh}，以后会方便一些。',f'Rúguǒ xuǎn zhège {py}, yǐhòu huì fāngbiàn yìxiē.',f'Bu {tr} seçilirse ileride daha kullanışlı olur.'),
          (f'这个{zh}还有一个优点。',f'Zhège {py} hái yǒu yí ge yōudiǎn.',f'Bu {tr} bir avantajı daha var.'),
        ]
    elif key in STATE3:
        pats=[
          (f'现在看起来有点{zh}。',f'Xiànzài kàn qǐlái yǒudiǎn {py}.',f'Şimdi biraz {tr} görünüyor.'),
          (f'别担心，{zh}的问题可以慢慢解决。',f'Bié dānxīn, {py} de wèntí kěyǐ mànmàn jiějué.',f'Endişelenme, {tr} ile ilgili sorun yavaş yavaş çözülebilir.'),
          (f'跟刚才比，现在没那么{zh}了。',f'Gēn gāngcái bǐ, xiànzài méi nàme {py} le.',f'Az öncesine göre artık o kadar {tr} değil.'),
          (f'这个情况越来越{zh}。',f'Zhège qíngkuàng yuèláiyuè {py}.',f'Bu durum giderek daha {tr} hale geliyor.'),
          (f'我们要注意别让情况太{zh}。',f'Wǒmen yào zhùyì bié ràng qíngkuàng tài {py}.',f'Durumun fazla {tr} olmamasına dikkat etmeliyiz.'),
        ]
    else:
        # Concepts/items: talk about, compare, record, verify rather than blindly inserting into verb frames.
        pats=[
          (f'关于{zh}，我们还要再讨论一下。',f'Guānyú {py}, wǒmen hái yào zài tǎolùn yíxià.',f'{tr.capitalize()} konusunda biraz daha konuşmalıyız.'),
          (f'我已经把{zh}记下来了。',f'Wǒ yǐjīng bǎ {py} jì xiàlái le.',f'{tr.capitalize()} notunu aldım.'),
          (f'{zh}是这次要考虑的重点之一。',f'{py.capitalize()} shì zhè cì yào kǎolǜ de zhòngdiǎn zhī yī.',f'{tr.capitalize()} bu kez değerlendirmemiz gereken ana noktalardan biri.'),
          (f'我们最好再确认一下{zh}。',f'Wǒmen zuìhǎo zài quèrèn yíxià {py}.',f'{tr.capitalize()} konusunu bir kez daha teyit etsek iyi olur.'),
          (f'如果{zh}没有问题，我们就继续。',f'Rúguǒ {py} méiyǒu wèntí, wǒmen jiù jìxù.',f'{tr.capitalize()} konusunda sorun yoksa devam ederiz.'),
        ]
    return pats[variant % len(pats)]

def make_dialogues(scene):
    n=scene['number']; keys=V[n]; roles=ROLES[n]
    lines=[]
    lines.extend(context_lines(scene,keys))
    # Introduce scene vocabulary naturally.
    for i,k in enumerate(keys[:6]):
        lines.append(usage_line(k,i))
        if i%2==0: lines.append(('我明白你的意思了。','Wǒ míngbai nǐ de yìsi le.','Ne demek istediğini anladım.'))
        else: lines.append(('好，这一点我会注意。','Hǎo, zhè yìdiǎn wǒ huì zhùyì.','Tamam, bu noktaya dikkat edeceğim.'))
    # HSK3 connected dialogue bank.
    lines.extend(COMMON)
    # Recycle scene words with different grammatical frames until 94 turns.
    idx=0
    responses=[
      ('这个安排比较实际。','Zhège ānpái bǐjiào shíjì.','Bu düzenleme oldukça uygulanabilir.'),
      ('我觉得可以接受。','Wǒ juéde kěyǐ jiēshòu.','Bence kabul edilebilir.'),
      ('这样的话就清楚多了。','Zhèyàng de huà jiù qīngchu duō le.','Böyle olunca çok daha net.'),
      ('对，我们继续看下一项。','Duì, wǒmen jìxù kàn xià yí xiàng.','Evet, sıradaki maddeye bakalım.'),
      ('这一点以后还会用到。','Zhè yìdiǎn yǐhòu hái huì yòngdào.','Bu nokta ileride yine işimize yarayacak.'),
    ]
    while len(lines)<94:
        k=keys[idx%len(keys)]
        lines.append(usage_line(k,idx+1))
        lines.append(responses[idx%len(responses)])
        idx+=1
    lines=lines[:94]
    lines += [
      ('现在主要问题已经解决了。','Xiànzài zhǔyào wèntí yǐjīng jiějué le.','Ana sorun artık çözüldü.'),
      ('剩下的按计划做就可以。','Shèngxià de àn jìhuà zuò jiù kěyǐ.','Kalanını plana göre yapmamız yeterli.'),
      ('今天的经验很有用。','Jīntiān de jīngyàn hěn yǒuyòng.','Bugünkü deneyim çok faydalı.'),
      ('下次我们会准备得更好。','Xià cì wǒmen huì zhǔnbèi de gèng hǎo.','Bir dahaki sefere daha iyi hazırlanacağız.'),
      ('好，今天就先到这里。','Hǎo, jīntiān jiù xiān dào zhèlǐ.','Tamam, bugünlük burada bitirelim.'),
      ('明天继续。','Míngtiān jìxù.','Yarın devam ederiz.'),
    ]
    lines=lines[:100]
    return [
      {'id':f'DLG_ZH_HSK3_SC{n:03d}_{i:03d}','speaker':roles[(i-1)%len(roles)],'zh':zh,'pinyin':py,'tr':tr}
      for i,(zh,py,tr) in enumerate(lines,1)
    ]

def make_cards(scene):
    n=scene['number']; cards=[]
    for i,key in enumerate(V[n],1):
        zh,py,tr=W[key]; ezh,epy,etr=usage_line(key,i)
        cards.append({'id':f'VOC_ZH_HSK3_SC{n:03d}_{i:03d}','zh':zh,'pinyin':py,'tr':tr,'exampleZh':ezh,'examplePinyin':epy,'exampleTr':etr,'kind':'active' if i<=6 else 'review'})
    return cards

def grammar_items(scene):
    n=scene['number']; keys=V[n]; a,b,c=[W[k] for k in keys[:3]]; g=scene['learning'].get('grammarTheme','')
    if '因为' in g:
        base=[
          {'type':'word_order','tokens':['因为',a[0],'所以',b[0]],'answerTokens':['因为',a[0],'所以',b[0]]},
          {'type':'fill_blank','blankSentenceZh':'因为时间不够，___我们要重新安排。','options':['所以','但是','然后'],'answer':'所以'},
          {'type':'sentence_repair','tokens':['所以','更方便','因为','这样做'],'answerTokens':['因为','这样做','所以','更方便']}]
    elif '如果' in g:
        base=[
          {'type':'word_order','tokens':['如果',a[0],'没问题','就','继续'], 'answerTokens':['如果',a[0],'没问题','就','继续']},
          {'type':'fill_blank','blankSentenceZh':'如果准备好了，___可以开始。','options':['就','但是','因为'],'answer':'就'},
          {'type':'sentence_repair','tokens':['就','我们','如果','有时间','再检查'],'answerTokens':['如果','有时间','我们','就','再检查']}]
    elif '虽然' in g:
        base=[
          {'type':'word_order','tokens':['虽然',a[0],'有点难','但是','可以解决'],'answerTokens':['虽然',a[0],'有点难','但是','可以解决']},
          {'type':'fill_blank','blankSentenceZh':'虽然有点麻烦，___我们有办法。','options':['但是','所以','如果'],'answer':'但是'},
          {'type':'sentence_repair','tokens':['但是','值得试','虽然','有风险'],'answerTokens':['虽然','有风险','但是','值得试']}]
    elif '一边' in g:
        base=[
          {'type':'word_order','tokens':['我们','一边','准备','一边','检查'],'answerTokens':['我们','一边','准备','一边','检查']},
          {'type':'fill_blank','blankSentenceZh':'我们一边讨论，___记录。','options':['一边','所以','如果'],'answer':'一边'},
          {'type':'sentence_repair','tokens':['一边','工作','一边','学习','他'],'answerTokens':['他','一边','工作','一边','学习']}]
    elif '越来越' in g:
        base=[
          {'type':'word_order','tokens':['事情','越来越','清楚','了'],'answerTokens':['事情','越来越','清楚','了']},
          {'type':'fill_blank','blankSentenceZh':'生意___好了。','options':['越来越','因为','如果'],'answer':'越来越'},
          {'type':'sentence_repair','tokens':['越来越','问题','少','了'],'answerTokens':['问题','越来越','少','了']}]
    else: # 先…然后…
        base=[
          {'type':'word_order','tokens':['先',a[0],'然后',b[0]],'answerTokens':['先',a[0],'然后',b[0]]},
          {'type':'fill_blank','blankSentenceZh':'我们先确认，___再决定。','options':['然后','因为','虽然'],'answer':'然后'},
          {'type':'sentence_repair','tokens':['然后','开始','先','准备'],'answerTokens':['先','准备','然后','开始']}]
    out=[]
    prompt={'word_order':'Kelimeleri doğru sıraya koy.','fill_blank':'Boşluğu doğru kelimeyle doldur.','sentence_repair':'Yanlış sıradaki cümleyi düzelt.'}
    for i in range(9):
        item=dict(base[i%3]); item['id']=f'SENT_ZH_HSK3_SC{n:03d}_{i+1:03d}'; item['promptTr']=prompt[item['type']]; out.append(item)
    return out

def make_comprehension(scene):
    n=scene['number']
    return [
      {'id':f'COMP_ZH_HSK3_SC{n:03d}_001','questionTr':'Bu sahnenin ana konusu hangisidir?','optionsTr':[scene['titleTr'],'Bir uzay yolculuğu','Bir tarih sınavı'],'correctIndex':0},
      {'id':f'COMP_ZH_HSK3_SC{n:03d}_002','questionTr':'Karakterler yalnızca bilgi mi veriyor, yoksa bir karar/sorun üzerinde de çalışıyor mu?','optionsTr':['Bir karar veya sorun üzerinde çalışıyorlar','Sadece sayıları sayıyorlar','Hiç konuşmuyorlar'],'correctIndex':0},
      {'id':f'COMP_ZH_HSK3_SC{n:03d}_003','questionTr':'Sahnede neden-sonuç, koşul veya karşılaştırma gibi bağlantılı dil kullanılıyor mu?','optionsTr':['Evet','Hayır','Sadece isimler var'],'correctIndex':0},
      {'id':f'COMP_ZH_HSK3_SC{n:03d}_004','questionTr':'Bu olay Zhang ailesinin hangi dönemine aittir?','optionsTr':['Kasabada kök salıp kafe fikrini geliştirdikleri dönem','Kasabaya ilk geldikleri gün','Yaşlılık dönemi'],'correctIndex':0},
      {'id':f'COMP_ZH_HSK3_SC{n:03d}_005','questionTr':'Sahnenin sonunda karakterler ortak bir çözüm veya sonraki adım belirliyor mu?','optionsTr':['Evet','Hayır','Belli değil'],'correctIndex':0},
    ]

def make_pron(scene,cards):
    n=scene['number']
    return [{'id':f'PRON_ZH_HSK3_SC{n:03d}_{i:03d}','zh':c['exampleZh'],'pinyin':c['examplePinyin'],'tr':c['exampleTr'],'scoring':['pronunciation','toneAccuracy','fluency','timing','completeness']} for i,c in enumerate(cards[:5],1)]

def make_interactive(scene):
    n=scene['number']; a=W[V[n][0]]; b=W[V[n][1]]
    return [
      {'id':f'INT_ZH_HSK3_SC{n:03d}_001','promptZh':'你觉得现在应该怎么办？','promptPinyin':'Nǐ juéde xiànzài yīnggāi zěnme bàn?','promptTr':'Sence şimdi ne yapmalıyız?','options':[{'zh':'我觉得先把情况确认清楚。','tr':'Bence önce durumu net biçimde teyit etmeliyiz.','correct':True},{'zh':'我昨天吃了三个苹果。','tr':'Dün üç elma yedim.','correct':False},{'zh':'他的书在桌子下面。','tr':'Onun kitabı masanın altında.','correct':False}]},
      {'id':f'INT_ZH_HSK3_SC{n:03d}_002','promptZh':f'关于{a[0]}，你怎么看？','promptPinyin':f'Guānyú {a[1]}, nǐ zěnme kàn?','promptTr':f'{a[2].capitalize()} hakkında ne düşünüyorsun?','options':[{'zh':'我觉得先比较一下比较好。','tr':'Bence önce karşılaştırmak daha iyi.','correct':True},{'zh':'今天星期二。','tr':'Bugün salı.','correct':False},{'zh':'我家有一只猫。','tr':'Evde bir kedim var.','correct':False}]},
      {'id':f'INT_ZH_HSK3_SC{n:03d}_003','promptZh':'为什么要这样安排？','promptPinyin':'Wèishénme yào zhèyàng ānpái?','promptTr':'Neden böyle planlamalıyız?','options':[{'zh':'因为这样更清楚，也更方便。','tr':'Çünkü böyle daha net ve daha kullanışlı.','correct':True},{'zh':'因为我有两支笔。','tr':'Çünkü iki kalemim var.','correct':False},{'zh':'在公园左边。','tr':'Parkın solunda.','correct':False}]},
      {'id':f'INT_ZH_HSK3_SC{n:03d}_004','promptZh':'如果还有问题呢？','promptPinyin':'Rúguǒ hái yǒu wèntí ne?','promptTr':'Başka sorun kalırsa ne olacak?','options':[{'zh':'我们就再调整一次。','tr':'O zaman bir kez daha ayarlarız.','correct':True},{'zh':'我喜欢蓝色。','tr':'Mavi rengi seviyorum.','correct':False},{'zh':'八点半。','tr':'Saat sekiz buçuk.','correct':False}]},
    ]

def make_production(scene):
    n=scene['number']; return {
      'scenePurposeTr':scene.get('miniAdventureTr',''),
      'timeOfDay':'evening' if n in [11,12,38,39,49,50] else 'day',
      'atmosphere':'sıcak, doğal, hikâye odaklı ve HSK3 seviyesinde bağlantılı günlük Mandarin',
      'characters':ROLES[n], 'locationId':scene.get('locationId',''),
      'visual':{'reuseLocation':True,'newVisualRequired':False,'style':'visual_novel_theatre'},
      'audio':{'voiceLanguage':'zh-CN','narratorProfile':'NARRATOR_ZH_001','defaultSpeechSpeed':0.90},
      'animation':{'level':'normal','mouthMode':'AUTO_SIMPLE','blink':True,'speakerFocus':True},
      'continuityNoteTr':f"{scene['titleTr']} olayı HSK3 yaşam çizgisinde sahne {n} olarak kaydedilir; kafe, iş, okul ve aile sürekliliği sonraki sahnelere aktarılır."
    }

def main():
    data=json.loads(PATH.read_text(encoding='utf-8'))
    assert len(data['scenes'])==50
    for scene in data['scenes']:
        n=scene['number']; cards=make_cards(scene); learning=dict(scene.get('learning') or {})
        learning.update({
          'vocabularyCards':cards,
          'sentenceExercises':grammar_items(scene),
          'comprehensionQuestions':make_comprehension(scene),
          'pronunciationItems':make_pron(scene,cards),
          'interactiveDialogue':make_interactive(scene),
          'examRules':{'vocabularyPassPercent':90,'sentencePassPercent':85,'lockNextSceneUntilPassed':True},
          'examStages':[{'stage':1,'type':'vocabulary','passPercent':90},{'stage':2,'type':'sentence','passPercent':85,'requiresStage':1}],
          'flashCardPolicy':{'allowPrevious':True,'allowNext':True,'allowFavorite':True,'favoritesStudyMode':True}
        })
        scene['learning']=learning
        scene['dialogues']=make_dialogues(scene)
        scene['production']=make_production(scene)
        scene['complete']=True
        scene['productionStatus']='complete'
        scene['editorialStatus']='generated_full_v1_requires_native_review'
        scene['dialogueCount']=len(scene['dialogues'])
    data['schemaVersion']=3
    data['completeSceneCount']=50
    data['editorialNoteTr']='HSK3 50 sahne veri olarak tamdır; doğal Mandarin, kültürel/pragmatik kullanım ve ticari yayın öncesi native editör kontrolü önerilir.'
    PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('HSK3 authoring completed:',len(data['scenes']),'scenes,',sum(len(s['dialogues']) for s in data['scenes']),'dialogues')

if __name__=='__main__': main()
