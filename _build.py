#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ZenBeads official site generator.

Generates index.html (zh-Hans), en.html, ko.html, th.html from a single
source of copy truth. Copy deck is aligned with ASC metadata v2.1
(deliverables/aso-metadata-v2.md) — do not invent feature promises here.
Also dumps the union of used characters (_fontchars.txt) for font subsetting.
"""
import os
import re

SITE = os.path.dirname(os.path.abspath(__file__))

# Canonical URLs — final deployment target; adjust here if the host changes.
CANON_BASE = "https://zenbeads-site.pages.dev"
PRIVACY_BASE = "/privacy"
APP_STORE = "https://apps.apple.com/app/id6821324992"
CONTACT = "yanoutech@163.com"

LANGS = ["zh-Hans", "en", "ko", "th"]
# lang -> (page file, hreflang, screenshot dir, privacy page, og image)
META = {
    "zh-Hans": ("index.html", "zh-Hans", "zh-Hans", "index.html", "assets/og/og-zh-Hans.jpg"),
    "en":      ("en.html",    "en",      "en-US",    "en.html",    "assets/og/og-en-US.jpg"),
    "ko":      ("ko.html",    "ko",      "ko",       "ko.html",    "assets/og/og-ko.jpg"),
    "th":      ("th.html",    "th",      "th",       "th.html",    "assets/og/og-th.jpg"),
}
OG_LOCALE = {"zh-Hans": "zh_CN", "en": "en_US", "ko": "ko_KR", "th": "th_TH"}

# ----------------------------------------------------------------------------
# Copy deck (MUST stay in sync with ASC metadata v2.1 — aso-metadata-v2.md)
# ----------------------------------------------------------------------------
COPY = {
    "zh-Hans": {
        "brand": "禅珠",
        "brand_latin": "ZenBeads",
        "tagline": "攒功德 · 步数换福袋 · 静心解压 · 许愿题壁",
        "hero_sub": "烦恼来的时候，敲一下就好。离线、私密、极简的电子佛珠与木鱼计数器。",
        "cta_small": "在 App Store 下载",
        "cta_big": "App Store",
        "lang_name": "简体中文",
        "skip": "跳到主要内容",
        "lang_label": "语言",
        "title": "禅珠 ZenBeads — 敲木鱼 · 108 念珠 · 今日功课 · 许愿壁纸",
        "meta_desc": "禅珠（ZenBeads）——离线、私密、极简的电子佛珠与木鱼计数器。敲木鱼攒功德，步数换算今日功课，许愿做成竖排题壁壁纸。无账号、无广告、无追踪、完全离线。",
        "og_title": "禅珠 ZenBeads · 敲一下，静一会儿",
        "og_desc": "电子木鱼 · 108 念珠 · 今日功课 · 许愿题壁。无账号、无广告、完全离线。",
        "features_title": "一珠一念，皆是功课",
        "features_sub": "五个安放注意力的地方",
        "features": [
            ("敲", "木鱼", "一次轻点，功德 +1。木鱼声配上今日佛语，把碎片时间变成片刻专注。", "01_knock"),
            ("走", "今日功课", "连接 Apple 健康，只读取步数与爬楼层数，自动换算今日功课；达标即得福袋。也可以完全不授权，用滑杆手动模拟。", "02_steps"),
            ("扮", "佛像", "用攒下的好运为小佛像换装：头饰、袈裟、配饰自由组合，慢慢攒，慢慢搭。", "03_wardrobe"),
            ("写", "心愿", "写下一句心愿，看它缓缓上飘。念起即觉，觉之即无。", "04_wish"),
            ("做", "壁纸", "把心愿或喜欢的话做成竖式题壁壁纸，7 档字号自适应，一键保存到相册。留白、竖排、书法字体，锁屏即道场。", "05_wallpaper"),
        ],
        "privacy_title": "无账号 · 无广告 · 无追踪 · 完全离线",
        "privacy_lead": "隐私承诺",
        "privacy_points": [
            ("无账号", "不需要注册，打开即用"),
            ("无广告", "没有横幅，没有插屏，没有声音"),
            ("无追踪", "不收集任何数据，不请求任何网络权限"),
            ("完全离线", "所有数据只留在这台设备上，卸载即清除"),
        ],
        "privacy_health": "健康数据只读取步数与爬楼层数，不写入、不上传；不授权也可用滑杆手动输入。",
        "gallery_title": "扮 · 佛像",
        "gallery_sub": "用攒下的好运，为小佛像换装：头饰、袈裟、配饰自由组合。",
        "gallery_alt": "佛像装扮组合",
        "gallery_hint": "横向滑动查看更多 →",
        "closing_title": "没有推送催促，没有排行榜。",
        "closing_text": "禅珠不会让你变得更好——它只是提醒你，你已经很好了。",
        "footer_privacy": "隐私政策",
        "footer_contact": "联系我们",
        "footer_font": "开源字体致谢：霞鹜文楷（LXGW WenKai），SIL Open Font License 1.1",
        "footer_rights": "保留所有权利。",
    },
    "en": {
        "brand": "ZenBeads",
        "brand_latin": "",
        "tagline": "Wooden Fish & Buddhist Chant",
        "hero_sub": "When a thought arises, tap it away. An offline, private, minimal set of prayer beads and a wooden-fish counter.",
        "cta_small": "Download on the",
        "cta_big": "App Store",
        "lang_name": "English",
        "skip": "Skip to content",
        "lang_label": "Language",
        "title": "ZenBeads — Prayer Beads & Wooden Fish, Fully Offline",
        "meta_desc": "ZenBeads — an offline, private, minimal set of Buddhist prayer beads and a wooden fish counter. One tap, one merit; today's steps become today's practice; turn a wish into a vertical wallpaper. No account, no ads, no tracking, fully offline.",
        "og_title": "ZenBeads · Tap. Breathe. Repeat.",
        "og_desc": "Buddhist prayer beads & wooden fish. No account, no ads, fully offline.",
        "features_title": "One bead, one breath",
        "features_sub": "Five places to rest your attention",
        "features": [
            ("Tap", "Wooden Fish", "One tap, one merit. The knock and a line of daily wisdom turn stray minutes into steady focus.", "01_knock"),
            ("Walk", "Daily Practice", "Reads only your step count and flights climbed from Apple Health, and turns the walk you already take into today's practice. Hit the goal, unlock a lucky pouch. Prefer not to grant access? Use the slider instead.", "02_steps"),
            ("Dress", "Buddha", "Spend the luck you've gathered to dress your little Buddha — headpieces, robes and accessories you can mix freely.", "03_wardrobe"),
            ("Write", "Wish", "Write one wish and watch it drift upward. Thoughts arise; notice them, and they pass.", "04_wish"),
            ("Make", "Wallpaper", "Turn a wish or a favourite phrase into a vertical temple-wall wallpaper with 7 auto-fitting type sizes. Save it in one tap. Your lock screen becomes your practice.", "05_wallpaper"),
        ],
        "privacy_title": "No account · No ads · No tracking · Fully offline",
        "privacy_lead": "Privacy promise",
        "privacy_points": [
            ("No account", "Open and start. Nothing to sign up for."),
            ("No ads", "No banners, no interstitials, no noise."),
            ("No tracking", "Nothing is collected; no network permission is ever requested."),
            ("Fully offline", "Everything stays on your device, and goes when you delete the app."),
        ],
        "privacy_health": "Health data is read-only: steps and flights climbed, never written, never uploaded. Prefer not to grant access? Use the slider instead.",
        "gallery_title": "Dress · Buddha",
        "gallery_sub": "Spend the luck you've gathered to dress your little Buddha — headpieces, robes and accessories you can mix freely.",
        "gallery_alt": "Buddha outfit combination",
        "gallery_hint": "Scroll sideways for more →",
        "closing_title": "No notifications nagging you. No leaderboards.",
        "closing_text": "ZenBeads won't make you better. It just reminds you: you are already enough.",
        "footer_privacy": "Privacy Policy",
        "footer_contact": "Contact",
        "footer_font": "Font credit: LXGW WenKai, licensed under the SIL Open Font License 1.1",
        "footer_rights": "All rights reserved.",
    },
    "ko": {
        "brand": "젠비즈",
        "brand_latin": "ZenBeads",
        "tagline": "108알 공덕 · 걷기 수행 · 마음챙김",
        "hero_sub": "마음이 복잡할 땐, 한 번 두드려 보세요. 오프라인으로 쓰는 나만의 염주와 목탁이에요.",
        "cta_small": "다운로드",
        "cta_big": "App Store",
        "lang_name": "한국어",
        "skip": "본문으로 건너뛰기",
        "lang_label": "언어",
        "title": "ZenBeads 젠비즈 — 염주 · 목탁 · 오늘의 수행",
        "meta_desc": "ZenBeads — 오프라인으로 쓰는 나만의 염주와 목탁. 한 번 두드리면 공덕 하나, 오늘 걸은 걸음이 오늘의 수행이 돼요. 소원으로 세로 배경화면을 만들어요. 계정도 광고도 없고 완전 오프라인이에요.",
        "og_title": "ZenBeads · 두드리면 마음이 조용해져요",
        "og_desc": "목탁 · 염주 108알 · 오늘의 수행. 계정도 광고도 없고 완전 오프라인이에요.",
        "features_title": "한 알에 한 호흡",
        "features_sub": "마음을 머무르게 하는 다섯 가지",
        "features": [
            ("두드려요", "목탁", "한 번 가볍게 두드리면 공덕 +1. 목탁 소리와 오늘의 말씀이 흩어진 시간을 고른 호흡으로 바꿔 줘요.", "01_knock"),
            ("걸어요", "오늘의 수행", "Apple 건강 앱에서 걸음 수와 계단 오르기만 읽어 와서, 오늘의 수행으로 자동 환산해 줘요. 목표를 채우면 복주머니를 드려요. 권한을 주지 않아도 슬라이더로 직접 걸음 수를 대신할 수 있어요.", "02_steps"),
            ("꾸며요", "불상", "모아 둔 행운으로 작은 불상을 꾸며 보세요. 머리장식과 가사, 작은 장신구까지 자유롭게 입힐 수 있어요.", "03_wardrobe"),
            ("적어요", "소원", "소원을 한 줄 적으면 조용히 위로 떠올라요. 떠오른 생각을 알아차리고, 알아차리면 흩어져요.", "04_wish"),
            ("만들어요", "배경화면", "소원이나 좋아하는 문장으로 세로쓰기 배경화면을 만들어요. 글자 크기는 7단계로 자동 맞춰지고, 한 번 터치로 저장돼요. 잠금 화면이 곧 도량이 돼요.", "05_wallpaper"),
        ],
        "privacy_title": "계정 없음 · 광고 없음 · 추적 없음 · 완전 오프라인",
        "privacy_lead": "개인정보 약속",
        "privacy_points": [
            ("계정 없음", "가입 없이 열어 바로 써요"),
            ("광고 없음", "배너도, 전면광고도, 소음도 없어요"),
            ("추적 없음", "아무것도 수집하지 않고, 네트워크 권한도 요청하지 않아요"),
            ("완전 오프라인", "모든 데이터는 이 기기에만 남고, 앱을 지우면 함께 사라져요"),
        ],
        "privacy_health": "건강 데이터는 걸음 수와 계단 오르기만 읽기 전용으로 읽어요. 기록하지도, 업로드하지도 않아요. 권한을 주지 않아도 슬라이더로 대신할 수 있어요.",
        "gallery_title": "꾸며요 · 불상",
        "gallery_sub": "모아 둔 행운으로 작은 불상을 꾸며 보세요. 머리장식과 가사, 작은 장신구까지 자유롭게 입힐 수 있어요.",
        "gallery_alt": "불상 꾸미기 조합",
        "gallery_hint": "옆으로 밀어 더 보기 →",
        "closing_title": "재촉하는 알림도, 순위표도 없어요.",
        "closing_text": "ZenBeads는 당신을 더 좋은 사람으로 만들지 않아요. 이미 충분하다는 걸 알려 줄 뿐이에요.",
        "footer_privacy": "개인정보 처리방침",
        "footer_contact": "연락처",
        "footer_font": "글꼴 안내: 샤뤼원카이(LXGW WenKai), SIL 오픈 폰트 라이선스 1.1",
        "footer_rights": "모든 권리 보유.",
    },
    "th": {
        "brand": "เซ็นบีดส์",
        "brand_latin": "ZenBeads",
        "tagline": "เคาะปลาไม้ สวดมนต์ ทำบุญ",
        "hero_sub": "เมื่อใจไม่สงบ ลองเคาะสักครั้งหนึ่ง ลูกประคำและไม้เคาะในมือถือที่ใช้งานได้แบบออฟไลน์และเป็นส่วนตัว",
        "cta_small": "ดาวน์โหลดบน",
        "cta_big": "App Store",
        "lang_name": "ไทย",
        "skip": "ข้ามไปยังเนื้อหา",
        "lang_label": "ภาษา",
        "title": "ZenBeads เซ็นบีดส์ — ลูกประคำ · ปลาไม้ · ภาวนา",
        "meta_desc": "ZenBeads — ชุดลูกประคำและไม้เคาะในมือถือที่ใช้งานได้แบบออฟไลน์และเป็นส่วนตัว เคาะหนึ่งครั้งเป็นบุญหนึ่งครั้ง ก้าวเดินในแต่ละวันก็เป็นการภาวนาของวันนี้ได้ และทำคำอธิษฐานเป็นภาพพื้นหลังแนวตั้ง ไม่มีบัญชี ไม่มีโฆษณา ไม่มีการติดตาม",
        "og_title": "ZenBeads · เคาะครั้งเดียว ใจก็สงบ",
        "og_desc": "ปลาไม้ · ลูกประคำ 108 เม็ด · การภาวนารายวัน ออฟไลน์เต็มรูปแบบ ไม่มีบัญชี ไม่มีโฆษณา",
        "features_title": "หนึ่งเม็ด หนึ่งลมหายใจ",
        "features_sub": "ที่ห้าแห่งสำหรับวางใจลง",
        "features": [
            ("เคาะ", "ปลาไม้", "แตะเบา ๆ หนึ่งครั้ง บุญ +1 เสียงปลาไม้พร้อมข้อคิดประจำวัน ช่วยให้เวลาที่ว่างเปล่ากลายเป็นช่วงเวลาแห่งสมาธิ", "01_knock"),
            ("เดิน", "การภาวนารายวัน", "อ่านเฉพาะจำนวนก้าวและจำนวนชั้นที่ปีนจากแอปสุขภาพ แล้วแปลงเป็นการภาวนาของวันนี้โดยอัตโนมัติ ครบเป้าหมายรับถุงโชค หากไม่เปิดสิทธิ์ก็ใช้แถบเลื่อนจำลองก้าวได้เลย", "02_steps"),
            ("แต่งตัว", "องค์พระ", "ใช้โชคที่สะสมไว้แต่งตัวองค์พระน้อย มงกุฎ ผ้าจีวร และเครื่องประดับ เลือกผสมกันได้ตามชอบ", "03_wardrobe"),
            ("เขียน", "คำอธิษฐาน", "เขียนคำอธิษฐานแล้วดูมันลอยขึ้นไปอย่างเบาสบาย ความคิดเกิดขึ้นเมื่อใดให้รู้ทัน เมื่อรู้ทันก็ปล่อยวาง", "04_wish"),
            ("สร้าง", "ภาพพื้นหลัง", "เปลี่ยนคำอธิษฐานหรือประโยคที่ชอบให้เป็นภาพพื้นหลังแนวตั้งสไตล์จารึกบนผนังวัด ปรับขนาดตัวอักษรอัตโนมัติ 7 ระดับ บันทึกได้ในครั้งเดียว หน้าจอล็อกคือสถานที่ปฏิบัติธรรม", "05_wallpaper"),
        ],
        "privacy_title": "ไม่มีบัญชี · ไม่มีโฆษณา · ไม่มีการติดตาม · ออฟไลน์เต็มรูปแบบ",
        "privacy_lead": "ข้อผูกพันด้านความเป็นส่วนตัว",
        "privacy_points": [
            ("ไม่มีบัญชี", "เปิดมาใช้ได้ทันที ไม่ต้องสมัคร"),
            ("ไม่มีโฆษณา", "ไม่มีแบนเนอร์ ไม่มีโฆษณาเต็มจอ ไม่มีเสียงรบกวน"),
            ("ไม่มีการติดตาม", "ไม่เก็บข้อมูลใด ๆ และไม่ขอสิทธิ์เครือข่ายแม้แต่ครั้งเดียว"),
            ("ออฟไลน์เต็มรูปแบบ", "ข้อมูลทั้งหมดอยู่บนอุปกรณ์ของคุณเท่านั้น ลบแอปแล้วข้อมูลจะหายไปด้วย"),
        ],
        "privacy_health": "ข้อมูลสุขภาพอ่านเพียงจำนวนก้าวและจำนวนชั้นที่ปีน ไม่บันทึก ไม่อัปโหลด หากไม่เปิดสิทธิ์ก็ใช้แถบเลื่อนจำลองก้าวได้เลย",
        "gallery_title": "แต่งตัว · องค์พระ",
        "gallery_sub": "ใช้โชคที่สะสมไว้แต่งตัวองค์พระน้อย มงกุฎ ผ้าจีวร และเครื่องประดับ เลือกผสมกันได้ตามชอบ",
        "gallery_alt": "ชุดแต่งตัวองค์พระ",
        "gallery_hint": "ปัดไปด้านข้างเพื่อดูเพิ่ม →",
        "closing_title": "ไม่มีการแจ้งเตือนเร่งเร้า ไม่มีตารางอันดับ",
        "closing_text": "ZenBeads ไม่ได้ทำให้คุณดีขึ้น เพียงแต่เตือนให้รู้ว่า คุณดีอยู่แล้ว",
        "footer_privacy": "นโยบายความเป็นส่วนตัว",
        "footer_contact": "ติดต่อเรา",
        "footer_font": "กิตติกรรมประกาศแบบอักษร: LXGW WenKai ภายใต้ SIL Open Font License 1.1",
        "footer_rights": "สงวนลิขสิทธิ์",
    },
}

GALLERY = [
    "WC_00c4de67", "WC_172470d5", "WC_2c73d54a", "WC_4398dc10",
    "WC_6275d5df", "WC_772dae78", "WC_98e4f56a", "WC_b40843ec",
    "WC_c707de88", "WC_dde1a5f0", "WC_ff041101",
]

# Apple logo (white, for the black badge) — standard SF-Symbols style silhouette.
APPLE_LOGO = (
    '<svg class="btn-apple" viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false">'
    '<path fill="#fff" d="M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.53 4.08zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z"/>'
    "</svg>"
)

# Decorative prayer-bead ring for the hero (108 dots arranged in a circle,
# one accent bead + tassel) — pure inline SVG, no external asset.
def hero_beads() -> str:
    import math
    cx, cy, r = 100, 100, 74
    n = 36  # visible beads in the decorative ring
    dots = []
    for i in range(n):
        a = 2 * math.pi * i / n - math.pi / 2
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        accent = ' class="accent"' if i == 0 else ""
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.4"{accent}/>')
    return (
        '<svg class="hero-beads" viewBox="0 0 200 210" aria-hidden="true" focusable="false">'
        '<g fill="#c9b18a">' + "".join(dots) + "</g>"
        '<circle cx="100" cy="100" r="30" fill="none" stroke="#8a6f4d" stroke-width="7" stroke-linecap="round" opacity="0.55"/>'
        '<path d="M100 174 q3 14 0 26" stroke="#8a6f4d" stroke-width="3" fill="none" opacity="0.5"/>'
        "</svg>"
    )


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_page(lang: str) -> str:
    c = COPY[lang]
    page, hreflang, shots_dir, privacy_page, og_img = META[lang]
    # Root page canonicalizes to the bare domain; others to their file path.
    canonical = f"{CANON_BASE}/" if page == "index.html" else f"{CANON_BASE}/{page}"
    privacy_url = f"{PRIVACY_BASE}/{privacy_page}"

    def page_url(l: str) -> str:
        p = META[l][0]
        return f"{CANON_BASE}/" if p == "index.html" else f"{CANON_BASE}/{p}"

    alts = "\n    ".join(
        f'<link rel="alternate" hreflang="{META[l][1]}" href="{page_url(l)}">' for l in LANGS
    )
    xdefault = f'<link rel="alternate" hreflang="x-default" href="{CANON_BASE}/en.html">'

    switches = "\n          ".join(
        f'<a lang="{META[l][1]}" hreflang="{META[l][1]}" href="{META[l][0]}"'
        + (' aria-current="page" class="cur"' if l == lang else "")
        + f'>{COPY[l]["lang_name"]}</a>'
        for l in LANGS
    )

    cards = "\n".join(
        f'''        <article class="feature">
          <div class="feature-media">
            <img src="assets/img/{shots_dir}/{shot}.jpg"
                 srcset="assets/img/{shots_dir}/{shot}@2x.jpg 2x"
                 width="440" height="954" loading="lazy" decoding="async"
                 alt="{c["brand"]} · {name}">
          </div>
          <div class="feature-body">
            <p class="feature-kicker"><span class="kicker-verb">{act}</span></p>
            <h3 class="feature-name">{name}</h3>
            <p class="feature-desc">{desc}</p>
          </div>
        </article>'''
        for act, name, desc, shot in c["features"]
    )

    pp = "\n          ".join(
        f"<li><strong>{t}</strong><span>{d}</span></li>" for t, d in c["privacy_points"]
    )

    gal = "\n          ".join(
        f'<figure class="gal-item" role="listitem"><img src="assets/img/gallery/{g}.webp" '
        f'loading="lazy" decoding="async" width="512" height="640" alt="{c["gallery_alt"]}"></figure>'
        for g in GALLERY
    )

    brand_display = c["brand"] + (
        f' <span class="brand-latin">{c["brand_latin"]}</span>' if c["brand_latin"] else ""
    )
    badge = (
        f'{APPLE_LOGO}<span class="btn-text"><small>{c["cta_small"]}</small>'
        f'<b>{c["cta_big"]}</b></span>'
    )

    return f"""<!DOCTYPE html>
