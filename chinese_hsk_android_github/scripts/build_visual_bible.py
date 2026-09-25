#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTENT = ROOT/'app'/'src'/'main'/'assets'/'chinese_course'
MEDIA = CONTENT/'media'
PROMPTS = MEDIA/'prompts'

CORE_CHARACTERS = {
'CHR_ZH_ZHANGWEI_001': dict(display='张伟', pinyin='Zhāng Wěi', ageStart=42, gender='male', height='175 cm', build='medium',
    identity='Chinese man, oval-square face, warm brown eyes, straight black eyebrows, short neat black hair with a slightly high hairline, medium warm skin tone, calm attentive expression, no facial hair',
    baseOutfit='navy casual jacket, light blue shirt, charcoal trousers, practical dark shoes',
    personality='calm, responsible, warm, observant, quietly humorous',
    variants=['YOUNG_MIDDLE','MIDDLE','SENIOR']),
'CHR_ZH_LIUMEI_001': dict(display='刘梅', pinyin='Liú Méi', ageStart=40, gender='female', height='164 cm', build='medium',
    identity='Chinese woman, soft oval face, warm dark-brown eyes, naturally arched brows, shoulder-length black hair usually tied low or half-up, medium-light warm skin tone, friendly capable expression',
    baseOutfit='soft beige cardigan, muted green blouse, straight dark trousers, comfortable shoes',
    personality='resourceful, practical, warm, socially skilled, creative',
    variants=['YOUNG_MIDDLE','MIDDLE','SENIOR']),
'CHR_ZH_ZHANGYUTONG_001': dict(display='张雨桐', pinyin='Zhāng Yǔtóng', ageStart=16, gender='female', height='165 cm at late teen', build='slim-average',
    identity='Chinese teenage girl, oval face, expressive dark eyes, straight black hair in a clean ponytail with loose front strands, medium-light skin tone, intelligent slightly reserved expression',
    baseOutfit='simple contemporary high-school casual wear, light sweatshirt or school-appropriate jacket, dark trousers or modest skirt depending scene',
    personality='curious, thoughtful, independent, quietly ambitious',
    variants=['TEEN','YOUNG_ADULT','ADULT']),
'CHR_ZH_ZHANGLELE_001': dict(display='张乐乐', pinyin='Zhāng Lèlè', ageStart=8, gender='male', height='128 cm at start', build='child-average',
    identity='Chinese boy, round-oval face, bright dark eyes, short slightly tousled black hair, medium-light skin tone, energetic open expression',
    baseOutfit='comfortable colorful hoodie or T-shirt, practical trousers, trainers',
    personality='playful, curious, affectionate, impulsive, optimistic',
    variants=['CHILD','TEEN','YOUNG_ADULT']),
'CHR_ZH_MIMI_001': dict(display='咪咪', pinyin='Mīmī', ageStart=3, gender='cat', height='domestic cat', build='small',
    identity='short-haired silver tabby cat with white chest and front paws, green-gold eyes, small pink nose, distinctive dark M marking on forehead',
    baseOutfit='no clothing, teal safety collar with small round tag',
    personality='curious, affectionate, mildly mischievous',
    variants=['ADULT_CAT','OLDER_CAT']),
'CHR_ZH_LICHEN_001': dict(display='李晨', pinyin='Lǐ Chén', ageStart=43, gender='male', height='178 cm', build='medium',
    identity='Chinese man, rectangular face, friendly dark eyes, short black hair with tidy side part, thin dark rectangular glasses, medium warm skin tone, approachable smile',
    baseOutfit='charcoal casual coat, warm-toned knit or polo shirt, dark trousers',
    personality='helpful, sociable, dependable, practical, good-humored',
    variants=['YOUNG_MIDDLE','MIDDLE','SENIOR']),
'CHR_ZH_AUTO_78E3EA6550': dict(display='李晨妻子', pinyin='Lǐ Chén qīzi', ageStart=41, gender='female', height='162 cm', build='medium',
    identity='Chinese woman, softly rounded face, warm dark eyes, neat chin-length black bob, medium-light warm skin tone, confident welcoming smile',
    baseOutfit='warm rust cardigan, cream blouse, dark straight trousers, simple jewelry',
    personality='friendly, observant, lively, tactful, family-oriented',
    variants=['YOUNG_MIDDLE','MIDDLE','SENIOR']),
'CHR_ZH_AUTO_BF795B2847': dict(display='爷爷', pinyin='Yéye', ageStart=68, gender='male', height='171 cm', build='lean-sturdy',
    identity='older Chinese man, weathered rectangular face, kind deep-set eyes, short grey hair, sun-warmed skin, strong hands from farm work, calm dignified posture',
    baseOutfit='simple checked shirt, dark work trousers, practical jacket, sturdy shoes',
    personality='experienced, patient, proud of farming, quietly humorous',
    variants=['SENIOR','OLDER_SENIOR']),
'CHR_ZH_AUTO_FE4C23D628': dict(display='奶奶', pinyin='Nǎinai', ageStart=66, gender='female', height='158 cm', build='medium-sturdy',
    identity='older Chinese woman, softly square face, kind alert dark eyes, black-and-silver hair in a low practical bun, warm medium-light skin tone, capable reassuring expression',
    baseOutfit='soft patterned blouse, practical cardigan, dark trousers, comfortable flat shoes',
    personality='highly capable, practical, nurturing, direct but kind',
    variants=['SENIOR','OLDER_SENIOR']),
}

