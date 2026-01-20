#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import random
import shutil
import tempfile
import sys
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# ==========================================
# ⚙️ الإعدادات الكبرى (مليون جلسة)
# ==========================================
MAX_SESSIONS = 1000000 
TOR_PROXY = "socks5://127.0.0.1:9050"

# قائمة الأجهزة المتطورة التي طلبتها
DEVICES = [
    {"name": "iPhone 16 Pro Max", "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1", "plat": "iPhone", "w": 430, "h": 932, "mobile": True},
    {"name": "iPhone 15 Pro", "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1", "plat": "iPhone", "w": 393, "h": 852, "mobile": True},
    {"name": "Samsung Galaxy S24 Ultra", "ua": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.64 Mobile Safari/537.36", "plat": "Linux armv8l", "w": 384, "h": 854, "mobile": True},
    {"name": "Samsung Galaxy S23 Ultra", "ua": "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36", "plat": "Linux armv8l", "w": 360, "h": 800, "mobile": True},
    {"name": "Google Pixel 9 Pro", "ua": "Mozilla/5.0 (Linux; Android 15; Pixel 9 Pro Build/AD1A.240530.019) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.103 Mobile Safari/537.36", "plat": "Linux aarch64", "w": 412, "h": 915, "mobile": True},
    {"name": "Huawei Mate 60 Pro", "ua": "Mozilla/5.0 (Linux; Android 12; ALN-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36", "plat": "Linux aarch64", "w": 412, "h": 915, "mobile": True},
    {"name": "Xiaomi 14 Ultra", "ua": "Mozilla/5.0 (Linux; Android 14; 24030PN60G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.119 Mobile Safari/537.36", "plat": "Linux armv8l", "w": 393, "h": 873, "mobile": True},
    {"name": "Windows 11 PC", "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", "plat": "Win32", "w": 1920, "h": 1080, "mobile": False},
    {"name": "MacBook Pro (macOS)", "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36", "plat": "MacIntel", "w": 1440, "h": 900, "mobile": False}
]

VIDEOS_POOL = [
    {"id": "MrKhyV4Gcog", "keywords": "وش الحلم اللي حققته"},
    {"id": "bmgpC4lGSuQ", "keywords": "أجمل جزيرة في العالم سقطرى"},
    {"id": "6hYLIDz-RRM", "keywords": "هنا اختلفنا وفارقنا علي شان"},
    {"id": "AvH9Ig3A0Qo", "keywords": "Socotra treasure island"}
]

# ==========================================
# 🛠️ أدوات الجيش البرمجي (التحقق والتزييف)
# ==========================================
def get_current_ip():
    """إظهار الـ IP المستخدم حالياً عبر Tor"""
    try:
        proxies = {'http': TOR_PROXY, 'https': TOR_PROXY}
        return requests.get('https://api.ipify.org', proxies=proxies, timeout=15).text
    except:
        return "جاري انتظار اتصال Tor..."

def apply_full_stealth(driver, dev):
    """حقن التزييف الكامل: بطارية، موقع، سرعة، نظام"""
    batt = random.choice([0.45, 0.65, 0.80, 0.92, 1.0])
    net_speed = random.randint(10, 50) # Mbps
    lat = random.uniform(21.0, 45.0)
    lon = random.uniform(35.0, 55.0)
    
    js = f"""
    // إخفاء الأتمتة
    Object.defineProperty(navigator, 'webdriver', {{get: () => undefined}});
    
    // تزييف النظام والمنصة
    Object.defineProperty(navigator, 'platform', {{get: () => '{dev["plat"]}'}});
    
    // تزييف البطارية
    if (navigator.getBattery) {{
        navigator.getBattery = () => Promise.resolve({{charging: true, level: {batt}}});
    }}
    
    // تزييف سرعة الشبكة (تبديل تلقائي)
    Object.defineProperty(navigator, 'connection', {{
        get: () => ({{effectiveType: '4g', downlink: {net_speed}, rtt: 50}})
    }});
    
    // تزييف الموقع الجغرافي GPS
    navigator.geolocation.getCurrentPosition = (success) => {{
        success({{ coords: {{ latitude: {lat}, longitude: {lon}, accuracy: 10 }} }});
    }};
    """
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})

