#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
👑 ULTIMATE IMPERIAL VIEWER - MILLION SESSIONS EDITION
تم الدمج: الأجهزة المحدثة، تزييف الموقع، تبديل السرعات، محاكاة البطارية، والبحث الذكي.
"""

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
# ⚙️ الإعدادات الكبرى
# ==========================================
MAX_SESSIONS = 1000000 
TOR_PROXY = "socks5://127.0.0.1:9050"

# قائمة الأجهزة المتطورة والشاملة
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
# 🛠️ أدوات التحكم في الهوية (IP/تزييف/سرعة)
# ==========================================
def show_current_ip():
    try:
        proxies = {'http': TOR_PROXY, 'https': TOR_PROXY}
        ip = requests.get('https://api.ipify.org', proxies=proxies, timeout=15).text
        print(f"🌍 IP النشط حالياً: {ip}")
        return ip
    except:
        print("⚠️ انتظار اتصال Tor...")
        return None

def apply_advanced_stealth(driver, device):
    """تزييف البطارية، الـ GPS، وسرعة الإنترنت"""
    batt_level = random.choice([0.32, 0.55, 0.78, 0.94, 1.0])
    net_speed = random.choice([5, 12, 25, 50, 100]) # Mbps محاكاة 4G/5G/WiFi
    lat = random.uniform(24.0, 48.0)
    lon = random.uniform(35.0, 58.0)
    
    js = f"""
    // 1. تزييف الأتمتة
    Object.defineProperty(navigator, 'webdriver', {{get: () => undefined}});
    
    // 2. تزييف البطارية
    if (navigator.getBattery) {{
        navigator.getBattery = () => Promise.resolve({{
            charging: true, level: {batt_level}, chargingTime: 0, dischargingTime: Infinity
        }});
    }}
    
    // 3. تزييف سرعة الشبكة التلقائية
    Object.defineProperty(navigator, 'connection', {{
        get: () => ({{ effectiveType: '4g', downlink: {net_speed}, rtt: 50 }})
    }});
    
    // 4. تزييف الـ GPS
    navigator.geolocation.getCurrentPosition = (success) => {{
        success({{ coords: {{ latitude: {lat}, longitude: {lon}, accuracy: 10 }} }});
    }};
    """
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})

# ==========================================
# 📺 محرك الجلسات (المشاهدة والتبديل)
# ==========================================
def run_session(session_num):
    # ضمان عدم تشغيل عدة متصفحات في وقت واحد
    os.system("pkill -f chrome 2>/dev/null || true")
    
    device = random.choice(DEVICES)
    video = random.choice(VIDEOS_POOL)
    
    print(f"\n{'='*50}")
    print(f"🚀 بدء الجلسة الإمبراطورية #{session_num}")
    show_current_ip()
    print(f"📱 الجهاز: {device['name']} | 📺 الفيديو: {video['keywords']}")

    profile_dir = tempfile.mkdtemp(prefix="imperial_")
    options = uc.ChromeOptions()
    options.add_argument(f'--user-data-dir={profile_dir}')
    options.add_argument(f'--user-agent={device["ua"]}')
    options.add_argument(f'--proxy-server={TOR_PROXY}')
    options.add_argument(f"--window-size={device['w']},{device['h']}")
    options.add_argument('--headless') # للعمل المستمر بدون استهلاك موارد الشاشة
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--mute-audio')

    try:
        driver = uc.Chrome(options=options, use_subprocess=True)
        apply_advanced_stealth(driver, device)
        wait = WebDriverWait(driver, 30)

        # 1. سلوك المشاهدة الذكي: البحث بالكلمات المفتاحية
        driver.get("https://www.youtube.com")
        time.sleep(random.randint(4, 7))
        
        try:
            search_box = wait.until(EC.presence_of_element_located((By.NAME, "search_query")))
            for char in video['keywords']:
                search_box.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            search_box.send_keys(Keys.ENTER)
            time.sleep(5)
            
            # النقر على الفيديو المستهدف
            video_element = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[contains(@href, '{video['id']}')]")))
            video_element.click()
        except:
            # رابط مباشر إذا فشل البحث لضمان احتساب الجلسة
            driver.get(f"https://www.youtube.com/watch?v={video['id']}")

        # 2. تشغيل الفيديو وتسريع السرعة عشوائياً
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "video")))
        speed = random.choice([1.25, 1.5, 2.0])
        driver.execute_script(f"document.querySelector('video').playbackRate = {speed};")
        driver.execute_script("document.querySelector('video').play();")
        print(f"⚡ تم تفعيل التسريع: {speed}x")

        # 3. وقت المشاهدة (لضمان احتساب 100%)
        watch_duration = random.randint(110, 200)
        print(f"⏳ مشاهدة جارية لمدة {watch_duration} ثانية...")
        
        # محاكاة تفاعل بشري (Scroll)
        time.sleep(watch_duration // 2)
        driver.execute_script(f"window.scrollBy(0, {random.randint(200, 600)});")
        time.sleep(watch_duration // 2)

        # 4. التفاعل (لايك عشوائي)
        if random.random() < 0.4:
            try:
                driver.find_element(By.XPATH, "//button[contains(@aria-label, 'like')]").click()
                print("👍 تم وضع إعجاب (Like)")
            except: pass

        # 5. مشاهدة فيديو مقترح في النهاية
        try:
            suggestions = driver.find_elements(By.CSS_SELECTOR, "a.ytd-thumbnail")
            if suggestions:
                suggestions[0].click()
                time.sleep(20) 
        except: pass

        print(f"✅ اكتملت الجلسة {session_num} بنجاح.")
        driver.quit()

    except Exception as e:
        print(f"❌ تعثرت الجلسة: {str(e)[:50]}")
    finally:
        # تنظيف المجلدات المؤقتة فوراً لضمان عدم امتلاء القرص
        if os.path.exists(profile_dir):
            shutil.rmtree(profile_dir, ignore_errors=True)

# ==========================================
# 🏁 المشغل الرئيسي (هدف: مليون جلسة)
# ==========================================
if __name__ == "__main__":
    print("👑 جيش المشاهدات الإمبراطوري في وضع الاستعداد...")
    for i in range(1, MAX_SESSIONS + 1):
        run_session(i)
        
        # استراحة بسيطة لتجديد الاتصال والـ IP
        time.sleep(random.randint(5, 10))
        
        # إيقاف يدوي إذا وجد ملف stop.txt
        if os.path.exists("stop.txt"):
            print("🛑 تم إيقاف السكربت بناءً على طلبك.")
            break