LOCATION_BIBLES = {
'LOC_ZH_NEW_HOME_001': dict(name='张家新家 / Zhang ailesinin yeni evi', layout='modern modest three-bedroom apartment; open living-dining zone, kitchen opening at rear-right, hallway to bedrooms on left, balcony windows across rear wall', fixed='light oak floor, warm off-white walls, grey fabric sofa, rectangular wood dining table, low media cabinet, family photo shelf added gradually', mood='warm lived-in family home, practical not luxurious'),
'LOC_ZH_FAMILY_CAFE_001': dict(name='家庭咖啡馆 / Aile kafesi', layout='cozy neighborhood café; entrance front-right, service counter rear-left, pastry display near counter, eight small tables, window seating along front, compact open prep area behind counter', fixed='warm wood, muted sage accents, cream walls, hanging pendant lamps, chalk-style menu board area without baked-in text, family recipe shelf', mood='welcoming, intimate, community-centered'),
'LOC_ZH_WORKPLACE_001': dict(name='张伟工作单位 / Zhang’ın iş yeri', layout='contemporary mid-sized company office; shared desks center, supervisor glass room rear-right, meeting room visible rear-left, corridor entrance front-right', fixed='neutral grey desks, blue-grey partitions, practical fluorescent/soft LED office lighting, plants used sparingly', mood='professional, realistic, modestly modern'),
'LOC_ZH_HIGH_SCHOOL_001': dict(name='新城高中 / Lise', layout='modern public high-school classroom and corridor visual identity; large windows, rows of desks, teacher desk front, noticeboard area', fixed='light walls, dark green/blue teaching board, pale desks, practical institutional lighting', mood='busy, youthful, realistic'),
'LOC_ZH_PRIMARY_SCHOOL_001': dict(name='新城小学 / İlkokul', layout='bright primary classroom with lower desks, colorful but not childish wall displays, reading corner, windows on one side', fixed='light wood desks, white walls with limited learning posters, storage cubbies', mood='safe, active, cheerful'),
'LOC_ZH_LICHEN_HOME_001': dict(name='李晨家 / Li Chen’in evi', layout='comfortable apartment living-dining room; dining table near window, sofa facing low cabinet, family bookshelf, compact open kitchen nearby', fixed='slightly warmer colors than Zhang home, walnut wood details, framed family photos', mood='sociable, welcoming, familiar'),
'LOC_ZH_PARK_001': dict(name='社区公园 / Mahalle parkı', layout='walkable neighborhood park with curved path, small lawn, mature trees, benches, modest children play area in distance', fixed='stone path, dark wood benches, low planting beds, no landmark-specific architecture', mood='calm community green space'),
'LOC_ZH_COMMUNITY_CENTER_001': dict(name='社区活动中心 / Topluluk merkezi', layout='multi-purpose community hall with movable tables, bulletin wall, storage side, small stage at rear', fixed='neutral light walls, stackable chairs, practical flooring, red/blue accents used sparingly', mood='functional, inclusive, volunteer-friendly'),
'LOC_ZH_GRANDPARENTS_HOME_001': dict(name='爷爷奶奶家 / Büyükanne-büyükbaba evi', layout='smaller apartment near family; living room connected to compact kitchen, balcony used for plants, simple guest room', fixed='older solid wood furniture mixed with newer practical pieces, plant pots, sewing basket, framed family photos', mood='traditional touches within contemporary ordinary home'),
'LOC_ZH_GRANDPARENTS_FARM_001': dict(name='爷爷的农场 / Büyükbabanın çiftliği', layout='small family farm outside town; vegetable rows, modest farmhouse, tool shed, dirt path, low greenhouse tunnel', fixed='weathered tools, irrigation hose, baskets, seasonal crops', mood='worked-in, authentic, peaceful'),
'LOC_ZH_UNIVERSITY_001': dict(name='大学校园 / Üniversite', layout='modern university campus/classroom identity; broad pedestrian paths, academic building lobby, flexible lecture room', fixed='concrete/light stone architecture, trees, notice boards, practical lecture furniture', mood='independent, energetic, forward-looking'),
'LOC_ZH_HOSPITAL_001': dict(name='医院 / Hastane', layout='clean modern general hospital; registration zone or patient room depending scene, clear corridor geometry', fixed='white and pale blue/green palette, durable flooring, simple seating, medical equipment only when scene requires', mood='professional, calm, not melodramatic'),
'LOC_ZH_NEW_STATION_001': dict(name='新城火车站 / Yeni kasaba istasyonu', layout='medium-sized contemporary railway station arrival hall; exit gates rear, information signs, taxi direction, seating edge', fixed='light stone floor, metal/glass architecture, practical signage zones without baked-in readable text', mood='busy but navigable, first-arrival energy'),
'LOC_ZH_TRAIN_001': dict(name='火车 / Tren', layout='modern intercity train carriage; 2+2 seating, overhead luggage racks, large windows, aisle center', fixed='blue-grey seats, clean light interior, fold-down tray tables', mood='comfortable realistic travel'),
'LOC_ZH_TOWN_CENTER_001': dict(name='城中心 / Kasaba merkezi', layout='walkable medium-sized town center; mixed small shops, low-midrise buildings, broad sidewalk, crossing, trees', fixed='contemporary Chinese urban context without famous landmark dependence', mood='lively local everyday life'),
}