# ==========================================
# 📺 تنفيذ الجلسة (فتح المتصفح والمشاهدة)
# ==========================================
def run_imperial_session(num):
    # الخطوة 1: تنظيف النظام (متصفح واحد فقط في نفس الوقت)
    os.system("pkill -f chrome 2>/dev/null || true")
    
    device = random.choice(DEVICES)
    video = random.choice(VIDEOS_POOL)
    ip_addr = get_current_ip()
    
    print(f"\n--- 🚀 الجلسة رقم {num} ---")
    print(f"🌍 IP الحالي: {ip_addr}")
    print(f"📱 الجهاز المحاكى: {device['name']}")
    print(f"📺 الفيديو المستهدف: {video['keywords']}")

    # الخطوة 2: إعدادات المتصفح
    temp_dir = tempfile.mkdtemp(prefix="imp_")
    options = uc.ChromeOptions()
    options.add_argument(f'--user-data-dir={temp_dir}')
    options.add_argument(f'--user-agent={device["ua"]}')
    options.add_argument(f'--proxy-server={TOR_PROXY}')
    options.add_argument(f"--window-size={device['w']},{device['h']}")
    options.add_argument('--headless') # للعمل بصمت وتوفير موارد السيرفر
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--mute-audio')

    driver = None
    try:
        driver = uc.Chrome(options=options, use_subprocess=True)
        apply_full_stealth(driver, device)
        
        # الخطوة 3: محاكاة البحث (لضمان احتساب المشاهدة 100%)
        driver.get("https://www.youtube.com")
        time.sleep(random.randint(5, 8))
        
        try:
            # كتابة الكلمات المفتاحية في خانة البحث
            search = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "search_query")))
            for char in video['keywords']:
                search.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            search.send_keys(Keys.ENTER)
            time.sleep(5)
            
            # النقر على الفيديو من النتائج
            target = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f"//a[contains(@href, '{video['id']}')]")))
            target.click()
        except:
            # إذا فشل البحث، نذهب للرابط المباشر لضمان عدم ضياع الجلسة
            driver.get(f"https://www.youtube.com/watch?v={video['id']}")

        # الخطوة 4: التلاعب بالمشغل (السرعة 2x)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "video")))
        driver.execute_script("document.querySelector('video').playbackRate = 2.0; document.querySelector('video').play();")
        
        # الخطوة 5: وقت المشاهدة العشوائي
        duration = random.randint(100, 180)
        print(f"⏱️ مشاهدة جارية بوضع التسريع لمدة {duration} ثانية...")
        
        # عمل سكرول بسيط لمحاكاة البشر
        time.sleep(duration // 2)
        driver.execute_script(f"window.scrollBy(0, {random.randint(200, 500)});")
        time.sleep(duration // 2)

        # الخطوة 6: مشاهدة فيديو مقترح في النهاية (خوارزمية يوتيوب تحب هذا)
        try:
            suggestions = driver.find_elements(By.CSS_SELECTOR, "a.ytd-thumbnail")
            if suggestions:
                suggestions[0].click()
                time.sleep(15)
        except: pass

        print(f"✅ انتهت الجلسة {num} بنجاح.")
        return True

    except Exception as e:
        print(f"❌ حدث خطأ في الجلسة: {str(e)[:50]}")
        return False
    finally:
        if driver: driver.quit()
        if os.path.exists(temp_dir): shutil.rmtree(temp_dir, ignore_errors=True)

# ==========================================
# 🏁 نقطة الانطلاق (التكرار مليون مرة)
# ==========================================
if __name__ == "__main__":
    print("👑 بدأ جيش المشاهدات الإمبراطوري... الهدف: مليون جلسة")
    for i in range(1, MAX_SESSIONS + 1):
        run_imperial_session(i)
        
        # استراحة بسيطة لتجديد الاتصال
        time.sleep(random.randint(3, 7))
        
        # ميزة التوقف الآمن (إذا أنشأت ملف باسم stop.txt سيتوقف السكربت)
        if os.path.exists("stop.txt"):
            print("🛑 تم العثور على طلب إيقاف. وداعاً!")
            break
