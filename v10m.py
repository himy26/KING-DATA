import requests
import os
import threading
import time
from datetime import datetime

# إعدادات الهوية الملكية لمشروع V10M
GITHUB_USER = "himy26"
GITHUB_TOKEN = "HIDDEN_TOKEN"
KING_REPO_URL = f"https://{GITHUB_USER}:{GITHUB_TOKEN}@github.com/{GITHUB_USER}/KING-DATA.git"

def classify_repo(name, description):
    """خوارزمية الفرز الذكي بناءً على الكلمات المفتاحية"""
    text = (name + " " + (description or "")).lower()
    if "samsung" in text: return "Samsung"
    if "mtk" in text or "mediatek" in text: return "MediaTek"
    if "qualcomm" in text or "snapdragon" in text: return "Qualcomm"
    if "oppo" in text or "realme" in text: return "Oppo-Realme"
    if "xiaomi" in text or "mi" in text: return "Xiaomi"
    return "General_Android"

def run_v10m_classified_radar():
    print(f"\n🔱 تشغيل رادار الفرز الذكي لـ V10M.. الشمعة مضيئة يا ملك 🔱")
    seen_exploits = set()

    while True:
        url = "https://api.github.com/search/repositories?q=frp+bypass+2026&sort=updated"
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        
        try:
            response = requests.get(url, headers=headers).json()
            for repo in response.get('items', [])[:3]:
                repo_url = repo['html_url']
                if repo_url not in seen_exploits:
                    # تنفيذ خوارزمية الفرز
                    category = classify_repo(repo['name'], repo['description'])
                    today = datetime.now().strftime("%Y-%m-%d")
                    folder_path = f"{category}/{today}_{repo['name']}"
                    
                    print(f"🔱 رصد ثغرة [{category}]: {repo['name']}")
                    
                    # إنشاء الهيكل المجلدي في المستودع
                    os.makedirs(folder_path, exist_ok=True)
                    
                    # الاستحواذ والرفع المباشر
                    os.system(f"git clone {repo_url} {folder_path}/source")
                    os.system(f"git add . && git commit -m 'V10M Classified: {category} - {repo['name']}'")
                    os.system(f"git push {KING_REPO_URL} main")
                    
                    seen_exploits.add(repo_url)
        except Exception as e:
            print(f"⚠️ تنبيه تقني: {e}")
        
        time.sleep(3600) # فحص دوري كل ساعة لضمان الحصيلة

# تشغيل المهمة بنظام Threading لضمان السرعة
threading.Thread(target=run_v10m_classified_radar, daemon=True).start()

while True:
    time.sleep(1)

