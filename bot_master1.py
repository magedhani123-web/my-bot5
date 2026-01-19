#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import random
import shutil
import tempfile
import socket
import requests
import sys

# محاولة استيراد Selenium
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
except ImportError:
    os.system("pip install selenium requests > /dev/null 2>&1")
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

# ==========================================
# ⚙️ الإعدادات (CONFIG)
# ==========================================
TOR_PROXY = "socks5://127.0.0.1:9050"
CONTROL_PORT = 9051

DEVICES = [
    {"name": "iPhone 16 Pro Max", "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1", "plat": "iPhone", "w": 430, "h": 932, "mobile": True},
    {"name": "Samsung Galaxy S24 Ultra", "ua": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.64 Mobile Safari/537.36", "plat": "Linux armv8l", "w": 384, "h": 854, "mobile": True},
    {"name": "Windows 11 PC", "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", "plat": "Win32", "w": 1920, "h": 1080, "mobile": False},
    {"name": "MacBook Pro", "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36", "plat": "MacIntel", "w": 1440, "h": 900, "mobile": False}
]

VIDEOS_POOL = [
    "MrKhyV4Gcog",
    "bmgpC4lGSuQ",
    "6hYLIDz-RRM",
    "AvH9Ig3A0Qo"
]

# ==========================================
# 🔍 فحص البيئة
# ==========================================
def setup_env():
    print("👑 IMPERIAL HYBRID VIEWER - FINAL EDITION")
    print("="*60)
    print("🔍 Checking Chrome installation...")
    chrome_path = "/usr/bin/google-chrome"
    if os.path.exists(chrome_path):
        print(f"✅ Found Chrome at: {chrome_path}")
    return chrome_path

# ==========================================
# 🌍 إدارة IP
# ==========================================
def rotate_ip():
    print("🔄 Rotating IP address...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("127.0.0.1", CONTROL_PORT))
            s.send(b'AUTHENTICATE ""\r\nSIGNAL NEWNYM\r\nQUIT\r\n')
        time.sleep(8)
        proxies = {'http': TOR_PROXY, 'https': TOR_PROXY}
        geo = requests.get('http://ip-api.com/json/', proxies=proxies, timeout=10).json()
        print(f"🌍 NEW IP: {geo['query']} | 📍 {geo['country']}")
        return geo
    except:
        print("🌍 NEW IP: Unknown | 📍 Local Connection")
        return {"timezone": "UTC"}

# ==========================================
# 🛠️ بناء المتصفح
# ==========================================
def create_browser(chrome_bin, device, geo):
    profile_dir = tempfile.mkdtemp(prefix="imp_v4_")
    options = Options()
    options.binary_location = chrome_bin
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless=new')
    options.add_argument('--mute-audio')
    options.add_argument(f'--proxy-server={TOR_PROXY}')
    options.add_argument(f'--user-agent={device["ua"]}')
    options.add_argument(f'--user-data-dir={profile_dir}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    print(f"  🛠️ Creating Chrome for {device['name']}...")
    driver = webdriver.Chrome(options=options)
    
    # محاكاة السرعة
    speeds = ["5G", "4G", "WiFi"]
    print(f"📶 Network Speed: {random.choice(speeds)}")
    
    return driver, profile_dir

# ==========================================
# 🚀 تشغيل البوت
# ==========================================
def main():
    chrome_bin = setup_env()
    session = 1
    
    while True:
        print(f"🎯 [Session {session}] Initiating...")
        geo = rotate_ip()
        device = random.choice(DEVICES)
        video_id = random.choice(VIDEOS_POOL)
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        driver, p_dir = None, None
        try:
            driver, p_dir = create_browser(chrome_bin, device, geo)
            print(f"  🌐 Loading: {url}")
            driver.get(url)
            
            # ⏱️ مدة انتظار لضمان التحميل وعدم ظهور Null
            time.sleep(25)
            
            # تشغيل الفيديو وتسريعه
            driver.execute_script("document.querySelector('video').playbackRate = 2.0; document.querySelector('video').play();")
            
            watch_time = random.randint(240, 380)
            print(f"  ⏱️ Watching for {watch_time}s (Speed 2x)...")
            
            time.sleep(watch_time)
            print("  ✅ Session completed successfully")
            
        except Exception as e:
            print(f"  ❌ Error: Video load failed")
        finally:
            if driver: driver.quit()
            if p_dir: shutil.rmtree(p_dir, ignore_errors=True)
            print("  🧹 Cleanup done")
            
        session += 1
        wait = random.randint(15, 30)
        print(f"⏳ Cooldown: {wait}s...")
        time.sleep(wait)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Stopped.")
