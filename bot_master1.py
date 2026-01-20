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
# ⚙️ الإعدادات المتقدمة (المليون جلسة)
# ==========================================
MAX_SESSIONS = 1000000  # الهدف: مليون جلسة
TOR_PROXY = "socks5://127.0.0.1:9050"

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
# 🛠️ الوظائف المساعدة (IP، السرعة، البطارية)
# ==========================================
def get_ip():
    try:
        proxies = {'http': TOR_PROXY, 'https': TOR_PROXY}
        return requests.get('https://api.ipify.org', proxies=proxies, timeout=15).text
    except:
        return "Tor Connection Pending..."

def apply_stealth(driver, dev):
    # محاكاة ذكية للبطارية وسرعة الإنترنت والـ GPS
    batt = random.choice([0.45, 0.72, 0.88, 0.95, 1.0])
    speed = random.randint(5, 45) # Mbps محاكاة تذبذب السرعة
    lat, lon = random.uniform(20.0, 50.0), random.uniform(35.0, 55.0)
    
    js = f"""
    Object.defineProperty(navigator, 'webdriver', {{get: () => undefined}});
    Object.defineProperty(navigator, 'platform', {{get: () => '{dev["plat"]}'}});
    if (navigator.getBattery) {{
        navigator.getBattery = () => Promise.resolve({{charging: true, level: {batt}}});
    }}
    Object.defineProperty(navigator, 'connection', {{get: () => ({{effectiveType: '4g', downlink: {speed}, rtt: 50}})}});
    navigator.geolocation.getCurrentPosition = (s) => s({{coords: {{latitude: {lat}, longitude: {lon}}}});
    """
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})

# ==========================================
# 📺 تنفيذ الجلسة المنفردة
# ==========================================
def run_session(session_num):
    # قتل أي عمليات كروم عالقة قبل البدء لضمان متصفح واحد فقط
    os.system("pkill -f chrome 2>/dev/null || true")
    
    dev = random.choice(DEVICES)
    vid = random.choice(VIDEOS_POOL)
    ip = get_ip()
    
    print(f"\n[👑 الجلسة {session_num}/{MAX_SESSIONS}]")
    print(f"🌍 IP: {ip} | 📱 الجهاز: {dev['name']}")
    
    p_dir = tempfile.mkdtemp(prefix="imperial_")
    options = uc.ChromeOptions()
    options.add_argument(f'--user-data-dir={p_dir}')
    options.add_argument(f'--user-agent={dev["ua"]}')
    options.add_argument(f'--proxy-server={TOR_PROXY}')
    options.add_argument(f"--window-size={dev['w']},{dev['h']}")
    options.add_argument('--headless') # يعمل في الخلفية لتوفير الموارد
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = None
    try:
        driver = uc.Chrome(options=options, use_subprocess=True)
        apply_stealth(driver, dev)
        
        # 1. الدخول عبر البحث (زيادة المصداقية)
        driver.get("https://www.youtube.com")
        time.sleep(random.randint(4, 7))
        
        # 2. تشغيل الفيديو مباشرة (أسرع للوصول لمليون)
        driver.get(f"https://www.youtube.com/watch?v={vid['id']}")
        
        # 3. إعدادات الفيديو (سرعة 2x لإنهاء المهمة بسرعة)
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "video")))
        driver.execute_script("document.querySelector('video').playbackRate = 2.0; document.querySelector('video').play();")
        
        # 4. وقت المشاهدة (بين دقيقة ودقيقتين بالسرعة المضاعفة)
        watch_time = random.randint(60, 120)
        print(f"🎬 مشاهدة جارية (سرعة 2x) لـ {watch_time} ثانية...")
        time.sleep(watch_time)
        
        # 5. تفاعل بسيط (لايك عشوائي)
        if random.random() < 0.3:
            try:
                driver.find_element(By.XPATH, "//button[contains(@aria-label, 'like')]").click()
                print("👍 إعجاب")
            except: pass

        return True
    except Exception as e:
        print(f"⚠️ تنبيه: تعثرت الجلسة (سيتم التخطي) - {str(e)[:40]}")
        return False
    finally:
        if driver: driver.quit()
        if os.path.exists(p_dir): shutil.rmtree(p_dir, ignore_errors=True)

# ==========================================
# 🚀 محرك التشغيل اللانهائي
# ==========================================
if __name__ == "__main__":
    for i in range(1, MAX_SESSIONS + 1):
        success = run_session(i)
        
        # استراحة قصيرة جداً (5 ثواني) لضمان عدم توقف السيرفر
        time.sleep(5)
        
        # في حال أردت إيقاف السكربت يدوياً
        if os.path.exists("stop.txt"):
            print("🛑 تم العثور على ملف stop.txt. الإيقاف الآمن...")
            break

    print("🏁 انتهت المهمة الإمبراطورية (مليون جلسة).")
