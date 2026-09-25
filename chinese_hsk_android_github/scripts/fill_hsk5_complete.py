#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate HSK5 full production payload for all 50 scenes.

Deterministic/offline generator. HSK5 adds evidence-based reasoning, professional and civic
communication, abstract values, health/care, career and inter-generational negotiation.
Generated content remains explicitly flagged for native/editorial review before commercial use.
"""
from __future__ import annotations
import importlib.util, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'authoring'/'hsk5_blueprints.json'
spec=importlib.util.spec_from_file_location('h4gen',ROOT/'scripts'/'fill_hsk4_complete.py')
h4=importlib.util.module_from_spec(spec); spec.loader.exec_module(h4)
W=h4.W

W.update({
'selfeval':('自我评价','zìwǒ píngjià','öz değerlendirme'),
'failcourse':('挂科','guàkē','dersten kalmak'),
'setback':('挫折','cuòzhé','aksilik / başarısızlık'),
'recovery':('调整状态','tiáozhěng zhuàngtài','kendini toparlamak'),
'boundary':('边界','biānjiè','sınır'),
'support2':('支持','zhīchí','desteklemek'),
'intervene':('干预','gānyù','müdahale etmek'),
'autonomy':('自主','zìzhǔ','özerklik / kendi kararını verme'),
'educationpath':('学业方向','xuéyè fāngxiàng','eğitim yönü'),
'strength2':('优势','yōushì','güçlü yön / avantaj'),
'fit':('匹配','pǐpèi','uyum / eşleşme'),
'delegate':('授权','shòuquán','yetki devretmek'),
'expectation2':('工作期待','gōngzuò qīdài','iş beklentisi'),
'management':('管理','guǎnlǐ','yönetim'),
'fairness':('公平','gōngpíng','adalet / hakkaniyet'),
'shift':('排班','páibān','vardiya planı'),
'policy':('制度','zhìdù','kural / sistem / politika'),
'appeal':('申诉','shēnsù','itiraz / başvuru'),
'investigate':('调查','diàochá','araştırmak / incelemek'),
'proof':('证据','zhèngjù','kanıt'),
'objective':('客观','kèguān','objektif'),
'corporategoal':('项目目标','xiàngmù mùbiāo','proje hedefi'),
'milestone':('里程碑','lǐchéngbēi','kilometre taşı'),
'deadline2':('截止日期','jiézhǐ rìqī','son tarih'),
'projectdelay':('项目延期','xiàngmù yánqī','proje gecikmesi'),
'contingency':('应对方案','yìngduì fāng’àn','önlem / alternatif plan'),
'accountability':('担当','dāndāng','sorumluluk üstlenme'),
'clientexpectation':('客户期待','kèhù qīdài','müşteri beklentisi'),
'commitment':('承诺','chéngnuò','taahhüt / söz'),
'internship':('实习','shíxí','staj'),
'cv':('简历','jiǎnlì','özgeçmiş'),
'application2':('申请','shēnqǐng','başvuru'),
'rejection':('拒绝','jùjué','reddetmek / ret'),
'feedback2':('反馈','fǎnkuì','geri bildirim'),
'selfpresent':('自我展示','zìwǒ zhǎnshì','kendini sunma'),
'digitalmedia':('数字媒体','shùzì méitǐ','dijital medya'),
'audience':('受众','shòuzhòng','hedef kitle'),
'source':('信息来源','xìnxī láiyuán','bilgi kaynağı'),
'verify':('核实','héshí','doğrulamak'),
'misinformation':('假消息','jiǎ xiāoxi','yanlış haber / yanlış bilgi'),
'credibility':('可信度','kěxìndù','güvenilirlik'),
'traditionalmethod':('传统方法','chuántǒng fāngfǎ','geleneksel yöntem'),
'moderntech':('现代技术','xiàndài jìshù','modern teknoloji'),
'sustainability':('可持续发展','kě chíxù fāzhǎn','sürdürülebilirlik'),
'environmentgroup':('环保小组','huánbǎo xiǎozǔ','çevre grubu'),
'plastic':('塑料用品','sùliào yòngpǐn','plastik ürünler'),
'disposable':('一次性用品','yícìxìng yòngpǐn','tek kullanımlık ürünler'),
'operatingcost':('经营成本','jīngyíng chéngběn','işletme maliyeti'),
'rawmaterial':('原材料','yuáncáiliào','ham madde'),
'raiseprice':('涨价','zhǎngjià','fiyat artırmak'),
'customerexpect':('顾客期待','gùkè qīdài','müşteri beklentisi'),
'partner2':('伴侣','bànlǚ','partner / eş adayı'),
'awkward':('尴尬','gāngà','mahcup / gergin'),
'courtesy':('分寸','fēncùn','ölçülülük / sosyal incelik'),
'rescuesituation':('解围','jiěwéi','zor durumu yumuşatmak'),
'humor':('幽默','yōumò','mizah'),
'prevention':('预防保健','yùfáng bǎojiàn','koruyucu sağlık'),
'symptom':('症状','zhèngzhuàng','belirti'),
'bloodpressure':('血压','xuèyā','tansiyon'),
'fitnessgoal':('运动目标','yùndòng mùbiāo','egzersiz hedefi'),
'cultureevent':('文化活动','wénhuà huódòng','kültür etkinliği'),
'performer':('表演者','biǎoyǎnzhě','sanatçı / performansçı'),
'publicservice':('公共服务','gōnggòng fúwù','kamusal hizmet'),
'urbanplan':('城市规划','chéngshì guīhuà','kent planlaması'),
'roadwork':('道路施工','dàolù shīgōng','yol çalışması'),
'merchant':('商户','shānghù','esnaf / işletme'),
'cooperate':('合作','hézuò','işbirliği yapmak'),
'joboffer':('工作邀请','gōngzuò yāoqǐng','iş teklifi'),
'compensation':('薪酬','xīnchóu','ücret / maaş paketi'),
'values':('价值观','jiàzhíguān','değerler'),
'lifequality':('生活质量','shēnghuó zhìliàng','yaşam kalitesi'),
'retiredate':('退休日期','tuìxiū rìqī','emeklilik tarihi'),
'financialplan':('财务规划','cáiwù guīhuà','finansal planlama'),
'creativefield':('创意专业','chuàngyì zhuānyè','yaratıcı alan / bölüm'),
'portfolio':('作品集','zuòpǐn jí','portfolyo'),
'gradproject':('毕业项目','bìyè xiàngmù','mezuniyet projesi'),
'academicargument':('学术论证','xuéshù lùnzhèng','akademik argümantasyon'),
'graduation':('毕业','bìyè','mezuniyet'),
'fulltimejob':('正式工作','zhèngshì gōngzuò','tam zamanlı iş'),
'onboarding':('入职','rùzhí','işe başlama / onboarding'),
'relocate':('搬迁','bānqiān','taşınmak / yer değiştirmek'),
'belonging':('归属感','guīshǔgǎn','aidiyet duygusu'),
'eldercare':('老人照护','lǎorén zhàohù','yaşlı bakımı'),
'careplan':('照护计划','zhàohù jìhuà','bakım planı'),
'dignity':('尊严','zūnyán','onur / saygınlık'),
'accepthelp':('接受帮助','jiēshòu bāngzhù','yardım kabul etmek'),
'youthvolunteer':('青年志愿者','qīngnián zhìyuànzhě','genç gönüllü'),
'fundraising':('募捐','mùjuān','bağış toplama'),
'publicappeal':('公益倡议','gōngyì chàngyì','toplumsal yardım çağrısı'),
'careerachievement':('职业成就','zhíyè chéngjiù','kariyer başarısı'),
'recognition':('肯定','kěndìng','takdir / onay'),
'identity':('身份认同','shēnfèn rèntóng','kimlik algısı'),
'lifepurpose':('人生目标','rénshēng mùbiāo','yaşam amacı'),
'marriage':('结婚','jiéhūn','evlilik'),
'marriageexpect':('婚姻期待','hūnyīn qīdài','evlilik beklentisi'),
'life_review':('人生回顾','rénshēng huígù','hayat muhasebesi'),
'companionship':('陪伴','péibàn','eşlik / hayat arkadaşlığı'),
'generationhandover':('代际交接','dàijì jiāojiē','kuşak devri'),
'confidence2':('自信','zìxìn','özgüven'),
'message2':('传播内容','chuánbō nèiróng','iletişim içeriği'),
'sharedinterest':('共同利益','gòngtóng lìyì','ortak çıkar'),
'research2':('研究','yánjiū','araştırma'),
'donation2':('捐款','juānkuǎn','bağış')
})
# Let imported semantic usage helper treat these naturally.
h4.ACTION.update({'support2','intervene','delegate','investigate','verify','cooperate','relocate','accepthelp','fundraising'})
h4.PERSON.update({'audience','performer','merchant','partner2','youthvolunteer'})
h4.STATE.update({'objective','awkward','fairness','belonging','dignity'})

V={
1:['selfeval','failcourse','setback','recovery','study','feedback2','futureplan','strength2'],
2:['boundary','support2','intervene','autonomy','family','respect','communicate','choice'],
3:['educationpath','strength2','fit','interest','futureplan','choice','career','family'],
4:['delegate','expectation2','management','responsibility2','training','service','team','communicate'],
5:['fairness','shift','policy','appeal','management','responsibility2','communicate','evidence'],
6:['investigate','proof','objective','decision','fairness','feedback2','communicate','responsibility'],
7:['corporategoal','milestone','deadline2','project','leadership','responsibility2','team','risk'],
8:['projectdelay','deadline2','contingency','risk','project','schedule','team','solution'],
9:['clientexpectation','commitment','projectdelay','communicate','persuade','deadline2','solution','risk'],
10:['accountability','leadership','responsibility2','mistake','team','clientexpectation','communicate','trust'],
11:['internship','cv','application2','career','strength2','experience','interview','futureplan'],
12:['rejection','feedback2','interview','selfeval','setback','recovery','experience','strategy'],
13:['selfpresent','interview','strength2','experience','internship','confidence2','communicate','career'],
14:['digitalmedia','audience','source','communication','project','technology','message2','impact'],
15:['misinformation','source','verify','credibility','evidence','online_review','communicate','responsibility2'],
16:['traditionalmethod','moderntech','farm','experience','compare2','sustainability','evidence','respect'],
17:['environmentgroup','sustainability','experience','publicappeal','community','communicate','farm','responsibility2'],
18:['plastic','disposable','sustainability','cost','customerexpect','policy','business','impact'],
19:['operatingcost','rawmaterial','cost','revenue','business','risk','price','budget'],
20:['raiseprice','customerexpect','operatingcost','price','fairness','business','communicate','trust'],
21:['partner2','relationship','privacy','trust','family','respect','communicate','courtesy'],
22:['awkward','courtesy','relationship','family','privacy','respect','communicate','emotion'],
23:['rescuesituation','humor','courtesy','respect','generation','communicate','family','emotion'],
24:['prevention','symptom','bloodpressure','checkup','health','doctor','lifestyle','risk'],
25:['lifestyle','prevention','health','doctor','habit','balance','rest','advice'],
26:['fitnessgoal','exercise','progress','habit','health','motivation','family','balance'],
27:['cultureevent','performer','audience','community','culture','cafeidea','organize','publicappeal'],
28:['publicservice','urbanplan','community','evidence','opinion','impact','communicate','priority'],
29:['roadwork','urbanplan','impact','business','customer','merchant','risk','solution'],
30:['merchant','cooperate','community','business','solution','publicservice','communicate','sharedinterest'],
31:['joboffer','compensation','career','condition','benefit','risk','lifequality','choice'],
32:['values','lifequality','compensation','family','career','balance','priority','lifepurpose'],
33:['joboffer','values','priority','career','decision','communicate','respect','commitment'],
34:['retiredate','financialplan','savings','budget','earlyretire','longterm','family','risk'],
35:['creativefield','portfolio','career','interest','strength2','futureplan','choice','family'],
36:['gradproject','academicargument','presentation','evidence','research2','university','deadline2','feedback2'],
37:['graduation','university','thanks','career','futureplan','family','achievement','memory'],
38:['fulltimejob','onboarding','expectation2','work','colleague','responsibility2','adapt','career'],
39:['relocate','belonging','career','family','choice','lifequality','futureplan','distance'],
40:['belonging','priority','career','family','decision','community','lifequality','futureplan'],
41:['eldercare','hospital','health','doctor','careplan','family','worry','responsibility2'],
42:['careplan','dividework','eldercare','responsibility2','family','schedule','communicate','balance'],
43:['dignity','accepthelp','independent','eldercare','respect','family','persuade','privacy'],
44:['youthvolunteer','generation','community','culture','communicate','respect','cafeidea','experience'],
45:['fundraising','publicappeal','community','organize','donation2','volunteer2','responsibility2','impact'],
46:['careerachievement','recognition','team','leadership','project','thanks','career','memory'],
47:['identity','lifepurpose','retirementplan','earlyretire','friend','values','time','career'],
48:['marriage','marriageexpect','family','relationship','futureplan','respect','communicate','choice'],
49:['life_review','companionship','memory2','values','family','regret','thanks','lifepurpose'],
50:['generationhandover','nextstage','family','career','futureplan','responsibility2','change2','hope']
}
# Existing dictionary aliases/fallbacks.
ALIASES={'confidence':'strength2','communication':'communicate','technology':'moderntech','message':'source','motivation':'cheer','commoninterest':'community','condition':'option','longterm':'retirementplan','research':'evidence','achievement':'award','adapt':'adjust','time':'schedule','information':'source','decision':'decide2'}
for n,keys in list(V.items()):
    fixed=[]
    for k in keys:
        if k not in W: k=ALIASES.get(k,k)
        if k not in W: raise KeyError((n,k))
        fixed.append(k)
    if len(set(fixed))<6: raise ValueError(f'Scene {n} has insufficient vocabulary diversity: {fixed}')
    V[n]=fixed

ROLES={n:['张伟','刘梅','张雨桐','张乐乐'] for n in range(1,51)}
ROLES.update({
1:['张雨桐','同学','老师','刘梅'],2:['张伟','张雨桐','刘梅','张乐乐'],3:['张乐乐','张伟','刘梅','老师'],
4:['刘梅','经理','员工','张伟'],5:['员工','刘梅','经理','张伟'],6:['刘梅','经理','员工','张伟'],
7:['张伟','经理','同事','客户'],8:['张伟','同事','经理','项目成员'],9:['张伟','客户','经理','同事'],10:['张伟','经理','同事','刘梅'],
11:['张雨桐','老师','同学','刘梅'],12:['张雨桐','面试官','刘梅','朋友'],13:['张雨桐','面试官','同事','刘梅'],
14:['张乐乐','同学','老师','张伟'],15:['张乐乐','张伟','刘梅','老师'],16:['爷爷','张伟','张乐乐','刘梅'],17:['爷爷','环保小组成员','张乐乐','刘梅'],18:['刘梅','经理','顾客','员工'],19:['刘梅','张伟','经理','供应商'],20:['刘梅','张伟','顾客','经理'],
21:['张雨桐','伴侣','刘梅','张伟'],22:['张雨桐','伴侣','张伟','奶奶'],23:['奶奶','张雨桐','伴侣','刘梅'],
24:['张伟','医生','刘梅','护士'],25:['医生','张伟','刘梅','护士'],26:['张伟','刘梅','张雨桐','张乐乐'],
27:['刘梅','表演者','顾客','张伟'],28:['张伟','社区代表','商户','居民'],29:['刘梅','商户','张伟','顾客'],30:['商户','刘梅','张伟','社区代表'],
31:['张伟','经理','招聘者','刘梅'],32:['张伟','刘梅','李晨','张雨桐'],33:['张伟','经理','刘梅','李晨'],34:['张伟','刘梅','理财顾问','李晨'],
35:['张乐乐','老师','张伟','刘梅'],36:['张雨桐','导师','同学','刘梅'],37:['张雨桐','张伟','刘梅','同学'],38:['张雨桐','经理','同事','刘梅'],39:['张雨桐','张伟','刘梅','伴侣'],40:['张雨桐','张伟','刘梅','伴侣'],
41:['爷爷','医生','张伟','奶奶'],42:['张伟','刘梅','奶奶','张雨桐'],43:['奶奶','张伟','刘梅','爷爷'],44:['青年志愿者','刘梅','奶奶','张乐乐'],45:['刘梅','志愿者','张伟','社区代表'],46:['张伟','经理','同事','刘梅'],47:['张伟','李晨','刘梅','朋友'],48:['张雨桐','刘梅','张伟','伴侣'],49:['张伟','刘梅','李晨','旁白'],50:['张伟','刘梅','张雨桐','张乐乐']})

COMMON5=[
('我觉得现在最重要的不是马上下结论，而是先把事实和判断分开。','Wǒ juéde xiànzài zuì zhòngyào de bú shì mǎshàng xià jiélùn, ér shì xiān bǎ shìshí hé pànduàn fēnkāi.','Bence şu anda en önemli şey hemen sonuca varmak değil, önce olgularla yorumları ayırmak.'),
('从现有的信息来看，我们还需要补充几个关键细节。','Cóng xiànyǒu de xìnxī lái kàn, wǒmen hái xūyào bǔchōng jǐ ge guānjiàn xìjié.','Mevcut bilgilere bakılırsa birkaç kritik ayrıntıyı daha tamamlamamız gerekiyor.'),
('尽管结果不理想，我们仍然可以从中找到下一步的方向。','Jǐnguǎn jiéguǒ bù lǐxiǎng, wǒmen réngrán kěyǐ cóng zhōng zhǎodào xià yí bù de fāngxiàng.','Sonuç ideal olmasa da buradan sonraki adımın yönünü çıkarabiliriz.'),
('之所以会出现这个问题，是因为我们之前低估了它的影响。','Zhī suǒyǐ huì chūxiàn zhège wèntí, shì yīnwèi wǒmen zhīqián dīgū le tā de yǐngxiǎng.','Bu sorunun ortaya çıkmasının nedeni etkisini daha önce küçümsememizdi.'),
('无论最后怎么选择，我们都应该把理由说清楚。','Wúlùn zuìhòu zěnme xuǎnzé, wǒmen dōu yīnggāi bǎ lǐyóu shuō qīngchu.','Sonunda hangi seçimi yaparsak yapalım gerekçesini açıkça söylemeliyiz.'),
('这个方案不仅要解决眼前的问题，还要考虑长期影响。','Zhège fāng’àn bùjǐn yào jiějué yǎnqián de wèntí, hái yào kǎolǜ chángqī yǐngxiǎng.','Bu plan yalnızca mevcut sorunu çözmemeli, uzun vadeli etkisini de düşünmeli.'),
('与以前的做法相比，现在这个方案更重视风险控制。','Yǔ yǐqián de zuòfǎ xiāngbǐ, xiànzài zhège fāng’àn gèng zhòngshì fēngxiǎn kòngzhì.','Önceki yönteme kıyasla bu plan risk kontrolüne daha çok önem veriyor.'),
('如果只看一个数字，很容易忽略背后的原因。','Rúguǒ zhǐ kàn yí ge shùzì, hěn róngyì hūlüè bèihòu de yuányīn.','Sadece tek bir sayıya bakarsak arkasındaki nedeni gözden kaçırmak kolaydır.'),
('我想先确认一下，这个结论有没有可靠的依据。','Wǒ xiǎng xiān quèrèn yíxià, zhège jiélùn yǒu méiyǒu kěkào de yījù.','Önce bu sonucun güvenilir bir dayanağı var mı teyit etmek istiyorum.'),
('有不同意见并不代表合作失败，关键是能不能把分歧说清楚。','Yǒu bùtóng yìjiàn bìng bù dàibiǎo hézuò shībài, guānjiàn shì néng bù néng bǎ fēnqí shuō qīngchu.','Farklı görüşlerin olması işbirliğinin başarısız olduğu anlamına gelmez; önemli olan ayrılığı açıkça ifade edebilmek.'),
('我们最好把短期收益和长期代价放在一起比较。','Wǒmen zuìhǎo bǎ duǎnqī shōuyì hé chángqī dàijià fàng zài yìqǐ bǐjiào.','Kısa vadeli getiriyi ve uzun vadeli bedeli birlikte karşılaştırmamız daha iyi olur.'),
('这件事涉及的不只是效率，也包括公平和信任。','Zhè jiàn shì shèjí de bù zhǐshì xiàolǜ, yě bāokuò gōngpíng hé xìnrèn.','Bu konu yalnızca verimlilikle değil, adalet ve güvenle de ilgili.'),
('我理解你的立场，不过我想从另一个角度补充一点。','Wǒ lǐjiě nǐ de lìchǎng, búguò wǒ xiǎng cóng lìng yí ge jiǎodù bǔchōng yìdiǎn.','Bakış açını anlıyorum ama başka bir açıdan bir nokta eklemek istiyorum.'),
('如果我们现在回避这个问题，以后付出的成本可能更高。','Rúguǒ wǒmen xiànzài huíbì zhège wèntí, yǐhòu fùchū de chéngběn kěnéng gèng gāo.','Bu sorundan şimdi kaçınırsak ileride ödeyeceğimiz bedel daha yüksek olabilir.'),
('这不是简单的对错问题，而是不同目标之间怎么平衡。','Zhè bú shì jiǎndān de duì cuò wèntí, ér shì bùtóng mùbiāo zhījiān zěnme pínghéng.','Bu basitçe doğru-yanlış meselesi değil; farklı hedeflerin nasıl dengeleneceği meselesi.'),
('我们可以先设一个评估标准，再比较几个选择。','Wǒmen kěyǐ xiān shè yí ge pínggū biāozhǔn, zài bǐjiào jǐ ge xuǎnzé.','Önce bir değerlendirme ölçütü belirleyip sonra seçenekleri karşılaştırabiliriz.'),
('我希望这个决定既尊重个人选择，也照顾整体需要。','Wǒ xīwàng zhège juédìng jì zūnzhòng gèrén xuǎnzé, yě zhàogù zhěngtǐ xūyào.','Bu kararın hem bireysel seçime saygı göstermesini hem de genel ihtiyacı gözetmesini istiyorum.'),
('从长远来看，稳定并不一定等于不改变。','Cóng chángyuǎn lái kàn, wěndìng bìng bù yídìng děngyú bù gǎibiàn.','Uzun vadede istikrar her zaman değişmemek anlamına gelmez.'),
('有时候承认不知道，比假装确定更负责任。','Yǒu shíhou chéngrèn bù zhīdào, bǐ jiǎzhuāng quèdìng gèng fù zérèn.','Bazen bilmediğini kabul etmek, kesinmiş gibi davranmaktan daha sorumlucadır.'),
('先把能够确认的部分确认下来，剩下的再继续核实。','Xiān bǎ nénggòu quèrèn de bùfen quèrèn xiàlái, shèngxià de zài jìxù héshí.','Önce doğrulayabildiğimiz kısmı netleştirip kalanını araştırmaya devam edelim.'),
('我不反对这个方向，只是希望执行的时候留一点调整空间。','Wǒ bù fǎnduì zhège fāngxiàng, zhǐshì xīwàng zhíxíng de shíhou liú yìdiǎn tiáozhěng kōngjiān.','Bu yöne karşı değilim; sadece uygularken biraz ayarlama payı bırakılmasını istiyorum.'),
('如果情况和我们的假设不同，就要及时修改计划。','Rúguǒ qíngkuàng hé wǒmen de jiǎshè bùtóng, jiù yào jíshí xiūgǎi jìhuà.','Durum varsayımımızdan farklıysa planı zamanında değiştirmeliyiz.'),
('我更关心的是，这个选择会给谁带来什么影响。','Wǒ gèng guānxīn de shì, zhège xuǎnzé huì gěi shéi dàilái shénme yǐngxiǎng.','Benim daha çok önemsediğim, bu seçimin kimi nasıl etkileyeceği.'),
('只要目标一致，方法上有一点差异是可以讨论的。','Zhǐyào mùbiāo yízhì, fāngfǎ shàng yǒu yìdiǎn chāyì shì kěyǐ tǎolùn de.','Hedefimiz aynı olduğu sürece yöntem farklılıkları tartışılabilir.'),
('现在大家的立场已经比开始时清楚多了。','Xiànzài dàjiā de lìchǎng yǐjīng bǐ kāishǐ shí qīngchu duō le.','Şimdi herkesin duruşu başlangıca göre çok daha net.'),
('我们还需要考虑一个现实问题：时间和资源够不够。','Wǒmen hái xūyào kǎolǜ yí ge xiànshí wèntí: shíjiān hé zīyuán gòu bú gòu.','Bir pratik konuyu daha düşünmeliyiz: zaman ve kaynak yeterli mi?'),
('这个提醒很重要，不然方案看起来很好，实际却做不了。','Zhège tíxǐng hěn zhòngyào, bùrán fāng’àn kàn qǐlái hěn hǎo, shíjì què zuò bùliǎo.','Bu uyarı önemli; yoksa plan kâğıt üzerinde iyi görünüp uygulamada imkânsız olabilir.'),
('我们先把最坏的情况想清楚，再决定能不能承担。','Wǒmen xiān bǎ zuì huài de qíngkuàng xiǎng qīngchu, zài juédìng néng bù néng chéngdān.','Önce en kötü senaryoyu netleştirip taşıyıp taşıyamayacağımıza karar verelim.'),
('风险不是不能接受，而是要知道风险在哪里。','Fēngxiǎn bú shì bù néng jiēshòu, ér shì yào zhīdào fēngxiǎn zài nǎlǐ.','Risk asla kabul edilemez değildir; önemli olan riskin nerede olduğunu bilmektir.'),
('我觉得现在的信息已经足够支持一个暂时的决定。','Wǒ juéde xiànzài de xìnxī yǐjīng zúgòu zhīchí yí ge zànshí de juédìng.','Bence mevcut bilgiler geçici bir kararı desteklemek için yeterli.'),
('那就先设一个检查时间，到时候再看结果。','Nà jiù xiān shè yí ge jiǎnchá shíjiān, dào shíhou zài kàn jiéguǒ.','O halde bir kontrol tarihi belirleyip o zaman sonucu yeniden değerlendirelim.'),
('这样既不会拖得太久，也不会太草率。','Zhèyàng jì bú huì tuō de tài jiǔ, yě bú huì tài cǎoshuài.','Böylece ne gereğinden fazla uzar ne de aceleci davranmış oluruz.'),
('我同意，关键是把后续责任也分清楚。','Wǒ tóngyì, guānjiàn shì bǎ hòuxù zérèn yě fēn qīngchu.','Katılıyorum; önemli olan sonraki sorumlulukları da netleştirmek.'),
('如果出了问题，不应该只找一个人承担。','Rúguǒ chū le wèntí, bù yīnggāi zhǐ zhǎo yí ge rén chéngdān.','Bir sorun çıkarsa sorumluluğu yalnızca tek kişiye yüklememeliyiz.'),
('团队做的决定，也需要团队一起面对结果。','Tuánduì zuò de juédìng, yě xūyào tuánduì yìqǐ miànduì jiéguǒ.','Ekipçe verilen kararın sonucuyla da ekipçe yüzleşmek gerekir.'),
('我会把今天的结论和还没解决的问题分别记录下来。','Wǒ huì bǎ jīntiān de jiélùn hé hái méi jiějué de wèntí fēnbié jìlù xiàlái.','Bugünkü sonuçlarla henüz çözülmemiş sorunları ayrı ayrı kaydedeceğim.'),
('这样下次讨论的时候就不用从头开始。','Zhèyàng xià cì tǎolùn de shíhou jiù bú yòng cóngtóu kāishǐ.','Böylece bir sonraki görüşmede baştan başlamak gerekmez.'),
('有些问题今天解决不了，但至少方向已经明确了。','Yǒuxiē wèntí jīntiān jiějué bùliǎo, dàn zhìshǎo fāngxiàng yǐjīng míngquè le.','Bazı sorunlar bugün çözülemese de en azından yön netleşti.'),
('我觉得这次讨论比单纯追求一个答案更有价值。','Wǒ juéde zhè cì tǎolùn bǐ dānchún zhuīqiú yí ge dá’àn gèng yǒu jiàzhí.','Bence bu tartışma tek bir cevabın peşinden gitmekten daha değerliydi.'),
('至少我们知道每个人真正担心的是什么。','Zhìshǎo wǒmen zhīdào měi ge rén zhēnzhèng dānxīn de shì shénme.','En azından artık herkesin gerçekten neden endişelendiğini biliyoruz.'),
('只要继续保持这种沟通方式，后面的分歧会更容易处理。','Zhǐyào jìxù bǎochí zhè zhǒng gōutōng fāngshì, hòumiàn de fēnqí huì gèng róngyì chǔlǐ.','Bu iletişim biçimini sürdürürsek sonraki görüş ayrılıklarını çözmek daha kolay olur.'),
('那我们就按照今天确定的优先顺序推进。','Nà wǒmen jiù ànzhào jīntiān quèdìng de yōuxiān shùnxù tuījìn.','O zaman bugün belirlediğimiz öncelik sırasına göre ilerleyelim.'),
('第一步先处理最紧急、影响最大的问题。','Dì yí bù xiān chǔlǐ zuì jǐnjí, yǐngxiǎng zuì dà de wèntí.','İlk olarak en acil ve en büyük etkiye sahip sorunu ele alalım.'),
('剩下的问题按照时间表逐步解决。','Shèngxià de wèntí ànzhào shíjiānbiǎo zhúbù jiějué.','Kalan sorunları zaman çizelgesine göre adım adım çözelim.'),
('如果有人发现新情况，要尽快共享信息。','Rúguǒ yǒu rén fāxiàn xīn qíngkuàng, yào jǐnkuài gòngxiǎng xìnxī.','Yeni bir durum fark eden olursa bilgiyi mümkün olduğunca hızlı paylaşmalı.'),
('透明一点，大家反而更容易建立信任。','Tòumíng yìdiǎn, dàjiā fǎn’ér gèng róngyì jiànlì xìnrèn.','Daha şeffaf olmak, aslında güven kurmayı kolaylaştırır.'),
('这次的经验以后还能用在别的事情上。','Zhè cì de jīngyàn yǐhòu hái néng yòng zài bié de shìqing shàng.','Bu deneyimi ileride başka konularda da kullanabiliriz.'),
('好，今天先到这里，下一步按计划继续。','Hǎo, jīntiān xiān dào zhèlǐ, xià yí bù àn jìhuà jìxù.','Tamam, bugünlük burada bitirelim; sonraki adım plana göre devam etsin.')
]

def intro(key):
    zh,py,tr=W[key]
    return (f'最近我一直在想{zh}这件事。',f'Zuìjìn wǒ yìzhí zài xiǎng {py} zhè jiàn shì.',f'Son zamanlarda {tr} meselesini düşünüyorum.')

def usage(key,v=0):
    zh,py,tr=W[key]
    special={
      'raiseprice':[
        ('如果现在涨价，老顾客可能会有意见。','Rúguǒ xiànzài zhǎngjià, lǎo gùkè kěnéng huì yǒu yìjiàn.','Şimdi fiyat artırırsak düzenli müşteriler itiraz edebilir.'),
        ('涨价以前，我们得先把成本变化算清楚。','Zhǎngjià yǐqián, wǒmen děi xiān bǎ chéngběn biànhuà suàn qīngchu.','Fiyat artırmadan önce maliyet değişimini net hesaplamalıyız.'),
        ('我不反对涨价，但幅度要让顾客能够理解。','Wǒ bù fǎnduì zhǎngjià, dàn fúdù yào ràng gùkè nénggòu lǐjiě.','Fiyat artışına karşı değilim ama oran müşterinin anlayabileceği düzeyde olmalı.')],
      'support2':[
        ('我想支持她，但不想替她做决定。','Wǒ xiǎng zhīchí tā, dàn bù xiǎng tì tā zuò juédìng.','Onu desteklemek istiyorum ama onun yerine karar vermek istemiyorum.'),
        ('真正的支持不一定等于直接给答案。','Zhēnzhèng de zhīchí bù yídìng děngyú zhíjiē gěi dá’àn.','Gerçek destek her zaman doğrudan cevap vermek demek değildir.'),
        ('她需要支持，也需要自己承担选择的结果。','Tā xūyào zhīchí, yě xūyào zìjǐ chéngdān xuǎnzé de jiéguǒ.','Desteğe ihtiyacı var ama seçiminin sonucunu da kendisi üstlenmeli.')],
      'intervene':[
        ('如果我们干预得太多，她反而很难学会自己判断。','Rúguǒ wǒmen gānyù de tài duō, tā fǎn’ér hěn nán xuéhuì zìjǐ pànduàn.','Çok fazla müdahale edersek kendi karar vermeyi öğrenmesi zorlaşabilir.'),
        ('什么时候需要干预，什么时候应该退一步，要看具体情况。','Shénme shíhou xūyào gānyù, shénme shíhou yīnggāi tuì yí bù, yào kàn jùtǐ qíngkuàng.','Ne zaman müdahale edip ne zaman geri çekilmek gerektiği duruma bağlıdır.')],
      'accepthelp':[
        ('接受帮助并不代表失去独立。','Jiēshòu bāngzhù bìng bù dàibiǎo shīqù dúlì.','Yardım kabul etmek bağımsızlığını kaybetmek anlamına gelmez.'),
        ('我们希望她愿意接受帮助，同时保留自己的选择。','Wǒmen xīwàng tā yuànyì jiēshòu bāngzhù, tóngshí bǎoliú zìjǐ de xuǎnzé.','Yardımı kabul ederken kendi seçimlerini de korumasını istiyoruz.')]
    }
    if key in special: return special[key][v%len(special[key])]
    return h4.usage(key,v)

def make_dialogues(scene):
    n=scene['number']; keys=V[n]; roles=ROLES[n]
    lines=[intro(keys[0]),intro(keys[1]),
      ('这次我们不能只凭感觉判断，最好把事实、影响和选择都摆出来。','Zhè cì wǒmen bù néng zhǐ píng gǎnjué pànduàn, zuìhǎo bǎ shìshí, yǐngxiǎng hé xuǎnzé dōu bǎi chūlái.','Bu kez yalnızca hislerimize göre karar veremeyiz; olguları, etkileri ve seçenekleri ortaya koymak daha iyi.'),
      ('我同意，先把问题定义清楚，后面的讨论才有意义。','Wǒ tóngyì, xiān bǎ wèntí dìngyì qīngchu, hòumiàn de tǎolùn cái yǒu yìyì.','Katılıyorum; önce sorunu net tanımlarsak sonraki tartışma anlamlı olur.'),
      ('那我们分别说说最在意的是什么。','Nà wǒmen fēnbié shuōshuo zuì zàiyì de shì shénme.','O zaman herkes en çok neyi önemsediğini söylesin.'),
      ('好，也把能确认的依据一起说出来。','Hǎo, yě bǎ néng quèrèn de yījù yìqǐ shuō chūlái.','Tamam, doğrulayabildiğimiz dayanakları da birlikte söyleyelim.')]
    reactions=[
      ('这个信息很关键。','Zhège xìnxī hěn guānjiàn.','Bu bilgi çok kritik.'),
      ('这样解释以后，我更理解你的立场了。','Zhèyàng jiěshì yǐhòu, wǒ gèng lǐjiě nǐ de lìchǎng le.','Böyle açıklayınca bakış açını daha iyi anladım.'),
      ('这一点值得继续确认。','Zhè yìdiǎn zhíde jìxù quèrèn.','Bu nokta doğrulanmaya devam edilmeye değer.'),
      ('我同意先把它列为优先问题。','Wǒ tóngyì xiān bǎ tā liè wéi yōuxiān wèntí.','Bunu öncelikli konu olarak belirlemeye katılıyorum.'),
      ('这个角度会影响最后的判断。','Zhège jiǎodù huì yǐngxiǎng zuìhòu de pànduàn.','Bu açı nihai değerlendirmeyi etkiler.'),
      ('我们也要看看有没有反面的证据。','Wǒmen yě yào kànkan yǒu méiyǒu fǎnmiàn de zhèngjù.','Ters yönde kanıt olup olmadığına da bakmalıyız.'),
      ('先记下来，等信息完整一点再决定。','Xiān jì xiàlái, děng xìnxī wánzhěng yìdiǎn zài juédìng.','Şimdilik not edelim, bilgiler biraz daha tamamlanınca karar veririz.'),
      ('我觉得这个建议比较稳妥。','Wǒ juéde zhège jiànyì bǐjiào wěntuǒ.','Bence bu öneri oldukça temkinli.')]
    for i,k in enumerate(keys[:8]):
        lines.append(usage(k,i)); lines.append(reactions[i%len(reactions)])
    lines.extend(COMMON5)
    idx=0
    while len(lines)<94:
        k=keys[idx%len(keys)]
        lines.append(usage(k,idx+3)); lines.append(reactions[(idx+3)%len(reactions)]); idx+=1
    lines=lines[:94]
    lines += [
      ('现在主要事实、风险和选择都比较清楚了。','Xiànzài zhǔyào shìshí, fēngxiǎn hé xuǎnzé dōu bǐjiào qīngchu le.','Artık temel olgular, riskler ve seçenekler oldukça net.'),
      ('我们先按今天确定的优先顺序执行。','Wǒmen xiān àn jīntiān quèdìng de yōuxiān shùnxù zhíxíng.','Önce bugün belirlediğimiz öncelik sırasına göre uygulayalım.'),
      ('如果新信息出现，就及时重新评估。','Rúguǒ xīn xìnxī chūxiàn, jiù jíshí chóngxīn pínggū.','Yeni bilgi çıkarsa zamanında yeniden değerlendirelim.'),
      ('这次的决定至少是建立在充分讨论上的。','Zhè cì de juédìng zhìshǎo shì jiànlì zài chōngfèn tǎolùn shàng de.','Bu karar en azından yeterli bir tartışmaya dayanıyor.'),
      ('我觉得大家都知道下一步该做什么了。','Wǒ juéde dàjiā dōu zhīdào xià yí bù gāi zuò shénme le.','Bence artık herkes bir sonraki adımda ne yapacağını biliyor.'),
      ('好，那就按计划继续，也别忘了留意变化。','Hǎo, nà jiù àn jìhuà jìxù, yě bié wàng le liúyì biànhuà.','Tamam, plana göre devam edelim ve değişiklikleri izlemeyi unutmayalım.')]
    return [{'id':f'DLG_ZH_HSK5_SC{n:03d}_{i:03d}','speaker':roles[(i-1)%len(roles)],'zh':zh,'pinyin':py,'tr':tr} for i,(zh,py,tr) in enumerate(lines[:100],1)]

def make_cards(scene):
    n=scene['number']; out=[]
    for i,k in enumerate(V[n],1):
        zh,py,tr=W[k]; ezh,epy,etr=usage(k,i)
        out.append({'id':f'VOC_ZH_HSK5_SC{n:03d}_{i:03d}','zh':zh,'pinyin':py,'tr':tr,'exampleZh':ezh,'examplePinyin':epy,'exampleTr':etr,'kind':'active' if i<=6 else 'review'})
    # defensive de-dup by surface form
    seen=set(); ded=[]
    for c in out:
        if c['zh'] in seen: continue
        seen.add(c['zh']); ded.append(c)
    return ded

def grammar_items(scene):
    n=scene['number']; g=scene['learning'].get('grammarTheme',''); topic=W[V[n][0]][0]
    templates={
      '尽管…仍然…':[
        {'type':'word_order','tokens':['尽管','情况很复杂','我们','仍然','要继续分析'],'answerTokens':['尽管','情况很复杂','我们','仍然','要继续分析']},
        {'type':'fill_blank','blankSentenceZh':'尽管结果不理想，我们___要面对问题。','options':['仍然','因此','相比'],'answer':'仍然'},
        {'type':'sentence_repair','tokens':['仍然','尽管','有压力','他','很冷静'],'answerTokens':['尽管','有压力','他','仍然','很冷静']}],
      '之所以…是因为…':[
        {'type':'word_order','tokens':['之所以','出现问题','是因为','准备不够'],'answerTokens':['之所以','出现问题','是因为','准备不够']},
        {'type':'fill_blank','blankSentenceZh':'我们之所以调整计划，___情况已经变了。','options':['是因为','仍然','无论'],'answer':'是因为'},
        {'type':'sentence_repair','tokens':['是因为','之所以','成功','大家合作得好'],'answerTokens':['之所以','成功','是因为','大家合作得好']}],
      '无论…都…':[
        {'type':'word_order','tokens':['无论','最后怎么决定','大家','都','要承担结果'],'answerTokens':['无论','最后怎么决定','大家','都','要承担结果']},
        {'type':'fill_blank','blankSentenceZh':'无论遇到什么变化，我们___要先核实信息。','options':['都','仍然是因为','相比'],'answer':'都'},
        {'type':'sentence_repair','tokens':['都','无论','谁负责','要说明理由'],'answerTokens':['无论','谁负责','都','要说明理由']}],
      '不仅…还…':[
        {'type':'word_order','tokens':['这个决定','不仅','影响现在','还','影响以后'],'answerTokens':['这个决定','不仅','影响现在','还','影响以后']},
        {'type':'fill_blank','blankSentenceZh':f'{topic}不仅关系到效率，___关系到公平。','options':['还','仍然','都'],'answer':'还'},
        {'type':'sentence_repair','tokens':['还','不仅','要考虑成本','要考虑体验'],'answerTokens':['不仅','要考虑成本','还','要考虑体验']}],
      '从…来看':[
        {'type':'word_order','tokens':['从','现有证据','来看','这个判断比较合理'],'answerTokens':['从','现有证据','来看','这个判断比较合理']},
        {'type':'fill_blank','blankSentenceZh':'从长期影响___，我们还需要更谨慎。','options':['来看','都','是因为'],'answer':'来看'},
        {'type':'sentence_repair','tokens':['来看','从','实际结果','方案需要调整'],'answerTokens':['从','实际结果','来看','方案需要调整']}],
      '与…相比':[
        {'type':'word_order','tokens':['与','以前的方案','相比','这个风险更低'],'answerTokens':['与','以前的方案','相比','这个风险更低']},
        {'type':'fill_blank','blankSentenceZh':'与短期收益___，长期稳定更重要。','options':['相比','仍然','都'],'answer':'相比'},
        {'type':'sentence_repair','tokens':['相比','与','去年','成本更高'],'answerTokens':['与','去年','相比','成本更高']}]
    }
    base=templates.get(g,templates['尽管…仍然…']); prompt={'word_order':'Kelimeleri doğru sıraya koy.','fill_blank':'Boşluğu doğru kelimeyle doldur.','sentence_repair':'Yanlış sıradaki cümleyi düzelt.'}
    out=[]
    for i in range(9):
        item=dict(base[i%3]); item['id']=f'SENT_ZH_HSK5_SC{n:03d}_{i+1:03d}'; item['promptTr']=prompt[item['type']]; out.append(item)
    return out

def make_comprehension(scene):
    n=scene['number']; title=scene['titleTr']; goal=scene['learning']['communicationGoals'][0]
    return [
      {'id':f'COMP_ZH_HSK5_SC{n:03d}_001','questionTr':'Bu sahnenin ana olayı hangisidir?','optionsTr':[title,'İlk taşınma günü','Sadece sayı sayma alıştırması'],'correctIndex':0},
      {'id':f'COMP_ZH_HSK5_SC{n:03d}_002','questionTr':'Sahnenin iletişim hedefi nedir?','optionsTr':[goal,'Yalnızca selamlaşmak','Sadece renk isimlerini öğrenmek'],'correctIndex':0},
      {'id':f'COMP_ZH_HSK5_SC{n:03d}_003','questionTr':'Karakterler karar verirken gerekçe veya kanıt kullanıyor mu?','optionsTr':['Evet','Hayır','Hiç konuşmuyorlar'],'correctIndex':0},
      {'id':f'COMP_ZH_HSK5_SC{n:03d}_004','questionTr':'Bu sahne hangi yaşam dönemindedir?','optionsTr':['Çocukların yetişkinliğe geçtiği, kariyer ve toplum konularının derinleştiği dönem','Ailenin ilk tren yolculuğu','Torunlarla son yaşlılık dönemi'],'correctIndex':0},
      {'id':f'COMP_ZH_HSK5_SC{n:03d}_005','questionTr':'Sahne sonunda bir karar, değerlendirme veya sonraki adım oluşuyor mu?','optionsTr':['Evet','Hayır','Sahne başlamadan bitiyor'],'correctIndex':0}]

def make_pron(scene,cards):
    n=scene['number']; return [{'id':f'PRON_ZH_HSK5_SC{n:03d}_{i:03d}','zh':c['exampleZh'],'pinyin':c['examplePinyin'],'tr':c['exampleTr'],'scoring':['pronunciation','toneAccuracy','fluency','timing','completeness']} for i,c in enumerate(cards[:5],1)]

def make_interactive(scene):
    n=scene['number']; topic=W[V[n][0]]
    return [
      {'id':f'INT_ZH_HSK5_SC{n:03d}_001','promptZh':'如果信息还不完整，你会怎么做？','promptPinyin':'Rúguǒ xìnxī hái bù wánzhěng, nǐ huì zěnme zuò?','promptTr':'Bilgi henüz tamamlanmamışsa ne yaparsın?','options':[{'zh':'先核实关键事实，再做判断。','tr':'Önce kritik olguları doğrular, sonra karar veririm.','correct':True},{'zh':'马上根据感觉决定。','tr':'Hemen hislerime göre karar veririm.','correct':False},{'zh':'不让任何人继续说话。','tr':'Kimsenin konuşmasına izin vermem.','correct':False}]},
      {'id':f'INT_ZH_HSK5_SC{n:03d}_002','promptZh':f'关于{topic[0]}，最需要考虑什么？','promptPinyin':f'Guānyú {topic[1]}, zuì xūyào kǎolǜ shénme?','promptTr':f'{topic[2].capitalize()} konusunda en çok neyi düşünmek gerekir?','options':[{'zh':'要同时考虑事实、影响和长期结果。','tr':'Olguları, etkileri ve uzun vadeli sonuçları birlikte düşünmek gerekir.','correct':True},{'zh':'只看谁说得声音大。','tr':'Yalnızca kimin daha yüksek sesle konuştuğuna bakmak gerekir.','correct':False},{'zh':'只看今天的天气。','tr':'Yalnızca bugünkü havaya bakmak gerekir.','correct':False}]},
      {'id':f'INT_ZH_HSK5_SC{n:03d}_003','promptZh':'如果你不同意对方，怎样表达更合适？','promptPinyin':'Rúguǒ nǐ bù tóngyì duìfāng, zěnyàng biǎodá gèng héshì?','promptTr':'Karşı tarafla aynı fikirde değilsen bunu en uygun nasıl ifade edersin?','options':[{'zh':'我理解你的理由，不过我想补充另一个角度。','tr':'Gerekçeni anlıyorum ama başka bir açı eklemek istiyorum.','correct':True},{'zh':'你完全错了，不用再说。','tr':'Tamamen yanılıyorsun, daha fazla konuşma.','correct':False},{'zh':'我不听任何解释。','tr':'Hiçbir açıklamayı dinlemiyorum.','correct':False}]},
      {'id':f'INT_ZH_HSK5_SC{n:03d}_004','promptZh':'做出决定以后还要做什么？','promptPinyin':'Zuòchū juédìng yǐhòu hái yào zuò shénme?','promptTr':'Karardan sonra ne yapmak gerekir?','options':[{'zh':'执行、观察结果，并根据新情况调整。','tr':'Uygulamak, sonucu izlemek ve yeni duruma göre ayarlamak gerekir.','correct':True},{'zh':'永远不再检查。','tr':'Bir daha asla kontrol etmemek gerekir.','correct':False},{'zh':'马上忘掉所有记录。','tr':'Bütün kayıtları hemen unutmak gerekir.','correct':False}]}
    ]

def make_production(scene):
    n=scene['number']
    return {'scenePurposeTr':scene.get('miniAdventureTr',''),'timeOfDay':'evening' if n in [2,21,22,23,32,34,39,40,47,48,49,50] else 'day','atmosphere':'doğal, olgun ve HSK5 düzeyinde gerekçe, kanıt, değer, profesyonel iletişim ve soyut değerlendirme odaklı Mandarin','characters':ROLES[n],'locationId':scene.get('locationId',''),'visual':{'reuseLocation':True,'newVisualRequired':False,'style':'visual_novel_theatre'},'audio':{'voiceLanguage':'zh-CN','narratorProfile':'NARRATOR_ZH_001','defaultSpeechSpeed':1.0},'animation':{'level':'normal','mouthMode':'AUTO_SIMPLE','blink':True,'speakerFocus':True},'continuityNoteTr':f"{scene['titleTr']} olayı HSK5 yaşam çizgisinde sahne {n} olarak kaydedilir; kariyer, yetişkin çocuklar, toplumsal sorumluluk ve yaşlanan aile büyükleriyle ilgili sonuçlar sonraki sahnelere aktarılır."}

def main():
    data=json.loads(PATH.read_text(encoding='utf-8')); assert len(data['scenes'])==50
    for scene in data['scenes']:
        n=scene['number']; cards=make_cards(scene); learning=dict(scene.get('learning') or {})
        learning.update({'vocabularyCards':cards,'sentenceExercises':grammar_items(scene),'comprehensionQuestions':make_comprehension(scene),'pronunciationItems':make_pron(scene,cards),'interactiveDialogue':make_interactive(scene),'examRules':{'vocabularyPassPercent':90,'sentencePassPercent':85,'lockNextSceneUntilPassed':True},'examStages':[{'stage':1,'type':'vocabulary','passPercent':90},{'stage':2,'type':'sentence','passPercent':85,'requiresStage':1}],'flashCardPolicy':{'allowPrevious':True,'allowNext':True,'allowFavorite':True,'favoritesStudyMode':True}})
        scene['learning']=learning; scene['dialogues']=make_dialogues(scene); scene['production']=make_production(scene)
        scene['complete']=True; scene['productionStatus']='complete'; scene['editorialStatus']='generated_full_v1_requires_native_review'; scene['dialogueCount']=len(scene['dialogues'])
    data['schemaVersion']=3; data['completeSceneCount']=50; data['editorialNoteTr']='HSK5 50 sahne veri olarak tamdır; ileri seviye doğal Mandarin, kültürel/pragmatik nüans ve ticari yayın öncesi native editör kontrolü önerilir.'
    PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('HSK5 authoring completed:',len(data['scenes']),'scenes,',sum(len(s['dialogues']) for s in data['scenes']),'dialogues')
if __name__=='__main__': main()
