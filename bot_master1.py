#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import random
import shutil
import socket
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
TOR_CONTROL_PORT = 9051

DEVICES = [
    {"name": "Samsung Galaxy S24 Ultra", "ua": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.64 Mobile Safari/537.36", "plat": "Linux armv8l", "w": 384, "h": 854, "gpu": "Adreno 750"},
    {"name": "iPhone 16 Pro Max", "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1", "plat": "iPhone", "w": 430, "h": 932, "gpu": "Apple GPU"},
    {"name": "Windows 11 PC", "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", "plat": "Win32", "w": 1920, "h": 1080, "gpu": "NVIDIA RTX 4090"}
]

VIDEOS_POOL = [
    {"id": "MrKhyV4Gcog", "keywords": "وش الحلم اللي حققته"},
    {"id": "bmgpC4lGSuQ", "keywords": "أجمل جزيرة في العالم سقطرى"},
    {"id": "6hYLIDz-RRM", "keywords": "هنا اختلفنا وفارقنا علي شان"},
    {"id": "AvH9Ig3A0Qo", "keywords": "Socotra treasure island"}
]

def clean_all():
    os.system("pkill -9 -f chrome 2>/dev/null || true")
    os.system("pkill -9 -f chromedriver 2>/dev/null || true")

def renew_tor():
    try:
        with socket.create_connection(("127.0.0.1", TOR_CONTROL_PORT)) as sig:
            sig.send(b'AUTHENTICATE ""\r\nSIGNAL NEWNYM\r\n')
            time.sleep(3)
    except: pass

def get_geo():
    try:
        proxies = {'http': TOR_PROXY, 'https': TOR_PROXY}
        return requests.get('http://ip-api.com/json/', proxies=proxies, timeout=10).json()
    except: return None

def apply_stealth(driver, device, geo):
    # تزييف البصمة الرقمية والموقع
    lat = geo.get('lat', 0) if geo else 0
    lon = geo.get('lon', 0) if geo else 0
    js = f"""
    Object.defineProperty(navigator, 'webdriver', {{get: () => undefined}});
    Object.defineProperty(navigator, 'deviceMemory', {{get: () => {random.choice([8, 16, 32])}}});
    """
    driver.execute_script(js)
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {"latitude": lat, "longitude": lon, "accuracy": 100})

def run_session(num):
    clean_all()
    renew_tor()
    geo = get_geo()
    device = random.choice(DEVICES)
    video = random.choice(VIDEOS_POOL)
    
    # استخدام مجلد مؤقت فريد لكل جلسة
    profile_path = os.path.join(os.getcwd(), f"temp_profile_{num}")
    
    print(f"\n🚀 الجلسة #{num} | IP: {geo['query'] if geo else 'Error'}")
    print(f"📍 الموقع: {geo.get('country', 'Unknown')} | الجهاز: {device['name']}")

    options = uc.ChromeOptions()
    options.add_argument(f'--user-data-dir={profile_path}')
    options.add_argument(f'--proxy-server={TOR_PROXY}')
    options.add_argument(f'--user-agent={device["ua"]}')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    try:
        # المحاولة باستخدام منفذ تصحيح ثابت لتجنب فشل الربط
        driver = uc.Chrome(options=options, port=random.randint(9300, 9500))
        apply_stealth(driver, device, geo)
        
        print(f"🔗 تم الربط بنجاح. الدخول إلى يوتيوب...")
        driver.get(f"https://www.youtube.com/watch?v={video['id']}")
        
        # انتظار تحميل الفيديو
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "video")))
        driver.execute_script("document.querySelector('video').play();")

        # وقت المشاهدة (بين 2 إلى 4 دقائق)
        watch_seconds = random.randint(120, 240)
        print(f"🎬 بدأ تشغيل: {video['keywords']}")
        
        # عداد تنازلي لوقت المشاهدة يظهر أمامك
        for i in range(watch_seconds, 0, -1):
            print(f"\r⏳ متبقي على نهاية المشاهدة: {i} ثانية   ", end="")
            time.sleep(1)
        
        print(f"\n✅ انتهت المشاهدة بنجاح.")
        
    except Exception as e:
        print(f"\n❌ فشل الربط: تأكد من إغلاق أي متصفح كروم يدوي مفتوح.")
    finally:
        try: driver.quit()
        except: pass
        if os.path.exists(profile_path):
            shutil.rmtree(profile_path, ignore_errors=True)

if __name__ == "__main__":
    for i in range(1, MAX_SESSIONS + 1):
        run_session(i)
        w = random.randint(10, 30)
        print(f"💤 انتظار {w} ثانية...")
        time.sleep(w)
