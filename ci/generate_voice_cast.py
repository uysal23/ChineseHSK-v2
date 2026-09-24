#!/usr/bin/env python3
"""Deterministic voice casting for the Chinese HSK app.

Reads canonical characters + scene catalog and emits ci/voice_cast_manifest.json.
The cast deliberately uses the 8 named Mandarin Kokoro voices as base identities.
Child/age variation is expressed as offline speed/pitch/energy metadata; the base
voice identity stays stable across HSK levels.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHARACTERS = ROOT / "ci/dialogue_source_snapshot/app/src/main/assets/chinese_course/characters.json"
CATALOG = ROOT / "docs/dialogue_naturalization/scene_catalog.json"
OUT = ROOT / "ci/voice_cast_manifest.json"

MAIN = {
  "张伟": {
    "g": "male",
    "age": "adult",
    "voice": "zm_yunyang",
    "tone": "sakin, güven veren, sıcak aile babası",
    "speed": 0.97,
    "pitch": -0.6,
    "ov": {
      "HSK1": {
        "age": "young_middle",
        "speed": 0.99,
        "pitch": -0.2
      },
      "HSK2": {
        "age": "young_middle",
        "speed": 0.99,
        "pitch": -0.2
      },
      "HSK3": {
        "age": "middle",
        "speed": 0.96,
        "pitch": -0.6
      },
      "HSK4": {
        "age": "middle",
        "speed": 0.95,
        "pitch": -0.8
      },
      "HSK5": {
        "age": "senior",
        "speed": 0.92,
        "pitch": -1.5
      },
      "HSK6": {
        "age": "senior",
        "speed": 0.9,
        "pitch": -1.9
      }
    }
  },
  "刘梅": {
    "g": "female",
    "age": "adult",
    "voice": "zf_xiaoyi",
    "tone": "sıcak, doğal, şefkatli ama kararlı",
    "speed": 0.99,
    "pitch": 0.1,
    "ov": {
      "HSK1": {
        "age": "young_middle",
        "speed": 1,
        "pitch": 0.2
      },
      "HSK2": {
        "age": "young_middle",
        "speed": 1,
        "pitch": 0.2
      },
      "HSK3": {
        "age": "middle",
        "speed": 0.97,
        "pitch": 0
      },
      "HSK4": {
        "age": "middle",
        "speed": 0.96,
        "pitch": -0.2
      },
      "HSK5": {
        "age": "senior",
        "speed": 0.93,
        "pitch": -0.8
      },
      "HSK6": {
        "age": "senior",
        "speed": 0.91,
        "pitch": -1.1
      }
    }
  },
  "李晨": {
    "g": "male",
    "age": "adult",
    "voice": "zm_yunxi",
    "tone": "samimi, sosyal, Zhang Wei'den biraz daha canlı",
    "speed": 0.99,
    "pitch": 0.3,
    "ov": {
      "HSK1": {
        "age": "young_middle",
        "speed": 1,
        "pitch": 0.4
      },
      "HSK2": {
        "age": "young_middle",
        "speed": 1,
        "pitch": 0.4
      },
      "HSK3": {
        "age": "middle",
        "speed": 0.97,
        "pitch": 0
      },
      "HSK4": {
        "age": "middle",
        "speed": 0.96,
        "pitch": -0.2
      },
      "HSK5": {
        "age": "senior",
        "speed": 0.93,
        "pitch": -1
      },
      "HSK6": {
        "age": "senior",
        "speed": 0.91,
        "pitch": -1.3
      }
    }
  },
  "李晨妻子": {
    "g": "female",
    "age": "adult",
    "voice": "zf_xiaoni",
    "tone": "sosyal, net, olgun ve sıcak",
    "speed": 0.99,
    "pitch": 0.1,
    "ov": {
      "HSK1": {
        "age": "young_middle",
        "speed": 1,
        "pitch": 0.2
      },
      "HSK2": {
        "age": "young_middle",
        "speed": 1,
        "pitch": 0.2
      },
      "HSK3": {
        "age": "middle",
        "speed": 0.97,
        "pitch": 0
      },
      "HSK4": {
        "age": "middle",
        "speed": 0.96,
        "pitch": -0.2
      },
      "HSK5": {
        "age": "senior",
        "speed": 0.93,
        "pitch": -0.8
      },
      "HSK6": {
        "age": "senior",
        "speed": 0.91,
        "pitch": -1.1
      }
    }
  },
  "张雨桐": {
    "g": "female",
    "age": "teen",
    "voice": "zf_xiaoxiao",
    "tone": "genç, canlı, zeki; yetişkinliğe doğru daha dengeli",
    "speed": 1.02,
    "pitch": 1.2,
    "ov": {
      "HSK1": {
        "age": "teen",
        "speed": 1.03,
        "pitch": 1.5
      },
      "HSK2": {
        "age": "teen",
        "speed": 1.03,
        "pitch": 1.4
      },
      "HSK3": {
        "age": "young_adult",
        "speed": 1.01,
        "pitch": 0.7
      },
      "HSK4": {
        "age": "young_adult",
        "speed": 1,
        "pitch": 0.5
      },
      "HSK5": {
        "age": "adult",
        "speed": 0.98,
        "pitch": 0.1
      },
      "HSK6": {
        "age": "adult",
        "speed": 0.97,
        "pitch": 0
      }
    }
  },
  "张乐乐": {
    "g": "male",
    "age": "child",
    "voice": "zm_yunxia",
    "tone": "çocukken neşeli ve yüksek; büyüdükçe doğal genç erkek",
    "speed": 1.06,
    "pitch": 3,
    "ov": {
      "HSK1": {
        "age": "child",
        "speed": 1.07,
        "pitch": 3.2
      },
      "HSK2": {
        "age": "child",
        "speed": 1.06,
        "pitch": 3
      },
      "HSK3": {
        "age": "teen",
        "speed": 1.04,
        "pitch": 1.8
      },
      "HSK4": {
        "age": "teen",
        "speed": 1.03,
        "pitch": 1.5
      },
      "HSK5": {
        "age": "young_adult",
        "speed": 1.01,
        "pitch": 0.6
      },
      "HSK6": {
        "age": "young_adult",
        "speed": 1,
        "pitch": 0.4
      }
    }
  },
  "奶奶": {
    "g": "female",
    "age": "senior",
    "voice": "zf_xiaobei",
    "tone": "yaşlı kadın, yumuşak, sabırlı, yavaş",
    "speed": 0.87,
    "pitch": -1.1
  },
  "爷爷": {
    "g": "male",
    "age": "senior",
    "voice": "zm_yunjian",
    "tone": "yaşlı erkek, tok, sakin, yavaş",
    "speed": 0.84,
    "pitch": -2.1
  },
  "旁白": {
    "g": "female",
    "age": "adult",
    "voice": "zf_xiaoni",
    "tone": "nötr, temiz, öğretici anlatıcı",
    "speed": 0.93,
    "pitch": 0
  },
  "咪咪": {
    "g": "nonhuman",
    "age": "pet",
    "voice": "zf_xiaoxiao",
    "tone": "kısa, sevimli evcil hayvan sesleri; mümkünse miyav SFX",
    "speed": 1.05,
    "pitch": 3.5
  },
  "张雨桐伴侣": {
    "g": "male",
    "age": "young_adult",
    "voice": "zm_yunxi",
    "tone": "genç yetişkin, sıcak ve dengeli",
    "speed": 1,
    "pitch": 0.4
  },
  "小朋友": {
    "g": "male",
    "age": "child",
    "voice": "zm_yunxia",
    "tone": "çocuk erkek, parlak ve enerjik",
    "speed": 1.07,
    "pitch": 3.3
  },
  "孙辈": {
    "g": "female",
    "age": "child",
    "voice": "zf_xiaoxiao",
    "tone": "çocuk, neşeli ve meraklı",
    "speed": 1.07,
    "pitch": 3
  },
  "同学": {
    "g": "female",
    "age": "child_or_teen",
    "voice": "zf_xiaoxiao",
    "tone": "öğrenci, genç ve doğal",
    "speed": 1.05,
    "pitch": 2
  },
  "新同学": {
    "g": "female",
    "age": "teen",
    "voice": "zf_xiaoxiao",
    "tone": "genç öğrenci, canlı ve samimi",
    "speed": 1.04,
    "pitch": 1.5
  },
  "亲家": {
    "g": "female",
    "age": "senior",
    "voice": "zf_xiaobei",
    "tone": "ileri yaş, sıcak ve ölçülü",
    "speed": 0.9,
    "pitch": -0.9
  },
  "王师傅": {
    "g": "male",
    "age": "senior",
    "voice": "zm_yunjian",
    "tone": "tecrübeli usta, tok ve sakin",
    "speed": 0.9,
    "pitch": -1.6
  },
  "老顾客": {
    "g": "male",
    "age": "senior",
    "voice": "zm_yunjian",
    "tone": "yaşlı müşteri, doğal ve ağırbaşlı",
    "speed": 0.91,
    "pitch": -1.4
  }
}
FEMALE = set(["主持人","伴侣","助理","护士","收银员","售货员","图书管理员","老师","服务员","店员","理发师","记者","导游","社区工作人员","酒店工作人员","银行工作人员","邻居","新朋友","好朋友","家人","宾客","居民","社区居民","环保小组成员","志愿者","顾客","年轻顾客"])
YOUNG_MALE = set(["年轻人","年轻创业者","青年志愿者","队友"])
PROFESSIONAL = set(["医生","兽医","律师","经理","场地方经理","面试官","招聘者","理财顾问","导师","记者","银行工作人员","公司职员","社区负责人","社区代表","技术志愿者"])
SERVICE = set(["司机","快递员","售货员","服务员","店员","收银员","导游","邮局工作人员","酒店工作人员","工作人员","摊主","商户"])

def base_for(ch):
    name = ch["nameZh"]
    if name in MAIN:
        return MAIN[name]
    gender = "female" if name in FEMALE else "male"
    age = "young_adult" if name in YOUNG_MALE else "adult"
    if gender == "female":
        if name in PROFESSIONAL:
            return dict(g=gender, age=age, voice="zf_xiaoni", tone="profesyonel, net, sakin", speed=.97, pitch=0)
        if name in SERVICE:
            return dict(g=gender, age=age, voice="zf_xiaoyi", tone="güler yüzlü, akıcı, hizmet odaklı", speed=1.01, pitch=.3)
        if age == "young_adult" or "年轻" in name:
            return dict(g=gender, age="young_adult", voice="zf_xiaoxiao", tone="genç, canlı ve doğal", speed=1.03, pitch=.8)
        return dict(g=gender, age=age, voice="zf_xiaoyi", tone="doğal, sıcak yetişkin kadın", speed=.99, pitch=.1)
    if name in YOUNG_MALE or "年轻" in name or "青年" in name:
        return dict(g="male", age="young_adult", voice="zm_yunxia", tone="genç, enerjik erkek", speed=1.03, pitch=.9)
    if name in PROFESSIONAL:
        return dict(g="male", age=age, voice="zm_yunjian", tone="profesyonel, tok ve ölçülü erkek", speed=.95, pitch=-.7)
    if name in SERVICE:
        return dict(g="male", age=age, voice="zm_yunyang", tone="dostça, anlaşılır yetişkin erkek", speed=1.0, pitch=-.1)
    return dict(g="male", age=age, voice="zm_yunxi", tone="doğal, samimi yetişkin erkek", speed=.99, pitch=.1)

def main():
    characters = json.loads(CHARACTERS.read_text(encoding="utf-8"))["characters"]
    raw_catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    scenes = raw_catalog if isinstance(raw_catalog, list) else raw_catalog.get("scenes", [])
    cast = []
    for ch in characters:
        b = base_for(ch)
        related = [s for s in scenes if ch["nameZh"] in s.get("speakers", [])]
        levels = sorted({s.get("level", "") for s in related if s.get("level")})
        cast.append({
            "characterId": ch["id"],
            "speaker": ch["nameZh"],
            "voiceProfileId": ch.get("voiceProfileId", ""),
            "genderPresentation": b["g"],
            "ageClass": b["age"],
            "intendedTone": b["tone"],
            "synthesis": {
                "engine": "kokoro-82m-mandarin",
                "voice": b["voice"],
                "speed": b["speed"],
                "pitchSemitones": b["pitch"],
                "energy": 1.08 if b["age"] == "child" else .92 if b["age"] == "senior" else 1.0,
            },
            "levelOverrides": b.get("ov", {}),
            "sceneCount": len(related),
            "levels": levels,
        })
    out = {
        "schemaVersion": 1,
        "status": "CAST_LOCKED_PRE_AUDIO",
        "generatedFrom": ["characters.json", "scene_catalog.json"],
        "policy": {
            "language": "cmn-Hans",
            "freeOfflinePrimary": "Kokoro-82M Mandarin named voices",
            "consistency": "Aynı karakter aynı temel voice embedding'i kullanır; yaş yalnızca hız/pitch/enerji ile evrilir.",
            "childPolicy": "Çocuk rolleri aynı cinsiyetteki Mandarin voice + offline pitch/speed post-processing ile çocuklaştırılır.",
            "narratorPolicy": "Anlatıcı ayrı ve nötr kadın sesidir.",
            "nonHumanPolicy": "Mimi için mümkünse kısa miyav/SFX; sözcük gerekiyorsa fallback zf_xiaoxiao.",
            "runtimeStrategy": "Önceden üretilmiş yerel Opus ses dosyaları > offline TTS fallback.",
        },
        "verifiedKokoroNamedMandarinVoices": {
            "female": ["zf_xiaobei", "zf_xiaoni", "zf_xiaoxiao", "zf_xiaoyi"],
            "male": ["zm_yunjian", "zm_yunxi", "zm_yunxia", "zm_yunyang"],
        },
        "cast": cast,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(cast)} cast entries to {OUT}")

if __name__ == "__main__":
    main()
