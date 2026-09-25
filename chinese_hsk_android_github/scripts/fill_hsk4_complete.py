#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the HSK4 production payload for all 50 scenes.

Deterministic/offline authoring generator. Technical completeness is kept separate from
native/editorial review. HSK4 emphasizes connected natural Mandarin, justification,
contrast, negotiation, tactful criticism, leadership, health and social/community topics.
"""
from __future__ import annotations
import importlib.util, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'authoring'/'hsk4_blueprints.json'

spec=importlib.util.spec_from_file_location('h3gen',ROOT/'scripts'/'fill_hsk3_complete.py')
h3=importlib.util.module_from_spec(spec); spec.loader.exec_module(h3)
W=dict(h3.W)

W.update({
'move_decision':('搬家决定','bānjiā juédìng','taşınma kararı'),
'reason':('理由','lǐyóu','gerekçe'), 'farm':('农场','nóngchǎng','çiftlik'),
'harvest':('收获','shōuhuò','hasat'), 'farewell':('告别','gàobié','veda etmek'),
'oldletter':('旧信','jiù xìn','eski mektup'), 'familyphoto':('家庭照片','jiātíng zhàopiàn','aile fotoğrafı'),
'memory2':('往事','wǎngshì','geçmiş anılar'), 'organize':('组织','zǔzhī','organize etmek'),
'dividework':('分工','fēngōng','iş bölümü'), 'independent':('独立','dúlì','bağımsız'),
'housing':('住房','zhùfáng','konut'), 'distance':('距离','jùlí','mesafe'),
'garden':('菜园','càiyuán','sebze bahçesi'), 'seed':('种子','zhǒngzi','tohum'),
'soil':('土壤','tǔrǎng','toprak'), 'resource':('资源','zīyuán','kaynak'),
'criticism':('批评','pīpíng','eleştiri'), 'suggestion':('建议','jiànyì','öneri'),
'kitchenlayout':('厨房布局','chúfáng bùjú','mutfak düzeni'), 'generation':('一代人','yí dài rén','bir kuşak'),
'habit':('习惯','xíguàn','alışkanlık'), 'compromise':('妥协','tuǒxié','uzlaşma'),
'exam_pressure':('考试压力','kǎoshì yālì','sınav baskısı'), 'strategy':('策略','cèlüè','strateji'),
'screentime':('手机使用时间','shǒujī shǐyòng shíjiān','telefon kullanım süresi'), 'rule2':('规则','guīzé','kural'),
'negotiate':('协商','xiéshāng','müzakere etmek'), 'recruit':('招聘','zhāopìn','işe alım'),
'newemployee':('新员工','xīn yuángōng','yeni çalışan'), 'training':('培训','péixùn','eğitim'),
'mistake':('错误','cuòwù','hata'), 'allergy':('过敏','guòmǐn','alerji'),
'ingredient':('食材','shícái','malzeme / gıda içeriği'), 'responsible':('负责','fùzé','sorumlu olmak'),
'online_review':('网上评价','wǎngshàng píngjià','internet yorumu'), 'reputation':('口碑','kǒubēi','itibar / ağızdan ağıza ün'),
'respond':('回应','huíyìng','yanıt vermek'), 'teamleader':('组长','zǔzhǎng','ekip lideri'),
'leadership':('领导能力','lǐngdǎo nénglì','liderlik becerisi'), 'conflict':('矛盾','máodùn','anlaşmazlık'),
'mediation':('协调','xiétiáo','uzlaştırmak / koordine etmek'), 'relationship':('恋爱关系','liàn’ài guānxì','romantik ilişki'),
'privacy':('隐私','yǐnsī','mahremiyet'), 'trust':('信任','xìnrèn','güven'),
'hearttalk':('谈心','tánxīn','içten konuşmak'), 'photography':('摄影','shèyǐng','fotoğrafçılık'),
'lens':('镜头','jìngtóu','objektif / kamera bakışı'), 'talent':('天赋','tiānfù','yetenek'),
'photo_competition':('摄影比赛','shèyǐng bǐsài','fotoğraf yarışması'), 'entry':('参赛作品','cānsài zuòpǐn','yarışma eseri'),
'produce_stall':('菜摊','cài tān','sebze tezgâhı'), 'produce':('农产品','nóngchǎnpǐn','tarım ürünü'),
'market':('市场','shìchǎng','pazar'),
'health':('健康','jiànkāng','sağlık'), 'doctor':('医生','yīshēng','doktor'), 'worry':('担心','dānxīn','endişe'),
'police':('警察','jǐngchá','polis'), 'tourist':('游客','yóukè','turist'), 'culture':('文化','wénhuà','kültür'),
'season':('季节','jìjié','mevsim'), 'emotion':('情绪','qíngxù','duygusal durum'), 'change2':('变化','biànhuà','değişim'),
'payment':('付款','fùkuǎn','ödeme'),

'local_supplier':('本地供应商','běndì gōngyìngshāng','yerel tedarikçi'), 'quality':('质量','zhìliàng','kalite'),
'wallet':('钱包','qiánbāo','cüzdan'), 'honesty':('诚信','chéngxìn','dürüstlük / güvenilirlik'),
'poweroutage':('停电','tíngdiàn','elektrik kesintisi'), 'emergency':('紧急情况','jǐnjí qíngkuàng','acil durum'),
'busyhour':('高峰时间','gāofēng shíjiān','yoğun saat'), 'burnout':('过度疲劳','guòdù píláo','aşırı yorgunluk'),
'balance':('平衡','pínghéng','denge'), 'vacation':('假期','jiàqī','tatil'),
'destination':('目的地','mùdìdì','varış yeri'), 'delay':('晚点','wǎndiǎn','gecikme'),
'platform2':('站台','zhàntái','peron'), 'noise':('噪音','zàoyīn','gürültü'),
'hotelcomplaint':('酒店投诉','jiǔdiàn tóusù','otel şikâyeti'), 'guide':('导游','dǎoyóu','rehber'),
'localhistory':('当地历史','dāngdì lìshǐ','yerel tarih'), 'lostphone':('手机丢失','shǒujī diūshī','telefon kaybı'),
'security':('安全','ānquán','güvenlik'), 'travelmemory':('旅行回忆','lǚxíng huíyì','seyahat anısı'),
'examresult':('考试成绩','kǎoshì chéngjì','sınav sonucu'), 'expectation':('期望','qīwàng','beklenti'),
'university':('大学','dàxué','üniversite'), 'admission':('录取','lùqǔ','kabul / yerleştirme'),
'campus':('校园','xiàoyuán','kampüs'), 'dorm':('宿舍','sùshè','yurt'),
'branch':('分店','fēndiàn','şube'), 'expansion':('扩张','kuòzhāng','büyüme / genişleme'),
'disagreement':('分歧','fēnqí','görüş ayrılığı'), 'evidence':('依据','yījù','dayanak / kanıt'),
'revenue':('营业额','yíngyè’é','ciro'), 'improve':('改进','gǎijìn','iyileştirmek'),
'hospital':('医院','yīyuàn','hastane'), 'checkup':('检查','jiǎnchá','muayene / kontrol'),
'lifestyle':('生活方式','shēnghuó fāngshì','yaşam tarzı'), 'rest':('休息','xiūxi','dinlenmek'),
'stubborn':('固执','gùzhí','inatçı'), 'charity_kitchen':('爱心厨房','àixīn chúfáng','sosyal yardım mutfağı'),
'volunteer2':('志愿者','zhìyuànzhě','gönüllü'), 'coordination':('统筹','tǒngchóu','genel koordinasyon'),
'award':('获奖','huòjiǎng','ödül kazanmak'), 'localnews':('地方新闻','dìfāng xīnwén','yerel haber'),
'acceptance_letter':('录取通知书','lùqǔ tōngzhīshū','üniversite kabul mektubu'), 'packing':('收拾行李','shōushi xíngli','eşya/bagaj toplamak'),
'orientation':('新生报到','xīnshēng bàodào','üniversite kayıt/oryantasyonu'), 'retirementplan':('退休计划','tuìxiū jìhuà','emeklilik planı'),
'savings':('储蓄','chǔxù','tasarruf'), 'media_interview':('媒体采访','méitǐ cǎifǎng','medya röportajı'),
'communityrole':('社区角色','shèqū juésè','toplumdaki rol'), 'threegenerations':('三代人','sān dài rén','üç kuşak'),
'familyportrait':('全家福','quánjiāfú','aile fotoğrafı'), 'independence2':('独立生活','dúlì shēnghuó','bağımsız yaşam'),
'nextstage':('人生新阶段','rénshēng xīn jiēduàn','hayatın yeni aşaması'),
'priority':('优先考虑','yōuxiān kǎolǜ','öncelik vermek'), 'impact':('影响','yǐngxiǎng','etki'),
'option':('选择方案','xuǎnzé fāng’àn','seçenek'), 'responsibility2':('责任感','zérèngǎn','sorumluluk duygusu'),
'communicate':('沟通','gōutōng','iletişim kurmak'), 'respect':('尊重','zūnzhòng','saygı'),
'persuade':('说服','shuōfú','ikna etmek'), 'adjust':('调整','tiáozhěng','ayarlamak / düzenlemek')
})

V={
1:['move_decision','reason','farm','independent','distance','family','option','futureplan'],
2:['harvest','farm','farewell','produce','memory2','tradition','family','season'],
3:['oldletter','familyphoto','memory2','tradition','family','past','remember','emotion'],
4:['organize','dividework','moving','schedule','responsibility2','family','confirm','adjust'],
5:['housing','independent','distance','compare2','option','location','rent','decide2'],
6:['garden','seed','soil','resource','planword','farm','need','responsibility2'],
7:['criticism','suggestion','kitchenlayout','improve','respect','communicate','quality','cafeidea'],
8:['generation','habit','compromise','respect','communicate','family','rule2','balance'],
9:['exam_pressure','strategy','studyplan','expectation','rest','schedule','study','family'],
10:['screentime','rule2','negotiate','compromise','responsibility2','habit','family','adjust'],
11:['recruit','newemployee','busyhour','service','workhours','responsibility','customer','training'],
12:['newemployee','training','mistake','responsible','service','communicate','adjust','experience'],
13:['allergy','ingredient','responsible','customer','service','check','safety','confirm'],
14:['online_review','reputation','respond','customer','criticism','improve','service','respect'],
15:['teamleader','leadership','responsibility2','project_team','meeting','communicate','decision','work'],
16:['conflict','mediation','communicate','respect','colleague','compromise','leadership','solution'],
17:['relationship','privacy','trust','communicate','family','respect','emotion','choice'],
18:['hearttalk','advice','relationship','trust','generation','respect','family','emotion'],
19:['photography','lens','talent','interest','park','practice','choice','futureplan'],
20:['photo_competition','entry','photography','lens','quality','prepare','deadline','talent'],
21:['produce_stall','produce','market','price','customer','farm','quality','trust'],
22:['local_supplier','ingredient','quality','supplier','cost','cafeidea','produce','business'],
23:['wallet','trust','honesty','customer','payment','responsible','solution','service'],
24:['poweroutage','emergency','busyhour','customer','service','repair','safety','solution'],
25:['burnout','balance','rest','work','family','lifestyle','schedule','health'],
26:['vacation','destination','compare2','family','budget','planword','choice','compromise'],
27:['delay','platform2','ticket','schedule','travel','announce','wait','adjust'],
28:['noise','hotelcomplaint','hotel','roomtype','communicate','respect','solution','rest'],
29:['guide','localhistory','tourist','travel','culture','choice','planword','experience'],
30:['lostphone','security','tourist','call','police','solution','check','travel'],
31:['travelmemory','family','experience','photo','story','emotion','remember','compare2'],
32:['examresult','expectation','disappointed','study','futureplan','family','choice','progress'],
33:['university','admission','compare2','major','cost','distance','futureplan','choice'],
34:['branch','expansion','risk','benefit','cost','business','customer','futureplan'],
35:['disagreement','expansion','risk','balance','family','business','persuade','priority'],
36:['evidence','revenue','cost','budget','business','compare2','decision','risk'],
37:['improve','quality','cafeidea','customer','service','business','priority','decision'],
38:['hospital','checkup','health','family','worry','doctor','rest','support'],
39:['lifestyle','checkup','doctor','health','advice','exercise','rest','change2'],
40:['stubborn','rest','health','persuade','family','lifestyle','respect','compromise'],
41:['charity_kitchen','volunteer2','community','help','organize','food','responsibility2','together'],
42:['coordination','volunteer2','organize','dividework','schedule','responsibility2','community','leadership'],
43:['award','photo_competition','photography','localnews','talent','family','happy','futureplan'],
44:['acceptance_letter','admission','university','family','futureplan','happy','study','choice'],
45:['packing','dorm','university','independence2','family','prepare','emotion','futureplan'],
46:['orientation','campus','university','independence2','friend','schedule','study','nextstage'],
47:['retirementplan','savings','budget','earlyretire','cafeidea','futureplan','balance','family'],
48:['media_interview','communityrole','cafeidea','localnews','service','community','memory','customer'],
49:['threegenerations','familyportrait','generation','memory2','family','photo','change2','emotion'],
50:['independence2','nextstage','family','futureplan','university','career','emotion','change2']
}

# If a key above comes from earlier levels and is missing, use a safe equivalent.
FALLBACKS={
'moving':'move_decision','season':'season','emotion':'emotion','decision':'decide2','safety':'security',
'payment':'payment','health':'health','announce':'confirm','wait':'schedule','tourist':'tourist','culture':'culture',
'police':'police','photo':'familyphoto','story':'memory2','worry':'worry','doctor':'doctor','support':'help',
'exercise':'fitness','change':'adjust','together':'community','deadline':'schedule','practice':'study','interest':'choice'
}
for n,keys in V.items():
    V[n]=[k if k in W else FALLBACKS.get(k,k) for k in keys]
    missing=[k for k in V[n] if k not in W]
    if missing: raise KeyError((n,missing))

ROLES={n:['张伟','刘梅','张雨桐','张乐乐'] for n in range(1,51)}
for n in [1,2,3,4,5,6]: ROLES[n]=['张伟','刘梅','爷爷','奶奶']
ROLES[7]=['奶奶','刘梅','张伟','员工']
ROLES[8]=['张伟','刘梅','爷爷','奶奶']
ROLES[9]=['张雨桐','刘梅','张伟','老师']
ROLES[10]=['张乐乐','刘梅','张伟','张雨桐']
ROLES[11]=['刘梅','张伟','员工','顾客']
ROLES[12]=['刘梅','新员工','员工','张伟']
ROLES[13]=['顾客','刘梅','员工','张伟']
ROLES[14]=['刘梅','张伟','员工','顾客']
ROLES[15]=['张伟','经理','同事','刘梅']
ROLES[16]=['张伟','同事甲','同事乙','刘梅']
ROLES[17]=['张雨桐','刘梅','张伟','朋友']
ROLES[18]=['奶奶','张雨桐','刘梅','张伟']
ROLES[19]=['张乐乐','朋友','张伟','刘梅']
ROLES[20]=['张乐乐','工作人员','张伟','刘梅']
ROLES[21]=['爷爷','顾客','刘梅','张伟']
ROLES[22]=['刘梅','供应商','张伟','员工']
ROLES[23]=['顾客','刘梅','员工','张伟']
ROLES[24]=['刘梅','员工','顾客','张伟']
ROLES[25]=['张伟','刘梅','李晨','张雨桐']
ROLES[26]=['张伟','刘梅','张雨桐','张乐乐']
ROLES[27]=['张伟','刘梅','工作人员','张乐乐']
ROLES[28]=['张伟','刘梅','酒店工作人员','张乐乐']
ROLES[29]=['导游','张伟','刘梅','张乐乐']
ROLES[30]=['张乐乐','张伟','刘梅','工作人员']
ROLES[31]=['张伟','刘梅','张雨桐','张乐乐']
ROLES[32]=['张雨桐','刘梅','张伟','老师']
ROLES[33]=['张雨桐','刘梅','张伟','老师']
ROLES[34]=['刘梅','张伟','李晨','员工']
ROLES[35]=['张伟','刘梅','李晨','张雨桐']
ROLES[36]=['张伟','刘梅','李晨','张雨桐']
ROLES[37]=['刘梅','张伟','员工','顾客']
ROLES[38]=['爷爷','奶奶','张伟','医生']
ROLES[39]=['医生','爷爷','张伟','刘梅']
ROLES[40]=['爷爷','奶奶','张伟','刘梅']
ROLES[41]=['刘梅','志愿者','奶奶','张伟']
ROLES[42]=['奶奶','志愿者','刘梅','工作人员']
ROLES[43]=['张乐乐','记者','张伟','刘梅']
ROLES[44]=['张雨桐','刘梅','张伟','老师']
ROLES[45]=['张雨桐','刘梅','张伟','张乐乐']
ROLES[46]=['张雨桐','新同学','老师','刘梅']
ROLES[47]=['张伟','刘梅','李晨','张雨桐']
ROLES[48]=['刘梅','记者','张伟','顾客']
ROLES[49]=['张伟','刘梅','爷爷','奶奶']
ROLES[50]=['张伟','刘梅','张雨桐','张乐乐']

COMMON4=[
('这件事不能只看眼前，我们还得考虑以后。','Zhè jiàn shì bù néng zhǐ kàn yǎnqián, wǒmen hái děi kǎolǜ yǐhòu.','Bu konuya yalnızca bugünü düşünerek bakamayız; sonrasını da değerlendirmeliyiz.'),
('我理解你的担心，不过情况并没有那么糟。','Wǒ lǐjiě nǐ de dānxīn, búguò qíngkuàng bìng méiyǒu nàme zāo.','Endişeni anlıyorum ama durum o kadar kötü değil.'),
('从实际情况来看，这个办法更合适。','Cóng shíjì qíngkuàng lái kàn, zhège bànfǎ gèng héshì.','Gerçek duruma bakınca bu yöntem daha uygun.'),
('我们先把各自的想法说出来，再做决定。','Wǒmen xiān bǎ gèzì de xiǎngfa shuō chūlái, zài zuò juédìng.','Önce herkes kendi düşüncesini söylesin, sonra karar verelim.'),
('你说得有道理，但我还有一点不同意见。','Nǐ shuō de yǒu dàolǐ, dàn wǒ hái yǒu yìdiǎn bùtóng yìjiàn.','Söylediğin mantıklı ama benim biraz farklı bir görüşüm var.'),
('如果只追求速度，可能会忽略质量。','Rúguǒ zhǐ zhuīqiú sùdù, kěnéng huì hūlüè zhìliàng.','Sadece hıza odaklanırsak kaliteyi gözden kaçırabiliriz.'),
('这也是我最担心的一点。','Zhè yě shì wǒ zuì dānxīn de yìdiǎn.','Benim en çok endişelendiğim nokta da bu.'),
('我们可以换个角度想一想。','Wǒmen kěyǐ huàn ge jiǎodù xiǎng yì xiǎng.','Başka bir açıdan düşünebiliriz.'),
('与其马上下结论，不如先把信息弄清楚。','Yǔqí mǎshàng xià jiélùn, bùrú xiān bǎ xìnxī nòng qīngchu.','Hemen sonuca varmaktansa önce bilgileri netleştirelim.'),
('我赞成先试一段时间，再看效果。','Wǒ zànchéng xiān shì yí duàn shíjiān, zài kàn xiàoguǒ.','Önce bir süre deneyip sonucu görmeyi destekliyorum.'),
('既然大家都同意，我们就按这个方向继续。','Jìrán dàjiā dōu tóngyì, wǒmen jiù àn zhège fāngxiàng jìxù.','Herkes kabul ettiğine göre bu yönde ilerleyelim.'),
('即使遇到困难，也不能把计划全都放弃。','Jíshǐ yùdào kùnnan, yě bù néng bǎ jìhuà quándōu fàngqì.','Zorlukla karşılaşsak bile planın tamamından vazgeçmemeliyiz.'),
('一方面要考虑成本，另一方面也要考虑体验。','Yì fāngmiàn yào kǎolǜ chéngběn, lìng yì fāngmiàn yě yào kǎolǜ tǐyàn.','Bir yandan maliyeti, diğer yandan deneyimi düşünmeliyiz.'),
('这个问题被我们想得太复杂了。','Zhège wèntí bèi wǒmen xiǎng de tài fùzá le.','Bu sorunu zihnimizde gereğinden fazla karmaşıklaştırmışız.'),
('先把最重要的部分处理好，其他的可以慢慢调整。','Xiān bǎ zuì zhòngyào de bùfen chǔlǐ hǎo, qítā de kěyǐ mànmàn tiáozhěng.','Önce en önemli kısmı halledelim, diğerlerini zamanla ayarlarız.'),
('你的建议很具体，我觉得值得试。','Nǐ de jiànyì hěn jùtǐ, wǒ juéde zhíde shì.','Önerin oldukça somut; bence denenmeye değer.'),
('有不同意见很正常，关键是把话说清楚。','Yǒu bùtóng yìjiàn hěn zhèngcháng, guānjiàn shì bǎ huà shuō qīngchu.','Farklı görüşlerin olması normal; önemli olan açık konuşmak.'),
('我们都希望结果好，只是考虑的角度不一样。','Wǒmen dōu xīwàng jiéguǒ hǎo, zhǐshì kǎolǜ de jiǎodù bù yíyàng.','Hepimiz sonucun iyi olmasını istiyoruz; sadece farklı açılardan düşünüyoruz.'),
('先听完对方的话，再表达自己的意见。','Xiān tīng wán duìfāng de huà, zài biǎodá zìjǐ de yìjiàn.','Önce karşı tarafı sonuna kadar dinleyip sonra fikrimizi söyleyelim.'),
('这样处理既比较公平，也比较容易让大家接受。','Zhèyàng chǔlǐ jì bǐjiào gōngpíng, yě bǐjiào róngyì ràng dàjiā jiēshòu.','Böyle çözmek hem daha adil hem de herkesin kabul etmesi daha kolay.'),
('我会把今天讨论的重点整理下来。','Wǒ huì bǎ jīntiān tǎolùn de zhòngdiǎn zhěnglǐ xiàlái.','Bugün konuştuğumuz önemli noktaları düzenleyip not edeceğim.'),
('有些事情现在决定还太早。','Yǒuxiē shìqing xiànzài juédìng hái tài zǎo.','Bazı konularda şimdi karar vermek için henüz erken.'),
('不管最后选哪一个，我们都要承担结果。','Bùguǎn zuìhòu xuǎn nǎ yí ge, wǒmen dōu yào chéngdān jiéguǒ.','Sonunda hangisini seçersek seçelim sonucunun sorumluluğunu almalıyız.'),
('这不是谁对谁错的问题，而是怎么做更合适。','Zhè bú shì shéi duì shéi cuò de wèntí, ér shì zěnme zuò gèng héshì.','Bu kimin haklı olduğu meselesi değil; neyin daha uygun olduğu meselesi.'),
('我们可以先定一个底线。','Wǒmen kěyǐ xiān dìng yí ge dǐxiàn.','Önce bir alt sınır/kırmızı çizgi belirleyebiliriz.'),
('只要不影响最重要的目标，细节可以商量。','Zhǐyào bù yǐngxiǎng zuì zhòngyào de mùbiāo, xìjié kěyǐ shāngliang.','En önemli hedef etkilenmediği sürece ayrıntılar konuşulabilir.'),
('我希望这个决定不是一时冲动。','Wǒ xīwàng zhège juédìng bú shì yìshí chōngdòng.','Bu kararın anlık bir dürtüyle verilmemesini umuyorum.'),
('所以我们才需要多看几个选择。','Suǒyǐ wǒmen cái xūyào duō kàn jǐ ge xuǎnzé.','Bu yüzden birkaç seçeneğe daha bakmamız gerekiyor.'),
('现在的信息已经比刚才完整多了。','Xiànzài de xìnxī yǐjīng bǐ gāngcái wánzhěng duō le.','Şimdiki bilgiler az öncekinden çok daha eksiksiz.'),
('这样一来，我们判断起来就容易多了。','Zhèyàng yì lái, wǒmen pànduàn qǐlái jiù róngyì duō le.','Böylece değerlendirme yapmak çok daha kolay oldu.'),
('还有谁想补充吗？','Hái yǒu shéi xiǎng bǔchōng ma?','Eklemek isteyen başka biri var mı?'),
('我想补充一个实际问题。','Wǒ xiǎng bǔchōng yí ge shíjì wèntí.','Pratik bir konuyu eklemek istiyorum.'),
('这个问题确实不能忽略。','Zhège wèntí quèshí bù néng hūlüè.','Bu konu gerçekten göz ardı edilemez.'),
('那我们把它也加到计划里。','Nà wǒmen bǎ tā yě jiā dào jìhuà lǐ.','O zaman bunu da plana ekleyelim.'),
('现在的方案已经比较完整了。','Xiànzài de fāng’àn yǐjīng bǐjiào wánzhěng le.','Mevcut plan artık oldukça tamamlandı.'),
('我建议最后再检查一次风险。','Wǒ jiànyì zuìhòu zài jiǎnchá yí cì fēngxiǎn.','Son olarak riskleri bir kez daha kontrol etmeyi öneriyorum.'),
('好，先看最可能发生的情况。','Hǎo, xiān kàn zuì kěnéng fāshēng de qíngkuàng.','Tamam, önce gerçekleşmesi en olası duruma bakalım.'),
('如果真的发生，我们也有第二个办法。','Rúguǒ zhēn de fāshēng, wǒmen yě yǒu dì èr ge bànfǎ.','Gerçekleşirse ikinci bir çözümümüz de var.'),
('有备用方案，我就放心多了。','Yǒu bèiyòng fāng’àn, wǒ jiù fàngxīn duō le.','Yedek planımız olması beni çok rahatlattı.'),
('事情终于开始往好的方向发展。','Shìqing zhōngyú kāishǐ wǎng hǎo de fāngxiàng fāzhǎn.','İşler sonunda iyi yönde ilerlemeye başladı.'),
('不过还不到完全放松的时候。','Búguò hái bú dào wánquán fàngsōng de shíhou.','Ama tamamen rahatlamak için henüz erken.'),
('对，我们把最后几个步骤做完。','Duì, wǒmen bǎ zuìhòu jǐ ge bùzhòu zuò wán.','Evet, son birkaç adımı tamamlayalım.'),
('这次大家配合得很好。','Zhè cì dàjiā pèihé de hěn hǎo.','Bu kez herkes çok iyi işbirliği yaptı.'),
('尤其是出现问题以后，大家都很冷静。','Yóuqí shì chūxiàn wèntí yǐhòu, dàjiā dōu hěn lěngjìng.','Özellikle sorun çıktıktan sonra herkes çok sakindi.'),
('我觉得这比结果本身还重要。','Wǒ juéde zhè bǐ jiéguǒ běnshēn hái zhòngyào.','Bence bu, sonucun kendisinden bile daha önemli.'),
('下次遇到类似情况，我们会更有经验。','Xià cì yùdào lèisì qíngkuàng, wǒmen huì gèng yǒu jīngyàn.','Bir dahaki benzer durumda daha deneyimli olacağız.'),
('今天的决定先这样执行。','Jīntiān de juédìng xiān zhèyàng zhíxíng.','Bugünkü kararı şimdilik bu şekilde uygulayalım.'),
('过一段时间以后再看看有没有需要调整的地方。','Guò yí duàn shíjiān yǐhòu zài kànkan yǒu méiyǒu xūyào tiáozhěng de dìfang.','Bir süre sonra yeniden bakıp ayarlanması gereken bir şey var mı görelim.'),
('我同意，这样比较稳妥。','Wǒ tóngyì, zhèyàng bǐjiào wěntuǒ.','Katılıyorum, böyle daha temkinli.'),
('那今天就先到这里。','Nà jīntiān jiù xiān dào zhèlǐ.','O zaman bugünlük burada bitirelim.'),
('辛苦大家了。','Xīnkǔ dàjiā le.','Herkesin emeğine sağlık.'),
('没事，事情解决了就好。','Méi shì, shìqing jiějué le jiù hǎo.','Sorun değil, iş çözülmüş olsun yeter.'),
('回去以后我再把细节确认一遍。','Huíqu yǐhòu wǒ zài bǎ xìjié quèrèn yí biàn.','Dönünce ayrıntıları bir kez daha kontrol edeceğim.'),
('有变化就及时告诉大家。','Yǒu biànhuà jiù jíshí gàosu dàjiā.','Bir değişiklik olursa herkese zamanında haber ver.'),
('好，我们保持联系。','Hǎo, wǒmen bǎochí liánxì.','Tamam, iletişimde kalalım.')
]

ACTION={'organize','dividework','negotiate','recruit','training','respond','mediation','communicate','persuade','adjust','improve','packing'}
PERSON={'newemployee','volunteer2','guide','teamleader'}
STATE={'independent','burnout','stubborn','security','balance'}
PLACE={'farm','housing','garden','hospital','university','campus','dorm','branch'}

def intro(key):
    zh,py,tr=W[key]
    if key in ACTION: return (f'今天我们得认真谈谈怎么{zh}。',f'Jīntiān wǒmen děi rènzhēn tántan zěnme {py}.',f'Bugün {tr} konusunu ciddi biçimde konuşmamız gerekiyor.')
    if key in PERSON: return (f'今天的重点跟{zh}有关。',f'Jīntiān de zhòngdiǎn gēn {py} yǒuguān.',f'Bugünün ana konusu {tr} ile ilgili.')
    if key in PLACE: return (f'关于{zh}，大家有几个不同的想法。',f'Guānyú {py}, dàjiā yǒu jǐ ge bùtóng de xiǎngfa.',f'{tr.capitalize()} konusunda herkesin birkaç farklı fikri var.')
    if key in STATE: return (f'最近大家越来越重视{zh}这个问题。',f'Zuìjìn dàjiā yuèláiyuè zhòngshì {py} zhège wèntí.',f'Son zamanlarda herkes {tr} konusuna giderek daha fazla önem veriyor.')
    return (f'今天我们先谈谈{zh}。',f'Jīntiān wǒmen xiān tántan {py}.',f'Bugün önce {tr} hakkında konuşalım.')

def usage(key,v=0):
    zh,py,tr=W[key]
    if key in ACTION:
        pats=[
          (f'这件事需要大家一起{zh}。',f'Zhè jiàn shì xūyào dàjiā yìqǐ {py}.',f'Bu konuda herkesin birlikte {tr} gerekiyor.'),
          (f'在决定以前，我们最好先{zh}。',f'Zài juédìng yǐqián, wǒmen zuìhǎo xiān {py}.',f'Karar vermeden önce {tr} daha iyi olur.'),
          (f'如果能提前{zh}，后面会顺利很多。',f'Rúguǒ néng tíqián {py}, hòumiàn huì shùnlì hěn duō.',f'Önceden {tr} mümkün olursa sonrası çok daha rahat ilerler.'),
          (f'我来负责{zh}这一部分。',f'Wǒ lái fùzé {py} zhè yí bùfen.',f'{tr.capitalize()} kısmını ben üstleneyim.')]
    elif key in PERSON:
        pats=[
          (f'我们也应该听听{zh}的意见。',f'Wǒmen yě yīnggāi tīngting {py} de yìjiàn.',f'{tr.capitalize()} görüşünü de dinlemeliyiz.'),
          (f'{zh}在这件事里很重要。',f'{py.capitalize()} zài zhè jiàn shì lǐ hěn zhòngyào.',f'{tr.capitalize()} bu konuda önemli.'),
          (f'我会跟{zh}再确认一次。',f'Wǒ huì gēn {py} zài quèrèn yí cì.',f'{tr.capitalize()} ile bir kez daha teyit edeceğim.')]
    elif key in PLACE:
        pats=[
          (f'这个{zh}有优点，也有需要考虑的地方。',f'Zhège {py} yǒu yōudiǎn, yě yǒu xūyào kǎolǜ de dìfang.',f'Bu {tr} avantajlara sahip ama düşünülmesi gereken yönleri de var.'),
          (f'我们得先看看{zh}是否真的合适。',f'Wǒmen děi xiān kànkan {py} shìfǒu zhēn de héshì.',f'Önce {tr} gerçekten uygun mu bakmalıyız.'),
          (f'如果选{zh}，以后会有什么影响？',f'Rúguǒ xuǎn {py}, yǐhòu huì yǒu shénme yǐngxiǎng?',f'{tr.capitalize()} seçersek ileride ne etkisi olur?')]
    else:
        pats=[
          (f'关于{zh}，我想再听听大家的看法。',f'Guānyú {py}, wǒ xiǎng zài tīngting dàjiā de kànfa.',f'{tr.capitalize()} konusunda herkesin fikrini bir kez daha duymak istiyorum.'),
          (f'{zh}是我们不能忽略的一点。',f'{py.capitalize()} shì wǒmen bù néng hūlüè de yìdiǎn.',f'{tr.capitalize()} göz ardı edemeyeceğimiz bir nokta.'),
          (f'我们把{zh}也列进考虑范围吧。',f'Wǒmen bǎ {py} yě liè jìn kǎolǜ fànwéi ba.',f'{tr.capitalize()} konusunu da değerlendirme kapsamına alalım.'),
          (f'如果{zh}发生变化，计划也得调整。',f'Rúguǒ {py} fāshēng biànhuà, jìhuà yě děi tiáozhěng.',f'{tr.capitalize()} değişirse planı da ayarlamak gerekir.')]
    return pats[v%len(pats)]

def make_dialogues(scene):
    n=scene['number']; keys=V[n]; roles=ROLES[n]
    lines=[intro(keys[0]),intro(keys[1]),
      ('这次的情况比以前更复杂，所以我们得多考虑几步。','Zhè cì de qíngkuàng bǐ yǐqián gèng fùzá, suǒyǐ wǒmen děi duō kǎolǜ jǐ bù.','Bu kez durum eskisine göre daha karmaşık; bu yüzden birkaç adım sonrasını düşünmeliyiz.'),
      ('我同意，先别急着做最后决定。','Wǒ tóngyì, xiān bié jízhe zuò zuìhòu juédìng.','Katılıyorum, son kararı vermek için acele etmeyelim.'),
      ('那我们先把最重要的条件列出来。','Nà wǒmen xiān bǎ zuì zhòngyào de tiáojiàn liè chūlái.','O zaman önce en önemli koşulları sıralayalım.'),
      ('好，这样比较容易比较。','Hǎo, zhèyàng bǐjiào róngyì bǐjiào.','Tamam, böyle karşılaştırmak daha kolay olur.')]
    reactions=[
      ('这一点我同意。','Zhè yìdiǎn wǒ tóngyì.','Bu noktaya katılıyorum.'),
      ('这个角度我刚才没有想到。','Zhège jiǎodù wǒ gāngcái méiyǒu xiǎngdào.','Bu açı daha önce aklıma gelmemişti.'),
      ('那确实需要重新考虑。','Nà quèshí xūyào chóngxīn kǎolǜ.','O zaman gerçekten yeniden düşünmek gerekiyor.'),
      ('听起来比较合理。','Tīng qǐlái bǐjiào hélǐ.','Kulağa oldukça mantıklı geliyor.'),
      ('我先把这一点记下来。','Wǒ xiān bǎ zhè yìdiǎn jì xiàlái.','Bu noktayı not edeyim.'),
      ('我们再看看还有没有别的影响。','Wǒmen zài kànkan hái yǒu méiyǒu bié de yǐngxiǎng.','Başka etkileri var mı bir de ona bakalım.')]
    for i,k in enumerate(keys[:8]):
        lines.append(usage(k,i)); lines.append(reactions[i%len(reactions)])
    lines.extend(COMMON4)
    idx=0
    while len(lines)<94:
        k=keys[idx%len(keys)]
        lines.append(usage(k,idx+2)); lines.append(reactions[(idx+2)%len(reactions)]); idx+=1
    lines=lines[:94]
    lines += [
      ('现在主要问题已经有了比较清楚的处理办法。','Xiànzài zhǔyào wèntí yǐjīng yǒu le bǐjiào qīngchu de chǔlǐ bànfǎ.','Ana sorun için artık oldukça net bir çözümümüz var.'),
      ('我们先按这个方案执行。','Wǒmen xiān àn zhège fāng’àn zhíxíng.','Şimdilik bu plana göre uygulayalım.'),
      ('如果实际情况有变化，再及时调整。','Rúguǒ shíjì qíngkuàng yǒu biànhuà, zài jíshí tiáozhěng.','Gerçek koşullar değişirse zamanında ayarlarız.'),
      ('这次大家都把自己的意见说清楚了。','Zhè cì dàjiā dōu bǎ zìjǐ de yìjiàn shuō qīngchu le.','Bu kez herkes görüşünü net biçimde ifade etti.'),
      ('这样做决定，我觉得更放心。','Zhèyàng zuò juédìng, wǒ juéde gèng fàngxīn.','Bu şekilde karar vermek bana daha güven veriyor.'),
      ('好，那我们进入下一步吧。','Hǎo, nà wǒmen jìnrù xià yí bù ba.','Tamam, o zaman bir sonraki adıma geçelim.')]
    return [{'id':f'DLG_ZH_HSK4_SC{n:03d}_{i:03d}','speaker':roles[(i-1)%len(roles)],'zh':zh,'pinyin':py,'tr':tr} for i,(zh,py,tr) in enumerate(lines[:100],1)]

def make_cards(scene):
    n=scene['number']; out=[]
    for i,k in enumerate(V[n],1):
        zh,py,tr=W[k]; ezh,epy,etr=usage(k,i)
        out.append({'id':f'VOC_ZH_HSK4_SC{n:03d}_{i:03d}','zh':zh,'pinyin':py,'tr':tr,'exampleZh':ezh,'examplePinyin':epy,'exampleTr':etr,'kind':'active' if i<=6 else 'review'})
    return out

def grammar_items(scene):
    n=scene['number']; g=scene['learning'].get('grammarTheme',''); k0=V[n][0]; zh0=W[k0][0]
    templates={
      '既然…就…':[
       {'type':'word_order','tokens':['既然','已经决定了','就','认真准备'],'answerTokens':['既然','已经决定了','就','认真准备']},
       {'type':'fill_blank','blankSentenceZh':'既然大家都同意，___按这个办法做吧。','options':['就','而且','即使'],'answer':'就'},
       {'type':'sentence_repair','tokens':['就','既然','有时间','再确认一次'],'answerTokens':['既然','有时间','就','再确认一次']}],
      '不但…而且…':[
       {'type':'word_order','tokens':['不但',zh0,'重要','而且','影响很大'],'answerTokens':['不但',zh0,'重要','而且','影响很大']},
       {'type':'fill_blank','blankSentenceZh':'这个办法不但省时间，___更安全。','options':['而且','就','即使'],'answer':'而且'},
       {'type':'sentence_repair','tokens':['而且','方便','不但','便宜'],'answerTokens':['不但','便宜','而且','方便']}],
      '即使…也…':[
       {'type':'word_order','tokens':['即使','有困难','也','要继续'],'answerTokens':['即使','有困难','也','要继续']},
       {'type':'fill_blank','blankSentenceZh':'即使今天很忙，___要把重要的事做完。','options':['也','就','而且'],'answer':'也'},
       {'type':'sentence_repair','tokens':['也','即使','下雨','会去'],'answerTokens':['即使','下雨','也','会去']}],
      '一方面…另一方面…':[
       {'type':'word_order','tokens':['一方面','要考虑时间','另一方面','要考虑费用'],'answerTokens':['一方面','要考虑时间','另一方面','要考虑费用']},
       {'type':'fill_blank','blankSentenceZh':'一方面要照顾家人，___也要安排工作。','options':['另一方面','就','即使'],'answer':'另一方面'},
       {'type':'sentence_repair','tokens':['另一方面','要看质量','一方面','要看价格'],'answerTokens':['一方面','要看价格','另一方面','要看质量']}],
      '与其…不如…':[
       {'type':'word_order','tokens':['与其','一直担心','不如','先试试看'],'answerTokens':['与其','一直担心','不如','先试试看']},
       {'type':'fill_blank','blankSentenceZh':'与其马上决定，___再比较一下。','options':['不如','而且','也'],'answer':'不如'},
       {'type':'sentence_repair','tokens':['不如','与其','争论','找办法'],'answerTokens':['与其','争论','不如','找办法']}],
      '把/被字句综合':[
       {'type':'word_order','tokens':['我们','把','问题','说清楚'],'answerTokens':['我们','把','问题','说清楚']},
       {'type':'fill_blank','blankSentenceZh':'重要文件___他放在桌上了。','options':['被','把','就'],'answer':'被'},
       {'type':'sentence_repair','tokens':['被','这个问题','大家','解决了'],'answerTokens':['这个问题','被','大家','解决了']}]
    }
    base=templates.get(g,templates['既然…就…']); prompt={'word_order':'Kelimeleri doğru sıraya koy.','fill_blank':'Boşluğu doğru kelimeyle doldur.','sentence_repair':'Yanlış sıradaki cümleyi düzelt.'}
    out=[]
    for i in range(9):
        item=dict(base[i%3]); item['id']=f'SENT_ZH_HSK4_SC{n:03d}_{i+1:03d}'; item['promptTr']=prompt[item['type']]; out.append(item)
    return out

def make_comprehension(scene):
    n=scene['number']; title=scene['titleTr']
    return [
      {'id':f'COMP_ZH_HSK4_SC{n:03d}_001','questionTr':'Bu sahnenin ana konusu hangisidir?','optionsTr':[title,'Uzay araştırması','Bir matematik yarışması'],'correctIndex':0},
      {'id':f'COMP_ZH_HSK4_SC{n:03d}_002','questionTr':'Karakterler olayın farklı yönlerini karşılaştırıyor mu?','optionsTr':['Evet','Hayır','Sadece kelime sayıyorlar'],'correctIndex':0},
      {'id':f'COMP_ZH_HSK4_SC{n:03d}_003','questionTr':'Sahnede görüş belirtme ve gerekçelendirme var mı?','optionsTr':['Evet','Hayır','Yalnızca selamlaşma var'],'correctIndex':0},
      {'id':f'COMP_ZH_HSK4_SC{n:03d}_004','questionTr':'Bu sahne hangi yaşam dönemine aittir?','optionsTr':['Ailenin köklerinin derinleştiği, çocukların büyüdüğü ve büyüklerin kasabaya geldiği dönem','İlk taşınma günü','Torunlarla yaşlılık dönemi'],'correctIndex':0},
      {'id':f'COMP_ZH_HSK4_SC{n:03d}_005','questionTr':'Sahnenin sonunda bir karar, çözüm veya sonraki adım belirleniyor mu?','optionsTr':['Evet','Hayır','Kimse konuşmuyor'],'correctIndex':0}]

def make_pron(scene,cards):
    n=scene['number']; return [{'id':f'PRON_ZH_HSK4_SC{n:03d}_{i:03d}','zh':c['exampleZh'],'pinyin':c['examplePinyin'],'tr':c['exampleTr'],'scoring':['pronunciation','toneAccuracy','fluency','timing','completeness']} for i,c in enumerate(cards[:5],1)]

def make_interactive(scene):
    n=scene['number']; topic=W[V[n][0]]
    return [
      {'id':f'INT_ZH_HSK4_SC{n:03d}_001','promptZh':'你怎么看这件事？','promptPinyin':'Nǐ zěnme kàn zhè jiàn shì?','promptTr':'Bu konu hakkında ne düşünüyorsun?','options':[{'zh':'我觉得应该先把情况了解清楚，再做决定。','tr':'Bence önce durumu iyice anlayıp sonra karar vermeliyiz.','correct':True},{'zh':'我今天穿的是蓝色衣服。','tr':'Bugün mavi kıyafet giyiyorum.','correct':False},{'zh':'桌子下面有一本书。','tr':'Masanın altında bir kitap var.','correct':False}]},
      {'id':f'INT_ZH_HSK4_SC{n:03d}_002','promptZh':f'关于{topic[0]}，最重要的是什么？','promptPinyin':f'Guānyú {topic[1]}, zuì zhòngyào de shì shénme?','promptTr':f'{topic[2].capitalize()} konusunda en önemli şey nedir?','options':[{'zh':'要考虑实际情况，也要考虑以后。','tr':'Hem gerçek durumu hem de sonrasını düşünmeliyiz.','correct':True},{'zh':'我喜欢喝热水。','tr':'Sıcak su içmeyi severim.','correct':False},{'zh':'现在是星期三。','tr':'Bugün çarşamba.','correct':False}]},
      {'id':f'INT_ZH_HSK4_SC{n:03d}_003','promptZh':'如果大家意见不一样呢？','promptPinyin':'Rúguǒ dàjiā yìjiàn bù yíyàng ne?','promptTr':'Herkesin görüşü farklıysa ne yapmalı?','options':[{'zh':'先听完每个人的理由，再找能接受的办法。','tr':'Önce herkesin gerekçesini dinleyip sonra kabul edilebilir bir çözüm bulmalıyız.','correct':True},{'zh':'马上结束谈话。','tr':'Konuşmayı hemen bitirmeliyiz.','correct':False},{'zh':'谁声音大就听谁的。','tr':'Sesi daha yüksek çıkan kimi ise onu dinlemeliyiz.','correct':False}]},
      {'id':f'INT_ZH_HSK4_SC{n:03d}_004','promptZh':'决定以后还需要做什么？','promptPinyin':'Juédìng yǐhòu hái xūyào zuò shénme?','promptTr':'Karardan sonra ne yapmak gerekir?','options':[{'zh':'执行一段时间，再根据结果调整。','tr':'Bir süre uygulayıp sonuca göre ayarlamak gerekir.','correct':True},{'zh':'什么都不用管。','tr':'Hiçbir şeye bakmaya gerek yok.','correct':False},{'zh':'把以前的计划全部忘掉。','tr':'Önceki planların hepsini unutmak gerekir.','correct':False}]}
    ]

def make_production(scene):
    n=scene['number']; return {'scenePurposeTr':scene.get('miniAdventureTr',''),'timeOfDay':'evening' if n in [8,17,18,25,26,31,35,36,47,50] else 'day','atmosphere':'doğal, sıcak ve HSK4 düzeyinde görüş, gerekçe, karşılaştırma ve uzlaşma odaklı Mandarin','characters':ROLES[n],'locationId':scene.get('locationId',''),'visual':{'reuseLocation':True,'newVisualRequired':False,'style':'visual_novel_theatre'},'audio':{'voiceLanguage':'zh-CN','narratorProfile':'NARRATOR_ZH_001','defaultSpeechSpeed':0.95},'animation':{'level':'normal','mouthMode':'AUTO_SIMPLE','blink':True,'speakerFocus':True},'continuityNoteTr':f"{scene['titleTr']} olayı HSK4 yaşam çizgisinde sahne {n} olarak kaydedilir; üç kuşak, kafe, okul ve kariyer sürekliliği sonraki sahnelere aktarılır."}

def main():
    data=json.loads(PATH.read_text(encoding='utf-8')); assert len(data['scenes'])==50
    for scene in data['scenes']:
        n=scene['number']; cards=make_cards(scene); learning=dict(scene.get('learning') or {})
        learning.update({'vocabularyCards':cards,'sentenceExercises':grammar_items(scene),'comprehensionQuestions':make_comprehension(scene),'pronunciationItems':make_pron(scene,cards),'interactiveDialogue':make_interactive(scene),'examRules':{'vocabularyPassPercent':90,'sentencePassPercent':85,'lockNextSceneUntilPassed':True},'examStages':[{'stage':1,'type':'vocabulary','passPercent':90},{'stage':2,'type':'sentence','passPercent':85,'requiresStage':1}],'flashCardPolicy':{'allowPrevious':True,'allowNext':True,'allowFavorite':True,'favoritesStudyMode':True}})
        scene['learning']=learning; scene['dialogues']=make_dialogues(scene); scene['production']=make_production(scene)
        scene['complete']=True; scene['productionStatus']='complete'; scene['editorialStatus']='generated_full_v1_requires_native_review'; scene['dialogueCount']=len(scene['dialogues'])
    data['schemaVersion']=3; data['completeSceneCount']=50; data['editorialNoteTr']='HSK4 50 sahne veri olarak tamdır; doğal Mandarin, kültürel/pragmatik kullanım ve ticari yayın öncesi native editör kontrolü önerilir.'
    PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('HSK4 authoring completed:',len(data['scenes']),'scenes,',sum(len(s['dialogues']) for s in data['scenes']),'dialogues')
if __name__=='__main__': main()