<html lang="{hreflang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(c["title"])}</title>
  <meta name="description" content="{esc(c["meta_desc"])}">
  <link rel="canonical" href="{canonical}">
    {alts}
    {xdefault}
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="ZenBeads">
  <meta property="og:title" content="{esc(c["og_title"])}">
  <meta property="og:description" content="{esc(c["og_desc"])}">
  <meta property="og:image" content="{CANON_BASE}/{og_img}">
  <meta property="og:image:width" content="1024">
  <meta property="og:image:height" content="1024">
  <meta property="og:url" content="{canonical}">
  <meta property="og:locale" content="{OG_LOCALE[lang]}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#faf9f7">
  <link rel="icon" type="image/png" href="assets/img/icon.png">
  <link rel="apple-touch-icon" href="assets/img/icon.png">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <a class="skip" href="#main">{c["skip"]}</a>
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="brand" href="{page}">{brand_display}</a>
      <nav class="lang-switch" aria-label="{c["lang_label"]}">
          {switches}
      </nav>
    </div>
  </header>

  <main id="main">
    <section class="hero">
      <div class="wrap hero-inner">
        {hero_beads()}
        <h1 class="hero-title">{c["brand"]}</h1>
        <p class="hero-tagline">{c["tagline"]}</p>
        <p class="hero-sub">{c["hero_sub"]}</p>
        <div class="hero-cta">
          <a class="appstore-btn" href="{APP_STORE}" rel="noopener">
            {badge}
          </a>
        </div>
      </div>
    </section>

    <section class="features" id="features">
      <div class="wrap">
        <h2 class="section-title">{c["features_title"]}</h2>
        <p class="section-sub">{c["features_sub"]}</p>
        <div class="feature-grid">
{cards}
        </div>
      </div>
    </section>

    <section class="privacy-band" id="privacy">
      <div class="wrap">
        <h2 class="privacy-title">{c["privacy_title"]}</h2>
        <p class="privacy-lead">{c["privacy_lead"]}</p>
        <ul class="privacy-points">
          {pp}
        </ul>
        <p class="privacy-health">{c["privacy_health"]}</p>
      </div>
    </section>

    <section class="gallery" id="gallery">
      <div class="wrap">
        <h2 class="section-title">{c["gallery_title"]}</h2>
        <p class="section-sub">{c["gallery_sub"]}</p>
      </div>
      <div class="gal-strip" role="list" aria-label="{c["gallery_title"]}">
          {gal}
      </div>
      <p class="gal-hint wrap">{c["gallery_hint"]}</p>
    </section>

    <section class="closing">
      <div class="wrap">
        <h2 class="closing-title">{c["closing_title"]}</h2>
        <p class="closing-text">{c["closing_text"]}</p>
        <a class="appstore-btn" href="{APP_STORE}" rel="noopener">
          {badge}
        </a>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="wrap footer-inner">
      <p class="footer-brand">© 2026 ZenBeads（{c["brand"]}）. {c["footer_rights"]}</p>
      <nav class="footer-links">
        <a href="{privacy_url}" rel="noopener">{c["footer_privacy"]}</a>
        <a href="mailto:{CONTACT}">{c["footer_contact"]}</a>
      </nav>
      <p class="footer-font">{c["footer_font"]} · <a href="fonts/OFL-LXGWWenKai.txt">OFL 1.1</a></p>
    </div>
  </footer>
</body>
</html>
"""


def main() -> None:
    all_chars = set()
    for lang in LANGS:
        html = build_page(lang)
        path = os.path.join(SITE, META[lang][0])
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", path, len(html), "bytes")
        text = re.sub(r"<[^>]+>", "", html)
        all_chars |= set(text)
    with open(os.path.join(SITE, "_fontchars.txt"), "w", encoding="utf-8") as f:
        f.write("".join(sorted(all_chars)))
    print("charset:", len(all_chars))


if __name__ == "__main__":
    main()