STYLE = {
    'styleId':'VISUAL_STYLE_ZH_001',
    'name':'Warm Semi-Realistic Visual Novel',
    'description':'semi-realistic 2D illustrated visual-novel art, contemporary China, clean shapes, soft painterly shading, believable anatomy, warm human expressions, cinematic but everyday realism',
    'characterMaster':'full-body isolated character, transparent background, 3/4 standing pose, neutral camera, consistent facial identity, soft studio-like light, no text, no watermark, no cropped limbs',
    'backgroundMaster':'16:9 environment plate, eye-level camera, empty of primary story characters, believable contemporary Chinese everyday architecture, reusable composition with clear foreground/midground/background, no readable brand text, no watermark',
    'negative':'no celebrity likeness, no exaggerated anime proportions, no chibi, no fantasy costume, no glamorized luxury, no warped hands, no extra fingers, no embedded subtitles, no logos, no watermarks',
    'runtime':{'character':'768x1152 WebP transparent','background':'1280x720 WebP','qualityHint':'WebP quality 80-86; reuse assets; source masters may be larger'}
}


def dump(path,obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def char_prompt(cid,d):
    return f"""ASSET ID: {cid}\nSTYLE: {STYLE['description']}\nSUBJECT: {d['display']} ({d['pinyin']}); {d['gender']}; starting age about {d['ageStart']}.\nIDENTITY LOCK: {d['identity']}.\nBODY: height/build {d['height']}, {d['build']}.\nBASE OUTFIT: {d['baseOutfit']}.\nPERSONALITY EXPRESSION: {d['personality']}.\nPOSE: relaxed 3/4 standing pose, arms naturally visible, neutral friendly expression, full body, front-facing enough for dialogue UI.\nOUTPUT: isolated transparent background character master, consistent face for all future variants.\nNEGATIVE: {STYLE['negative']}.\nVARIANTS TO DERIVE WITHOUT CHANGING IDENTITY: {', '.join(d['variants'])}.\n"""


def loc_prompt(lid,d):
    return f"""ASSET ID: {lid}_DAY\nSTYLE: {STYLE['description']}\nLOCATION: {d['name']}.\nLAYOUT LOCK: {d['layout']}.\nFIXED DETAILS: {d['fixed']}.\nMOOD: {d['mood']}.\nCAMERA: eye-level 16:9 reusable visual-novel background, wide enough for 3-4 character layers, keep major furniture/doors/windows in stable positions.\nOUTPUT: empty environment plate, daylight master, 1280x720 runtime target (larger source master allowed).\nNEGATIVE: {STYLE['negative']}; no primary story characters; no readable text baked into signs.\nFUTURE VARIANTS: NIGHT, RAIN, HOLIDAY only by changing light/weather/decor; never move architecture or fixed furniture.\n"""


def level_variant_map(variants):
    if variants == ['YOUNG_MIDDLE','MIDDLE','SENIOR']:
        names={'HSK1':'YOUNG_MIDDLE','HSK2':'YOUNG_MIDDLE','HSK3':'MIDDLE','HSK4':'MIDDLE','HSK5':'SENIOR','HSK6':'SENIOR'}
    elif variants == ['TEEN','YOUNG_ADULT','ADULT']:
        names={'HSK1':'TEEN','HSK2':'TEEN','HSK3':'YOUNG_ADULT','HSK4':'YOUNG_ADULT','HSK5':'ADULT','HSK6':'ADULT'}
    elif variants == ['CHILD','TEEN','YOUNG_ADULT']:
        names={'HSK1':'CHILD','HSK2':'CHILD','HSK3':'TEEN','HSK4':'TEEN','HSK5':'YOUNG_ADULT','HSK6':'YOUNG_ADULT'}
    elif variants == ['ADULT_CAT','OLDER_CAT']:
        names={'HSK1':'ADULT_CAT','HSK2':'ADULT_CAT','HSK3':'ADULT_CAT','HSK4':'ADULT_CAT','HSK5':'OLDER_CAT','HSK6':'OLDER_CAT'}
    elif variants == ['SENIOR','OLDER_SENIOR']:
        names={'HSK1':'SENIOR','HSK2':'SENIOR','HSK3':'SENIOR','HSK4':'SENIOR','HSK5':'SENIOR','HSK6':'OLDER_SENIOR'}
    else:
        names={level:(variants[0] if variants else '') for level in ['HSK1','HSK2','HSK3','HSK4','HSK5','HSK6']}
    return names

def main():
    PROMPTS.mkdir(parents=True, exist_ok=True)
    (PROMPTS/'characters').mkdir(parents=True, exist_ok=True)
    (PROMPTS/'locations').mkdir(parents=True, exist_ok=True)
    bible={'schemaVersion':1,'style':STYLE,'coreCharacters':[],'coreLocations':[],'rules':{
        'identityLock':'face shape, eye shape, brow shape, nose, hairline and silhouette remain stable across age/outfit variants',
        'ageing':'age variants add subtle age cues gradually; never replace the person with a new face',
        'locationLock':'doors, windows, counters, major furniture and camera family stay spatially consistent',
        'layering':'background + transparent characters + props/effects + subtitles',
        'newAssetDecision':'reuse exact asset first; then variant; generate new only when neither satisfies the scene'
    }}
    for cid,d in CORE_CHARACTERS.items():
        asset=f'chinese_course/media/characters/{cid}/base.webp'
        variants=[f'chinese_course/media/characters/{cid}/{v.lower()}.webp' for v in d['variants']]
        promptFile=f'chinese_course/media/prompts/characters/{cid}.txt'
        variantMap={v: f'chinese_course/media/characters/{cid}/{v.lower()}.webp' for v in d['variants']}
        levelVariantNames=level_variant_map(d['variants'])
        portraitByLevel={level:variantMap.get(name,asset) for level,name in levelVariantNames.items()}
        bible['coreCharacters'].append({'characterId':cid,**d,'baseAsset':asset,'variantAssets':variants,'variantMap':variantMap,'levelVariantNames':levelVariantNames,'portraitByLevel':portraitByLevel,'promptFile':promptFile,'status':'prompt_ready_binary_missing'})
        (PROMPTS/'characters'/f'{cid}.txt').write_text(char_prompt(cid,d),encoding='utf-8')
    for lid,d in LOCATION_BIBLES.items():
        base=f'chinese_course/media/backgrounds/{lid}_DAY.webp'
        variants={k:f'chinese_course/media/backgrounds/{lid}_{k}.webp' for k in ['NIGHT','RAIN','HOLIDAY']}
        promptFile=f'chinese_course/media/prompts/locations/{lid}.txt'
        bible['coreLocations'].append({'locationId':lid,**d,'baseAsset':base,'variantAssets':variants,'promptFile':promptFile,'status':'prompt_ready_binary_missing'})
        (PROMPTS/'locations'/f'{lid}.txt').write_text(loc_prompt(lid,d),encoding='utf-8')
    dump(MEDIA/'visual_bible.json',bible)

    # Expose age/identity variants to the Android runtime through characters.json.
    characters_path=CONTENT/'characters.json'
    if characters_path.exists():
        characters=json.loads(characters_path.read_text(encoding='utf-8'))
        by_id={x['characterId']:x for x in bible['coreCharacters']}
        for item in characters.get('characters',[]):
            entry=by_id.get(item.get('id'))
            if entry:
                item['portraitAsset']=entry['baseAsset']
                item['portraitVariants']=entry['variantMap']
                item['portraitByLevel']=entry['portraitByLevel']
                item['visualIdentityLocked']=True
        dump(characters_path,characters)

    # supplement visual manifest generated by build_media_catalog
    vm_path=MEDIA/'visual_manifest.json'
    vm=json.loads(vm_path.read_text(encoding='utf-8')) if vm_path.exists() else {'schemaVersion':2,'backgrounds':[],'characters':[]}
    vm['schemaVersion']=2
    vm['styleId']=STYLE['styleId']
    vm['visualBible']='chinese_course/media/visual_bible.json'
    corec={x['characterId']:x for x in bible['coreCharacters']}
    corel={x['locationId']:x for x in bible['coreLocations']}
    for x in vm.get('characters',[]):
        if x['characterId'] in corec:
            x['status']='prompt_ready_binary_missing'; x['promptFile']=corec[x['characterId']]['promptFile']; x['variants']=corec[x['characterId']]['variantAssets']
    for x in vm.get('backgrounds',[]):
        if x['locationId'] in corel:
            x['status']='prompt_ready_binary_missing'; x['promptFile']=corel[x['locationId']]['promptFile']; x['variants']=corel[x['locationId']]['variantAssets']
    dump(vm_path,vm)
    status_path=CONTENT/'content_status.json'
    if status_path.exists():
        status=json.loads(status_path.read_text(encoding='utf-8'))
        status['visualProduction']={
            'styleId':STYLE['styleId'],
            'coreCharacterBibles':len(CORE_CHARACTERS),
            'coreLocationBibles':len(LOCATION_BIBLES),
            'promptReadyAssets':len(CORE_CHARACTERS)+len(LOCATION_BIBLES),
            'binaryAssetsBundled':0,
            'state':'visual_identity_locked_prompts_ready'
        }
        dump(status_path,status)
    print(f"Visual bible: {len(CORE_CHARACTERS)} core characters, {len(LOCATION_BIBLES)} core locations, {len(CORE_CHARACTERS)+len(LOCATION_BIBLES)} prompt files.")

if __name__=='__main__': main()
