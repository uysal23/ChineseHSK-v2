#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate HSK6 full production payload for all 50 scenes.

Deterministic/offline generator. HSK6 emphasizes nuanced pragmatic language, rhetoric,
inter-generational storytelling, cultural memory, crisis communication, aging, legacy,
belonging and reflective life themes. Generated language is data-complete and remains
explicitly flagged for native/editorial review before commercial publication.
"""
from __future__ import annotations
import importlib.util, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'authoring'/'hsk6_blueprints.json'
spec=importlib.util.spec_from_file_location('h5gen',ROOT/'scripts'/'fill_hsk5_complete.py')
h5=importlib.util.module_from_spec(spec); spec.loader.exec_module(h5)

# Scene-specific advanced concepts: (Chinese, tone-marked pinyin, Turkish)
T={
1:[('订婚','dìnghūn','nişanlanmak'),('婚讯','hūnxùn','evlilik/nişan haberi'),('祝福','zhùfú','iyi dilek / kutlama'),('人生阶段','rénshēng jiēduàn','yaşam evresi')],
2:[('正式见面','zhèngshì jiànmiàn','resmî tanışma'),('礼节','lǐjié','görgü / protokol'),('分寸','fēncùn','ölçülülük / sosyal sınır'),('家庭期待','jiātíng qīdài','aile beklentisi')],
3:[('婚礼预算','hūnlǐ yùsuàn','düğün bütçesi'),('妥协','tuǒxié','uzlaşma / taviz'),('分歧','fēnqí','görüş ayrılığı'),('共识','gòngshí','ortak anlayış')],
4:[('传统','chuántǒng','gelenek'),('简约','jiǎnyuē','sadelik'),('仪式感','yíshìgǎn','tören/ritüel hissi'),('象征意义','xiàngzhēng yìyì','sembolik anlam')],
5:[('往事','wǎngshì','geçmiş anılar'),('婚俗','hūnsú','düğün gelenekleri'),('时代背景','shídài bèijǐng','dönemin bağlamı'),('回忆','huíyì','anı / hatıra')],
6:[('场地合同','chǎngdì hétóng','mekân sözleşmesi'),('违约','wéiyuē','sözleşme ihlali'),('备用方案','bèiyòng fāng’àn','yedek plan'),('协商','xiéshāng','müzakere etmek')],
7:[('婚礼仪式','hūnlǐ yíshì','düğün töreni'),('誓言','shìyán','yemin / söz'),('宾客','bīnkè','davetliler'),('祝酒','zhùjiǔ','kadeh kaldırıp kutlamak')],
8:[('致辞','zhìcí','konuşma / hitap'),('修辞','xiūcí','retorik'),('回顾','huígù','geriye dönük değerlendirme'),('祝愿','zhùyuàn','iyi dilek')],
9:[('空巢','kōngcháo','boş yuva dönemi'),('失落感','shīluògǎn','boşluk / kayıp hissi'),('适应','shìyìng','uyum sağlamak'),('生活节奏','shēnghuó jiézòu','yaşam ritmi')],
10:[('毕业','bìyè','mezuniyet'),('职业身份','zhíyè shēnfèn','mesleki kimlik'),('选择','xuǎnzé','seçim'),('新起点','xīn qǐdiǎn','yeni başlangıç')],
11:[('摄影师','shèyǐngshī','fotoğrafçı'),('创作风格','chuàngzuò fēnggé','yaratıcı üslup'),('客户定位','kèhù dìngwèi','müşteri konumlandırması'),('专业化','zhuānyèhuà','profesyonelleşme')],
12:[('商业委托','shāngyè wěituō','ticari iş / komisyon'),('需求边界','xūqiú biānjiè','talep kapsamı ve sınırları'),('报价','bàojià','fiyat teklifi'),('合作条款','hézuò tiáokuǎn','işbirliği şartları')],
13:[('著作权','zhùzuòquán','telif hakkı'),('授权','shòuquán','lisans / yetkilendirme'),('使用范围','shǐyòng fànwéi','kullanım kapsamı'),('署名','shǔmíng','eser sahibini belirtme')],
14:[('退休公告','tuìxiū gōnggào','emeklilik duyurusu'),('职业生涯','zhíyè shēngyá','kariyer yaşamı'),('交接','jiāojiē','devir teslim'),('告别','gàobié','veda')],
15:[('离职','lízhí','işten ayrılma'),('同事情谊','tóngshì qíngyì','iş arkadaşı dostluğu'),('感谢','gǎnxiè','teşekkür'),('经验传承','jīngyàn chuánchéng','deneyim aktarımı')],
16:[('职业总结','zhíyè zǒngjié','kariyer özeti'),('成就','chéngjiù','başarı'),('遗憾','yíhàn','pişmanlık / ukde'),('经验','jīngyàn','deneyim')],
17:[('角色转换','juésè zhuǎnhuàn','rol değişimi'),('适应期','shìyìngqī','uyum dönemi'),('咖啡馆日常','kāfēiguǎn rìcháng','kafenin günlük işleri'),('新节奏','xīn jiézòu','yeni ritim')],
18:[('工作习惯','gōngzuò xíguàn','çalışma alışkanlığı'),('默契','mòqì','sözsüz uyum'),('幽默','yōumò','mizah'),('边界','biānjiè','sınır')],
19:[('分工','fēngōng','iş bölümü'),('责任','zérèn','sorumluluk'),('协作','xiézuò','işbirliği'),('夫妻关系','fūqī guānxì','eş ilişkisi')],
20:[('新菜单','xīn càidān','yeni menü'),('创新','chuàngxīn','yenilik'),('老味道','lǎo wèidào','eski/tanıdık lezzet'),('代际顾客','dàijì gùkè','farklı kuşak müşteriler')],
21:[('孕讯','yùnxùn','hamilelik haberi'),('祖辈','zǔbèi','büyükanne-büyükbaba kuşağı'),('喜悦','xǐyuè','sevinç'),('家庭变化','jiātíng biànhuà','ailede değişim')],
22:[('爷爷角色','yéye juésè','büyükbaba rolü'),('期待','qīdài','beklenti'),('焦虑','jiāolǜ','kaygı'),('代际责任','dàijì zérèn','kuşaklar arası sorumluluk')],
23:[('医院走廊','yīyuàn zǒuláng','hastane koridoru'),('等待','děngdài','bekleme'),('不确定性','bù quèdìngxìng','belirsizlik'),('安慰','ānwèi','teselli etmek')],
24:[('新生儿','xīnshēng’ér','yenidoğan'),('出生','chūshēng','doğum'),('亲情','qīnqíng','aile sevgisi'),('激动','jīdòng','yoğun heyecan')],
25:[('四世同堂','sì shì tóng táng','dört kuşağın bir arada olması'),('合影','héyǐng','birlikte fotoğraf'),('家族记忆','jiāzú jìyì','aile hafızası'),('时间感','shíjiāngǎn','zaman duygusu')],
26:[('农场往事','nóngchǎng wǎngshì','çiftlik anıları'),('农业变迁','nóngyè biànqiān','tarımın değişimi'),('劳作','láozuò','emek / çalışmak'),('乡土记忆','xiāngtǔ jìyì','memleket/kırsal hafıza')],
27:[('城镇化','chéngzhènhuà','kentleşme'),('老街','lǎojiē','eski sokak'),('便利','biànlì','kolaylık / erişilebilirlik'),('失去','shīqù','kaybetmek')],
28:[('周年纪念','zhōunián jìniàn','yıldönümü'),('品牌历史','pǐnpái lìshǐ','marka geçmişi'),('老顾客','lǎo gùkè','eski/düzenli müşteri'),('延续','yánxù','sürdürmek / devamlılık')],
29:[('重逢','chóngféng','yeniden buluşma'),('怀旧','huáijiù','nostalji'),('共同记忆','gòngtóng jìyì','ortak anılar'),('情感纽带','qínggǎn niǔdài','duygusal bağ')],
30:[('创业建议','chuàngyè jiànyì','girişimcilik tavsiyesi'),('导师','dǎoshī','mentor'),('风险意识','fēngxiǎn yìshí','risk farkındalığı'),('经验传递','jīngyàn chuándì','deneyim aktarma')],
31:[('职业观','zhíyèguān','kariyer anlayışı'),('成功定义','chénggōng dìngyì','başarı tanımı'),('选择成本','xuǎnzé chéngběn','seçimin bedeli'),('工作意义','gōngzuò yìyì','işin anlamı')],
32:[('创业工作坊','chuàngyè gōngzuòfāng','girişimcilik atölyesi'),('失败经验','shībài jīngyàn','başarısızlık deneyimi'),('现金流','xiànjīnliú','nakit akışı'),('顾客价值','gùkè jiàzhí','müşteri değeri')],
33:[('菜谱本','càipǔběn','tarif defteri'),('家传味道','jiāchuán wèidào','aileden gelen lezzet'),('手写记录','shǒuxiě jìlù','el yazısı kayıt'),('文化记忆','wénhuà jìyì','kültürel hafıza')],
34:[('数字化','shùzìhuà','dijitalleştirme'),('扫描','sǎomiáo','tarama'),('资料整理','zīliào zhěnglǐ','arşiv/doküman düzenleme'),('长期保存','chángqī bǎocún','uzun süreli koruma')],
35:[('社区花园','shèqū huāyuán','topluluk bahçesi'),('公共空间','gōnggòng kōngjiān','kamusal alan'),('可持续性','kě chíxùxìng','sürdürülebilirlik'),('志愿维护','zhìyuàn wéihù','gönüllü bakım')],
36:[('洪水预警','hóngshuǐ yùjǐng','sel uyarısı'),('应急预案','yìngjí yù’àn','acil durum planı'),('撤离','chèlí','tahliye'),('物资','wùzī','malzeme / yardım stoğu')],
37:[('救助中心','jiùzhù zhōngxīn','yardım merkezi'),('协调','xiétiáo','koordine etmek'),('志愿者','zhìyuànzhě','gönüllü'),('物资分配','wùzī fēnpèi','malzeme dağıtımı')],
38:[('灾后复盘','zāihòu fùpán','afet sonrası değerlendirme'),('韧性','rènxìng','dayanıklılık / dirençlilik'),('漏洞','lòudòng','açık / zayıf nokta'),('改进','gǎijìn','iyileştirme')],
39:[('退休身份','tuìxiū shēnfèn','emekli kimliği'),('友情','yǒuqíng','dostluk'),('空闲','kòngxián','boş zaman'),('新生活','xīn shēnghuó','yeni yaşam')],
40:[('老朋友','lǎo péngyou','eski dost'),('往事','wǎngshì','geçmiş anılar'),('时间跨度','shíjiān kuàdù','zaman aralığı'),('共同成长','gòngtóng chéngzhǎng','birlikte büyümek/gelişmek')],
41:[('健康警告','jiànkāng jǐnggào','sağlık uyarısı'),('风险指标','fēngxiǎn zhǐbiāo','risk göstergesi'),('检查','jiǎnchá','muayene / kontrol'),('生活方式','shēnghuó fāngshì','yaşam tarzı')],
42:[('慢生活','màn shēnghuó','yavaş yaşam'),('节奏','jiézòu','ritim'),('取舍','qǔshě','öncelik seçimi / vazgeçiş'),('生活质量','shēnghuó zhìliàng','yaşam kalitesi')],
43:[('孙辈','sūnbèi','torun kuşağı'),('好奇心','hàoqíxīn','merak'),('代沟','dàigōu','kuşak farkı'),('陪伴','péibàn','eşlik etmek / birlikte zaman geçirmek')],
44:[('婚礼','hūnlǐ','düğün'),('接纳','jiēnà','kabul etme'),('新成员','xīn chéngyuán','yeni aile üyesi'),('家庭边界','jiātíng biānjiè','aile sınırları')],
45:[('遗产','yíchǎn','miras'),('精神财富','jīngshén cáifù','manevi miras/değer'),('公平','gōngpíng','adalet'),('传承','chuánchéng','mirası aktarma')],
46:[('旧车票','jiù chēpiào','eski tren bileti'),('记忆触发','jìyì chùfā','anı tetikleyicisi'),('收藏','shōucáng','koleksiyon / saklamak'),('时间痕迹','shíjiān hénjì','zamanın izi')],
47:[('老车站','lǎo chēzhàn','eski istasyon'),('重访','chóngfǎng','yeniden ziyaret'),('今昔对照','jīnxī duìzhào','geçmiş-bugün karşılaştırması'),('物是人非','wù shì rén fēi','yer aynı olsa da insanların/zamanın değişmesi')],
48:[('大家庭','dà jiātíng','geniş aile'),('多代同堂','duō dài tóng táng','çok kuşağın bir arada olması'),('话题转换','huàtí zhuǎnhuàn','konu geçişi'),('家庭氛围','jiātíng fēnwéi','aile atmosferi')],
49:[('感恩','gǎn’ēn','şükran'),('遗憾','yíhàn','pişmanlık / ukde'),('幸福','xìngfú','mutluluk'),('人生意义','rénshēng yìyì','hayatın anlamı')],
50:[('归属感','guīshǔgǎn','aidiyet duygusu'),('家','jiā','ev / yuva'),('一生','yìshēng','bir ömür'),('圆满','yuánmǎn','tamamlanmışlık / huzurlu bütünlük')]
}

COMMON_TERMS=[
('语境','yǔjìng','bağlam'),('立场','lìchǎng','tutum / bakış açısı'),('权衡','quánhéng','dengeleyerek değerlendirmek'),('长期影响','chángqī yǐngxiǎng','uzun vadeli etki')]

ROLES={n:['张伟','刘梅','张雨桐','张乐乐'] for n in range(1,51)}
ROLES.update({
1:['张雨桐','伴侣','张伟','刘梅'],2:['张伟','刘梅','亲家','张雨桐'],3:['张雨桐','伴侣','刘梅','张伟'],4:['张伟','刘梅','张雨桐','奶奶'],5:['奶奶','张雨桐','刘梅','张伟'],6:['张雨桐','伴侣','场地方经理','刘梅'],7:['张雨桐','伴侣','张伟','刘梅'],8:['张伟','张雨桐','刘梅','宾客'],9:['张伟','刘梅','李晨','奶奶'],10:['张乐乐','张伟','刘梅','导师'],
11:['张乐乐','客户','刘梅','张伟'],12:['张乐乐','客户','助理','刘梅'],13:['张乐乐','客户','律师','刘梅'],14:['张伟','经理','同事','刘梅'],15:['张伟','同事','经理','李晨'],16:['张伟','刘梅','李晨','同事'],17:['张伟','刘梅','员工','顾客'],18:['刘梅','张伟','员工','顾客'],19:['张伟','刘梅','员工','李晨'],20:['刘梅','张伟','年轻顾客','老顾客'],
21:['张雨桐','伴侣','张伟','刘梅'],22:['张伟','刘梅','李晨','奶奶'],23:['张伟','刘梅','张雨桐伴侣','护士'],24:['张雨桐','伴侣','张伟','刘梅'],25:['张伟','刘梅','奶奶','张雨桐'],26:['爷爷','张伟','张乐乐','刘梅'],27:['张伟','刘梅','李晨','爷爷'],28:['刘梅','张伟','老顾客','员工'],29:['刘梅','老顾客','张伟','李晨'],30:['刘梅','年轻创业者','张伟','员工'],
31:['张伟','年轻人','刘梅','李晨'],32:['刘梅','创业者','张伟','主持人'],33:['奶奶','刘梅','张雨桐','张乐乐'],34:['张乐乐','刘梅','奶奶','技术志愿者'],35:['爷爷','社区居民','张乐乐','刘梅'],36:['张伟','刘梅','社区负责人','居民'],37:['刘梅','张伟','志愿者','社区负责人'],38:['张伟','刘梅','社区负责人','李晨'],39:['李晨','张伟','刘梅','朋友'],40:['张伟','刘梅','李晨','家人'],
41:['张伟','医生','刘梅','护士'],42:['张伟','刘梅','李晨','张雨桐'],43:['张伟','孙辈','刘梅','张雨桐'],44:['张乐乐','伴侣','张伟','刘梅'],45:['张伟','刘梅','张雨桐','张乐乐'],46:['张伟','刘梅','张乐乐','孙辈'],47:['张伟','刘梅','李晨','旁白'],48:['张伟','刘梅','张雨桐','张乐乐'],49:['张伟','刘梅','旁白','李晨'],50:['张伟','刘梅','张雨桐','张乐乐']})

ADVANCED6=[
('很多事情到了人生后半程，答案反而没有年轻时想得那么绝对。','Hěn duō shìqing dào le rénshēng hòubànchéng, dá’àn fǎn’ér méiyǒu niánqīng shí xiǎng de nàme juéduì.','Hayatın ikinci yarısına gelince birçok konuda cevaplar gençken düşündüğümüz kadar kesin olmuyor.'),
('一个选择真正的分量，往往要放到更长的时间里才能看清。','Yí ge xuǎnzé zhēnzhèng de fènliàng, wǎngwǎng yào fàng dào gèng cháng de shíjiān lǐ cái néng kàn qīng.','Bir seçimin gerçek ağırlığı çoğu zaman ancak daha uzun bir zaman diliminde anlaşılır.'),
('我们以为自己在告别过去，其实也在重新解释过去。','Wǒmen yǐwéi zìjǐ zài gàobié guòqù, qíshí yě zài chóngxīn jiěshì guòqù.','Geçmişe veda ettiğimizi sanırken aslında geçmişi yeniden yorumluyoruz.'),
('有些话不必说得太满，给彼此留一点余地反而更真诚。','Yǒuxiē huà bú bì shuō de tài mǎn, gěi bǐcǐ liú yìdiǎn yúdì fǎn’ér gèng zhēnchéng.','Bazı sözleri sonuna kadar keskin söylememek, karşılıklı biraz alan bırakmak bazen daha samimidir.'),
('真正的理解并不是完全同意，而是知道对方为什么这样想。','Zhēnzhèng de lǐjiě bìng bú shì wánquán tóngyì, ér shì zhīdào duìfāng wèishénme zhèyàng xiǎng.','Gerçek anlayış tamamen aynı fikirde olmak değil, karşı tarafın neden böyle düşündüğünü bilmektir.'),
('回忆会改变细节，却常常保留当时最重要的感受。','Huíyì huì gǎibiàn xìjié, què chángcháng bǎoliú dāngshí zuì zhòngyào de gǎnshòu.','Anılar ayrıntıları değiştirebilir ama çoğu zaman o zamanki en önemli duyguyu korur.'),
('所谓经验，不是知道所有答案，而是更清楚哪些问题值得先问。','Suǒwèi jīngyàn, bú shì zhīdào suǒyǒu dá’àn, ér shì gèng qīngchu nǎxiē wèntí zhíde xiān wèn.','Deneyim, bütün cevapları bilmek değil; hangi soruların önce sorulmaya değer olduğunu daha iyi bilmektir.'),
('如果一种传统失去了原来的生活背景，我们也可以重新理解它的意义。','Rúguǒ yì zhǒng chuántǒng shīqù le yuánlái de shēnghuó bèijǐng, wǒmen yě kěyǐ chóngxīn lǐjiě tā de yìyì.','Bir gelenek eski yaşam bağlamını kaybederse anlamını yeniden yorumlayabiliriz.'),
('改变并不一定否定过去，有时候恰恰是为了让重要的东西继续留下来。','Gǎibiàn bìng bù yídìng fǒudìng guòqù, yǒu shíhou qiàqià shì wèile ràng zhòngyào de dōngxi jìxù liú xiàlái.','Değişim geçmişi reddetmek değildir; bazen önemli olanın yaşamaya devam etmesi içindir.'),
('面对不确定性，最难的往往不是做决定，而是接受没有完美答案。','Miànduì bù quèdìngxìng, zuì nán de wǎngwǎng bú shì zuò juédìng, ér shì jiēshòu méiyǒu wánměi dá’àn.','Belirsizlik karşısında en zor şey çoğu zaman karar vermek değil, kusursuz cevabın olmadığını kabul etmektir.'),
('关系越亲近，越需要把理所当然的事情重新说清楚。','Guānxì yuè qīnjìn, yuè xūyào bǎ lǐsuǒdāngrán de shìqing chóngxīn shuō qīngchu.','İlişki ne kadar yakınsa, kendiliğinden anlaşılır sandığımız şeyleri o kadar yeniden açık etmek gerekir.'),
('我们能留下来的，未必只是东西，也可能是一种做事和待人的方式。','Wǒmen néng liú xiàlái de, wèibì zhǐshì dōngxi, yě kěnéng shì yì zhǒng zuòshì hé dàirén de fāngshì.','Arkamızda bıraktığımız yalnızca eşyalar olmayabilir; bir çalışma ve insanlara davranma biçimi de olabilir.'),
('一个地方之所以成为家，往往不是因为房子本身，而是因为在那里积累的关系。','Yí ge dìfang zhī suǒyǐ chéngwéi jiā, wǎngwǎng bú shì yīnwèi fángzi běnshēn, ér shì yīnwèi zài nàlǐ jīlěi de guānxì.','Bir yerin yuva olması çoğu zaman binanın kendisinden değil, orada biriken ilişkilerden kaynaklanır.'),
('有时候我们怀念的不是某个地点，而是那个地点里的自己。','Yǒu shíhou wǒmen huáiniàn de bú shì mǒu ge dìdiǎn, ér shì nàge dìdiǎn lǐ de zìjǐ.','Bazen özlediğimiz belirli bir yer değil, o yerdeki eski halimizdir.'),
('把复杂的问题说得简单是一种能力，但把它说得过分简单也会失真。','Bǎ fùzá de wèntí shuō de jiǎndān shì yì zhǒng nénglì, dàn bǎ tā shuō de guòfèn jiǎndān yě huì shīzhēn.','Karmaşık bir konuyu sade anlatmak beceridir; ama aşırı basitleştirmek gerçeği çarpıtabilir.'),
('真正成熟的决定，通常既看现实条件，也承认人的感情。','Zhēnzhèng chéngshú de juédìng, tōngcháng jì kàn xiànshí tiáojiàn, yě chéngrèn rén de gǎnqíng.','Olgun bir karar genellikle hem gerçek koşulları hem de insan duygularını hesaba katar.'),
('有些遗憾无法补回来，但可以影响我们以后怎样对待别人。','Yǒuxiē yíhàn wúfǎ bǔ huílái, dàn kěyǐ yǐngxiǎng wǒmen yǐhòu zěnyàng duìdài biérén.','Bazı pişmanlıklar telafi edilemez ama gelecekte başkalarına nasıl davranacağımızı etkileyebilir.'),
('危机过去以后，最值得做的不是庆祝结束，而是认真复盘哪里还能更好。','Wēijī guòqù yǐhòu, zuì zhíde zuò de bú shì qìngzhù jiéshù, ér shì rènzhēn fùpán nǎlǐ hái néng gèng hǎo.','Kriz geçtikten sonra yapılacak en değerli şey bitişi kutlamak değil, nerelerin iyileştirilebileceğini ciddi biçimde değerlendirmektir.'),
('一个社区的韧性，常常体现在普通人愿不愿意互相照顾。','Yí ge shèqū de rènxìng, chángcháng tǐxiàn zài pǔtōng rén yuàn bù yuànyì hùxiāng zhàogù.','Bir toplumun dayanıklılığı çoğu zaman sıradan insanların birbirine bakmaya istekli olup olmamasında görülür.'),
('退休以后失去的也许是职位，留下来的却是能力、关系和判断。','Tuìxiū yǐhòu shīqù de yěxǔ shì zhíwèi, liú xiàlái de què shì nénglì, guānxì hé pànduàn.','Emeklilikte kaybolan şey belki unvandır; kalan ise beceri, ilişkiler ve muhakemedir.'),
('年龄增长并不自动带来智慧，愿意反思经验才更重要。','Niánlíng zēngzhǎng bìng bù zìdòng dàilái zhìhuì, yuànyì fǎnsī jīngyàn cái gèng zhòngyào.','Yaş almak otomatik olarak bilgelik getirmez; deneyimi düşünmeye istekli olmak daha önemlidir.'),
('我们不能替下一代决定他们的人生，但可以把自己的经验诚实地交给他们。','Wǒmen bù néng tì xià yí dài juédìng tāmen de rénshēng, dàn kěyǐ bǎ zìjǐ de jīngyàn chéngshí de jiāo gěi tāmen.','Bir sonraki kuşağın hayatına onların yerine karar veremeyiz; ama deneyimimizi dürüstçe aktarabiliriz.')
]

OPENING=[
('这件事表面上看很简单，真正谈起来却牵涉到很多层面。','Zhè jiàn shì biǎomiàn shàng kàn hěn jiǎndān, zhēnzhèng tán qǐlái què qiānshè dào hěn duō céngmiàn.','Bu konu yüzeyde basit görünüyor ama gerçekten konuşunca birçok boyutu olduğu ortaya çıkıyor.'),
('我想先听听大家最真实的想法，不急着找一个统一答案。','Wǒ xiǎng xiān tīngting dàjiā zuì zhēnshí de xiǎngfǎ, bù jí zhe zhǎo yí ge tǒngyī dá’àn.','Önce herkesin en gerçek düşüncesini duymak istiyorum; hemen tek bir cevap bulmak zorunda değiliz.'),
('有些变化来得很快，可真正适应往往需要更长时间。','Yǒuxiē biànhuà lái de hěn kuài, kě zhēnzhèng shìyìng wǎngwǎng xūyào gèng cháng shíjiān.','Bazı değişiklikler çok hızlı gelir ama gerçekten uyum sağlamak daha uzun sürer.'),
('这一次我们不仅要看事情怎么做，也要想为什么这样做。','Zhè yí cì wǒmen bùjǐn yào kàn shìqing zěnme zuò, yě yào xiǎng wèishénme zhèyàng zuò.','Bu kez yalnızca ne yapılacağına değil, neden böyle yapılacağına da bakmalıyız.'),
('如果只从自己的位置出发，很容易忽略别人正在经历什么。','Rúguǒ zhǐ cóng zìjǐ de wèizhi chūfā, hěn róngyì hūlüè biérén zhèngzài jīnglì shénme.','Yalnızca kendi bulunduğumuz yerden bakarsak başkalarının ne yaşadığını gözden kaçırmak kolaydır.'),
('先把感受和事实都说出来，我们再慢慢梳理。','Xiān bǎ gǎnshòu hé shìshí dōu shuō chūlái, wǒmen zài mànmàn shūlǐ.','Önce duyguları ve olguları ortaya koyalım, sonra yavaşça düzenleyelim.')
]

CLOSING=[
('今天没有把所有问题都解决，但我们已经知道真正重要的是什么。','Jīntiān méiyǒu bǎ suǒyǒu wèntí dōu jiějué, dàn wǒmen yǐjīng zhīdào zhēnzhèng zhòngyào de shì shénme.','Bugün bütün sorunları çözmedik ama gerçekten neyin önemli olduğunu biliyoruz.'),
('有些答案需要时间验证，我们先把能做的事情做好。','Yǒuxiē dá’àn xūyào shíjiān yànzhèng, wǒmen xiān bǎ néng zuò de shìqing zuò hǎo.','Bazı cevapları zaman doğrulayacak; önce yapabildiğimiz şeyleri iyi yapalım.'),
('至少这次我们没有回避彼此真正关心的问题。','Zhìshǎo zhè cì wǒmen méiyǒu huíbì bǐcǐ zhēnzhèng guānxīn de wèntí.','En azından bu kez birbirimizin gerçekten önemsediği konulardan kaçmadık.'),
('以后再回头看今天，也许我们会有新的理解。','Yǐhòu zài huítóu kàn jīntiān, yěxǔ wǒmen huì yǒu xīn de lǐjiě.','İleride bugüne geri baktığımızda belki yeni bir anlayışımız olacak.'),
('不管接下来怎么变化，我们还是会继续把日子过下去。','Bùguǎn jiēxiàlái zěnme biànhuà, wǒmen háishi huì jìxù bǎ rìzi guò xiàqù.','Bundan sonra ne değişirse değişsin hayatımızı yaşamaya devam edeceğiz.'),
('好，今天先到这里，下一步我们一起面对。','Hǎo, jīntiān xiān dào zhèlǐ, xià yí bù wǒmen yìqǐ miànduì.','Tamam, bugünlük burada bitirelim; bir sonraki adımla birlikte yüzleşiriz.'),
('把今天说过的话记住，比急着证明谁对谁错更重要。','Bǎ jīntiān shuō guo de huà jìzhù, bǐ jí zhe zhèngmíng shéi duì shéi cuò gèng zhòngyào.','Bugün söylenenleri hatırlamak, kimin haklı olduğunu aceleyle kanıtlamaktan daha önemli.'),
('等我们走得再远一点，也许会更明白今天这个决定的意义。','Děng wǒmen zǒu de zài yuǎn yìdiǎn, yěxǔ huì gèng míngbai jīntiān zhège juédìng de yìyì.','Biraz daha yol aldıktan sonra belki bugünkü kararın anlamını daha iyi anlayacağız.')
]

def term_usage(term, variant=0):
    zh,py,tr=term
    forms=[
      (f'谈到{zh}，我更关心的是它背后的意义，而不只是表面的结果。',f'Tándào {py}, wǒ gèng guānxīn de shì tā bèihòu de yìyì, ér bù zhǐshì biǎomiàn de jiéguǒ.',f'{tr.capitalize()} konuşulurken benim daha çok önemsediğim, yüzeydeki sonuçtan çok arkasındaki anlam.'),
      (f'{zh}之所以重要，是因为它会影响我们接下来怎么理解这件事。',f'{py.capitalize()} zhī suǒyǐ zhòngyào, shì yīnwèi tā huì yǐngxiǎng wǒmen jiēxiàlái zěnme lǐjiě zhè jiàn shì.',f'{tr.capitalize()} önemli; çünkü bundan sonra bu meseleyi nasıl anlayacağımızı etkiliyor.'),
      (f'如果忽略{zh}，很多看似合理的判断其实会失去依据。',f'Rúguǒ hūlüè {py}, hěn duō kànshì hélǐ de pànduàn qíshí huì shīqù yījù.',f'{tr.capitalize()} göz ardı edilirse makul görünen birçok değerlendirme aslında dayanağını kaybedebilir.'),
      (f'我想把{zh}放回具体语境里看，这样更容易理解彼此的选择。',f'Wǒ xiǎng bǎ {py} fàng huí jùtǐ yǔjìng lǐ kàn, zhèyàng gèng róngyì lǐjiě bǐcǐ de xuǎnzé.',f'{tr.capitalize()} konusunu somut bağlamına yerleştirirsek birbirimizin seçimlerini anlamak daha kolay olur.')]
    return forms[variant%4]

def terms_for_scene(n):
    return T[n] + COMMON_TERMS

def make_dialogues(scene):
    n=scene['number']; roles=ROLES[n]; terms=terms_for_scene(n)
    lines=list(OPENING)
    for i,t in enumerate(terms):
        lines.append(term_usage(t,i)); lines.append(term_usage(t,i+1))
    lines.extend(h5.COMMON5)
    lines.extend(ADVANCED6)
    # 6 + 16 + 50 + 22 = 94; add the six reflective closing turns.
    lines.extend(CLOSING)
    assert len(lines)==100, len(lines)
    return [{'id':f'DLG_ZH_HSK6_SC{n:03d}_{i:03d}','speaker':roles[(i-1)%len(roles)],'zh':zh,'pinyin':py,'tr':tr} for i,(zh,py,tr) in enumerate(lines,1)]

def make_cards(scene):
    n=scene['number']; out=[]
    for i,t in enumerate(terms_for_scene(n),1):
        zh,py,tr=t; ezh,epy,etr=term_usage(t,i)
        out.append({'id':f'VOC_ZH_HSK6_SC{n:03d}_{i:03d}','zh':zh,'pinyin':py,'tr':tr,'exampleZh':ezh,'examplePinyin':epy,'exampleTr':etr,'kind':'active' if i<=6 else 'review'})
    return out

def grammar_items(scene):
    n=scene['number']; g=scene['learning'].get('grammarTheme','')
    templates={
      '多层复句与衔接':[
        {'type':'word_order','tokens':['即使','情况发生变化','只要','核心目标不变','我们就','可以继续调整'],'answerTokens':['即使','情况发生变化','只要','核心目标不变','我们就','可以继续调整']},
        {'type':'fill_blank','blankSentenceZh':'___我们尊重彼此的选择，分歧也不一定会破坏关系。','options':['只要','反而','至于'],'answer':'只要'},
        {'type':'sentence_repair','tokens':['我们','不仅要','看结果','还要','理解过程','为什么会这样'],'answerTokens':['我们','不仅要','看结果','还要','理解过程','为什么会这样']}],
      '委婉与言外之意':[
        {'type':'word_order','tokens':['我理解','你的意思','不过','也许','我们还可以','换个角度看'],'answerTokens':['我理解','你的意思','不过','也许','我们还可以','换个角度看']},
        {'type':'fill_blank','blankSentenceZh':'这件事恐怕没有表面上___简单。','options':['那么','既然','无论'],'answer':'那么'},
        {'type':'sentence_repair','tokens':['不一定','我不是说','这个方案不好','只是','最合适'],'answerTokens':['我不是说','这个方案不好','只是','不一定','最合适']}],
      '让步与反驳':[
        {'type':'word_order','tokens':['虽然','你的担心有道理','但是','我们也不能','忽略另一面的影响'],'answerTokens':['虽然','你的担心有道理','但是','我们也不能','忽略另一面的影响']},
        {'type':'fill_blank','blankSentenceZh':'___成本更高，这个方案在长期上可能更稳妥。','options':['尽管','因此','至于'],'answer':'尽管'},
        {'type':'sentence_repair','tokens':['未必','看起来方便','就','长期合适'],'answerTokens':['看起来方便','未必','就','长期合适']}],
      '抽象因果论证':[
        {'type':'word_order','tokens':['之所以','这个变化影响很大','是因为','它改变了','原来的关系结构'],'answerTokens':['之所以','这个变化影响很大','是因为','它改变了','原来的关系结构']},
        {'type':'fill_blank','blankSentenceZh':'真正的问题不在结果本身，___在我们如何理解它。','options':['而','只要','尽管'],'answer':'而'},
        {'type':'sentence_repair','tokens':['结果','表面原因','不能只归因于','还要考虑','长期背景'],'answerTokens':['结果','不能只归因于','表面原因','还要考虑','长期背景']}],
      '修辞与语用':[
        {'type':'word_order','tokens':['有时候','一句简单的话','比','很长的解释','更能表达','真正的感情'],'answerTokens':['有时候','一句简单的话','比','很长的解释','更能表达','真正的感情']},
        {'type':'fill_blank','blankSentenceZh':'他说“路还长”，这里的“路”更像是在___人生。','options':['比喻','计算','拒绝'],'answer':'比喻'},
        {'type':'sentence_repair','tokens':['这句话','字面意思以外','还有','更深的含义'],'answerTokens':['这句话','字面意思以外','还有','更深的含义']}],
      '正式/非正式语域转换':[
        {'type':'word_order','tokens':['正式场合','我们需要','表达得更明确','也更注意','措辞'],'answerTokens':['正式场合','我们需要','表达得更明确','也更注意','措辞']},
        {'type':'fill_blank','blankSentenceZh':'跟家人说话可以更自然，但正式通知需要更___。','options':['规范','随便','含糊'],'answer':'规范'},
        {'type':'sentence_repair','tokens':['同一个意思','不同场合','需要','不同的表达方式'],'answerTokens':['同一个意思','不同场合','需要','不同的表达方式']}]
    }
    base=templates.get(g,templates['多层复句与衔接']); prompt={'word_order':'Kelimeleri doğru sıraya koy.','fill_blank':'Boşluğu doğru kelimeyle doldur.','sentence_repair':'Yanlış sıradaki cümleyi düzelt.'}
    out=[]
    for i in range(9):
        item=dict(base[i%3]); item['id']=f'SENT_ZH_HSK6_SC{n:03d}_{i+1:03d}'; item['promptTr']=prompt[item['type']]; out.append(item)
    return out

def make_comprehension(scene):
    n=scene['number']; title=scene['titleTr']; goal=scene['learning']['communicationGoals'][0]
    return [
      {'id':f'COMP_ZH_HSK6_SC{n:03d}_001','questionTr':'Bu sahnenin ana olayı hangisidir?','optionsTr':[title,'Ailenin ilk taşınma günü','Basit sayı tekrarı'],'correctIndex':0},
      {'id':f'COMP_ZH_HSK6_SC{n:03d}_002','questionTr':'Sahnenin temel iletişim hedefi nedir?','optionsTr':[goal,'Yalnızca renk isimlerini saymak','Sadece selamlaşmak'],'correctIndex':0},
      {'id':f'COMP_ZH_HSK6_SC{n:03d}_003','questionTr':'HSK6 düzeyinde bu sahne yalnızca olayı mı, yoksa ima/bağlam/değerleri de mi ele alır?','optionsTr':['İma, bağlam ve değerleri de ele alır','Yalnızca nesne isimlerini öğretir','Hiç iletişim içermez'],'correctIndex':0},
      {'id':f'COMP_ZH_HSK6_SC{n:03d}_004','questionTr':'Karakterlerin farklı bakış açılarını gerekçelendirmesi bekleniyor mu?','optionsTr':['Evet','Hayır','Sahne sessizdir'],'correctIndex':0},
      {'id':f'COMP_ZH_HSK6_SC{n:03d}_005','questionTr':'Sahnenin sonucu sonraki yaşam olaylarıyla süreklilik kuruyor mu?','optionsTr':['Evet','Hayır','Her sahne tamamen bağımsızdır'],'correctIndex':0}]

def make_pron(scene,cards):
    n=scene['number']; return [{'id':f'PRON_ZH_HSK6_SC{n:03d}_{i:03d}','zh':c['exampleZh'],'pinyin':c['examplePinyin'],'tr':c['exampleTr'],'scoring':['pronunciation','toneAccuracy','fluency','timing','completeness','prosody']} for i,c in enumerate(cards[:5],1)]

def make_interactive(scene):
    n=scene['number']; term=terms_for_scene(n)[0]
    return [
      {'id':f'INT_ZH_HSK6_SC{n:03d}_001','promptZh':'如果对方的选择和你的价值观不同，你会怎么回应？','promptPinyin':'Rúguǒ duìfāng de xuǎnzé hé nǐ de jiàzhíguān bùtóng, nǐ huì zěnme huíyìng?','promptTr':'Karşı tarafın seçimi senin değerlerinle farklıysa nasıl cevap verirsin?','options':[{'zh':'我未必会做同样的选择，但我想先理解你的理由。','tr':'Ben aynı seçimi yapmayabilirim ama önce gerekçeni anlamak isterim.','correct':True},{'zh':'跟我不同就是错的。','tr':'Benden farklıysa yanlıştır.','correct':False},{'zh':'不用解释，我不想听。','tr':'Açıklamana gerek yok, dinlemek istemiyorum.','correct':False}]},
      {'id':f'INT_ZH_HSK6_SC{n:03d}_002','promptZh':f'谈到{term[0]}时，什么做法更符合高级沟通？','promptPinyin':f'Tándào {term[1]} shí, shénme zuòfǎ gèng fúhé gāojí gōutōng?','promptTr':f'{term[2].capitalize()} konuşulurken hangi yaklaşım ileri düzey iletişime daha uygundur?','options':[{'zh':'同时考虑语境、关系、事实和长期影响。','tr':'Bağlamı, ilişkiyi, olguları ve uzun vadeli etkiyi birlikte düşünmek.','correct':True},{'zh':'只挑最难的词来说。','tr':'Yalnızca en zor kelimeleri kullanmak.','correct':False},{'zh':'故意让对方听不懂。','tr':'Karşı tarafın anlamamasını bilerek sağlamak.','correct':False}]},
      {'id':f'INT_ZH_HSK6_SC{n:03d}_003','promptZh':'如果一句话可能让人误解，最合适的做法是什么？','promptPinyin':'Rúguǒ yí jù huà kěnéng ràng rén wùjiě, zuì héshì de zuòfǎ shì shénme?','promptTr':'Bir cümle yanlış anlaşılabilecekse en uygun yaklaşım nedir?','options':[{'zh':'根据关系和语境补充说明，必要时换一种表达。','tr':'İlişkiye ve bağlama göre açıklamak, gerekirse farklı ifade etmek.','correct':True},{'zh':'重复同一句话，声音更大。','tr':'Aynı cümleyi daha yüksek sesle tekrarlamak.','correct':False},{'zh':'马上结束所有交流。','tr':'İletişimi hemen bitirmek.','correct':False}]},
      {'id':f'INT_ZH_HSK6_SC{n:03d}_004','promptZh':'高级表达最重要的是什么？','promptPinyin':'Gāojí biǎodá zuì zhòngyào de shì shénme?','promptTr':'İleri düzey ifadede en önemli şey nedir?','options':[{'zh':'准确表达意思，同时照顾语气、关系和语境。','tr':'Anlamı doğru ifade ederken ton, ilişki ve bağlamı da gözetmek.','correct':True},{'zh':'每句话都必须很长。','tr':'Her cümlenin mutlaka çok uzun olması.','correct':False},{'zh':'尽量使用别人不知道的词。','tr':'Mümkün olduğunca başkalarının bilmediği kelimeleri kullanmak.','correct':False}]}
    ]

def make_production(scene):
    n=scene['number']
    return {'scenePurposeTr':scene.get('miniAdventureTr',''),'timeOfDay':'evening' if n in [1,2,3,5,8,9,21,23,24,25,29,39,40,46,47,48,49,50] else 'day','atmosphere':'HSK6 düzeyinde doğal, nüanslı, bağlam ve pragmatik anlamı güçlü; yaşamın ileri dönemleri, miras, kuşaklar, aidiyet ve soyut değerlendirme odaklı Mandarin','characters':ROLES[n],'locationId':scene.get('locationId',''),'visual':{'reuseLocation':True,'newVisualRequired':False,'style':'visual_novel_theatre'},'audio':{'voiceLanguage':'zh-CN','narratorProfile':'NARRATOR_ZH_001','defaultSpeechSpeed':1.0},'animation':{'level':'normal','mouthMode':'AUTO_SIMPLE','blink':True,'speakerFocus':True},'continuityNoteTr':f"{scene['titleTr']} olayı HSK6 yaşam çizgisinde sahne {n} olarak kaydedilir; evlilikler, torunlar, emeklilik, yaşlılık, toplumsal miras ve aile hafızasına ilişkin sonuçlar sonraki sahnelere aktarılır."}

def main():
    data=json.loads(PATH.read_text(encoding='utf-8')); assert len(data['scenes'])==50
    for scene in data['scenes']:
        n=scene['number']; cards=make_cards(scene); learning=dict(scene.get('learning') or {})
        learning.update({'vocabularyCards':cards,'sentenceExercises':grammar_items(scene),'comprehensionQuestions':make_comprehension(scene),'pronunciationItems':make_pron(scene,cards),'interactiveDialogue':make_interactive(scene),'examRules':{'vocabularyPassPercent':90,'sentencePassPercent':85,'lockNextSceneUntilPassed':True},'examStages':[{'stage':1,'type':'vocabulary','passPercent':90},{'stage':2,'type':'sentence','passPercent':85,'requiresStage':1}],'flashCardPolicy':{'allowPrevious':True,'allowNext':True,'allowFavorite':True,'favoritesStudyMode':True}})
        scene['learning']=learning; scene['dialogues']=make_dialogues(scene); scene['production']=make_production(scene)
        scene['complete']=True; scene['productionStatus']='complete'; scene['editorialStatus']='generated_full_v1_requires_native_review'; scene['dialogueCount']=len(scene['dialogues'])
    data['schemaVersion']=3; data['completeSceneCount']=50; data['editorialNoteTr']='HSK6 50 sahne veri olarak tamdır; ileri düzey doğal Mandarin, ima, retorik, kültürel/pragmatik nüans ve ticari yayın öncesi native editör kontrolü özellikle önerilir.'
    PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('HSK6 authoring completed:',len(data['scenes']),'scenes,',sum(len(s['dialogues']) for s in data['scenes']),'dialogues')

if __name__=='__main__': main()
