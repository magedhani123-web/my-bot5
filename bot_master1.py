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

# تثبيت المكتبات اللازمة تلقائياً
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError:
    print("📦 Installing required libraries...")
    os.system("pip install selenium requests > /dev/null 2>&1")
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

# ==========================================
# ⚙️ الإعدادات والمصفوفات (CONFIG)
# ==========================================
TOR_PROXY = "socks5://127.0.0.1:9050"
CONTROL_PORT = 9051

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

# 👇 مصفوفة الروابط (تم تحديث المعرفات والكلمات المفتاحية) 👇
VIDEOS_POOL = [
    {"id": "MrKhyV4Gcog", "keywords": "وش الحلم اللي حققته"},
    {"id": "bmgpC4lGSuQ", "keywords": "أجمل جزيرة في العالم سقطرى"},
    {"id": "6hYLIDz-RRM", "keywords": "هنا اختلفنا وفارقنا علي شان"},
    {"id": "AvH9Ig3A0Qo", "keywords": "Socotra treasure island"}
]

# ==========================================
# 🌍 نظام الـ IP والمنطقة الزمنية
# ==========================================
def rotate_and_get_geo():
    print("\n" + "🔄" * 20)
    print("🔄 Rotating IP Address...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("127.0.0.1", CONTROL_PORT))
            s.send(b'AUTHENTICATE ""\r\nSIGNAL NEWNYM\r\nQUIT\r\n')
        time.sleep(12)
        proxies = {'http': TOR_PROXY, 'https': TOR_PROXY}
        geo = requests.get('http://ip-api.com/json/', proxies=proxies, timeout=15).json()
        if geo['status'] == 'success':
            print(f"🌍 NEW IP: {geo['query']} | 📍 {geo['country']} - {geo['city']} | 🕒 {geo['timezone']}")
            return geo
    except Exception as e:
        print(f"⚠️ IP Rotation Failed: {e}")
    return {"query": "Unknown", "countryCode": "US", "timezone": "America/New_York"}

# ==========================================
# 📶 محاكاة سرعة الإنترنت التلقائية
# ==========================================
def set_net_speed(driver):
    speeds = [
        {"name": "5G-High", "latency": 15, "download": 150 * 1024 * 1024},
        {"name": "WiFi-Home", "latency": 30, "download": 70 * 1024 * 1024},
        {"name": "4G-LTE", "latency": 50, "download": 20 * 1024 * 1024}
    ]
    s = random.choice(speeds)
    try:
        driver.execute_cdp_cmd("Network.emulateNetworkConditions", {
            "offline": False, "latency": s["latency"],
            "downloadThroughput": s["download"], "uploadThroughput": s["download"] // 2
        })
        print(f"📶 Net Speed Switched to: {s['name']}")
    except: pass

# ==========================================
# 🛠️ بناء المتصفح الإمبراطوري
# ==========================================
def create_browser(device, geo):
    profile_dir = tempfile.mkdtemp(prefix="imp_v4_")
    options = Options()
    
    chrome_bin = "/usr/bin/google-chrome"
    if not os.path.exists(chrome_bin): chrome_bin = "/usr/bin/chromium-browser"
    options.binary_location = chrome_bin

    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless=new')
    options.add_argument('--mute-audio')
    options.add_argument(f'--proxy-server={TOR_PROXY}')
    options.add_argument(f'--user-agent={device["ua"]}')
    options.add_argument(f'--user-data-dir={profile_dir}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.execute_cdp_cmd("Emulation.setTimezoneOverride", {"timezoneId": geo['timezone']})
        driver.execute_script(f"Object.defineProperty(navigator, 'platform', {{get: () => '{device['plat']}'}});")
    except: pass
    
    set_net_speed(driver)
    return driver, profile_dir

# ==========================================
# 🔍 محرك البحث الذكي (لضمان احتساب المشاهدة)
# ==========================================
def smart_search_and_play(driver, video, device):
    try:
        driver.get("https://www.youtube.com")
        time.sleep(random.randint(12, 18))
        
        if device['mobile']:
            try:
                WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Search YouTube']"))).click()
                time.sleep(4)
            except: pass

        search_input = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.NAME, "search_query")))
        for char in video['keywords']:
            search_input.send_keys(char)
            time.sleep(random.uniform(0.1, 0.4))
        search_input.send_keys(Keys.ENTER)
        time.sleep(10)

        links = driver.find_elements(By.TAG_NAME, "a")
        found = False
        for link in links:
            if video['id'] in (link.get_attribute("href") or ""):
                driver.execute_script("arguments[0].scrollIntoView();", link)
                time.sleep(3)
                link.click()
                found = True
                print("🎯 Found & Clicked via Search Results!")
                break
        
        if not found:
            driver.get(f"https://www.youtube.com/watch?v={video['id']}")

        time.sleep(25)
        
        js_enhancer = """
            var v = document.querySelector('video');
            if(v) { 
                v.playbackRate = 2.0; 
                v.play(); 
                v.muted = true;
            }
            setInterval(() => {
                var skipBtn = document.querySelector('.ytp-ad-skip-button, .ytp-skip-ad-button');
                if(skipBtn) skipBtn.click();
                var closeBanner = document.querySelector('.ytp-ad-overlay-close-button');
                if(closeBanner) closeBanner.click();
            }, 8000);
        """
        driver.execute_script(js_enhancer)
        return True
    except Exception as e:
        print(f"❌ Playback Error: {e}")
        return False

# ==========================================
# 🚀 الحلقة اللانهائية (Eternal Loop)
# ==========================================
def start_bot():
    session = 1
    os.system("pkill -f chrome 2>/dev/null || true")
    
    while True:
        geo = rotate_and_get_geo()
        device = random.choice(DEVICES)
        video = random.choice(VIDEOS_POOL)
        
        print(f"\n🚀 Session {session} | Device: {device['name']}")
        print(f"🎬 Watching: {video['keywords']}")
        
        driver, p_dir = None, None
        try:
            driver, p_dir = create_browser(device, geo)
            if smart_search_and_play(driver, video, device):
                watch_time = random.randint(240, 500)
                print(f"⏱️ Viewing for {watch_time}s at 2x Speed...")
                
                start_mark = time.time()
                while time.time() - start_mark < watch_time:
                    time.sleep(random.randint(30, 60))
                    driver.execute_script(f"window.scrollBy(0, {random.randint(150, 500)})")
                
                print(f"✅ Session {session} completed.")
        except Exception as e:
            print(f"❌ Critical error: {e}")
        finally:
            if driver: driver.quit()
            if p_dir: shutil.rmtree(p_dir, ignore_errors=True)
            os.system("sync; echo 1 > /proc/sys/vm/drop_caches 2>/dev/null || true")

        session += 1
        wait = random.randint(25, 45)
        print(f"💤 Cooldown for {wait}s before next IP rotation...")
        time.sleep(wait)

if __name__ == "__main__":
    try:
        start_bot()
    except KeyboardInterrupt:
        print("\n🛑 Stopped. Cleaning up...")
        os.system("pkill -f chrome 2>/dev/null || true")
