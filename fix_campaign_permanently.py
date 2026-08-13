import os
import re

app_path = os.path.join('src', 'App.jsx')

if not os.path.exists(app_path):
    print("❌ فایل App.jsx پیدا نشد!")
    exit(1)

with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# ۱. اطمینان از ایمپورت CampaignManager
if "import CampaignManager" not in content:
    content = "import CampaignManager from './components/CampaignManager/CampaignManager';\n" + content

# ۲. اطمینان از تعریف State مدیریت مودال
if "isCampaignOpen" not in content:
    content = re.sub(
        r'(export\s+default\s+function\s+App\s*\([^)]*\)\s*\{)',
        r'\1\n  const [isCampaignOpen, setIsCampaignOpen] = useState(false);',
        content
    )

# ۳. متصل کردن رویداد onClick به دکمه پویش‌ها
# اگر دکمه پویش‌ها وجود دارد اما onClick ندارد، آن را اضافه می‌کنیم
if 'setIsCampaignOpen(true)' not in content:
    content = re.sub(
        r'(<button[^>]*?)(>\s*<span>🌐</span>\s*<span>پویش‌ها?</span>)',
        r'\1 onClick={() => setIsCampaignOpen(true)}\2',
        content
    )
    # حالت جایگزین برای ساختار دکمه بدون spans
    content = re.sub(
        r'(<button[^>]*?)(>.*?پویش‌ها?.*?</button>)',
        r'\1 onClick={() => setIsCampaignOpen(true)}\2',
        content
    )

# ۴. اطمینان از وجود کامپوننت CampaignManager در انتهای رندر JSX
if "<CampaignManager" not in content:
    content = re.sub(
        r'(\s*</div\s*>\s*\);?\s*\}\s*$)',
        r'\n      <CampaignManager isOpen={isCampaignOpen} onClose={() => setIsCampaignOpen(false)} />\n\1',
        content
    )

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ دکمه پویش‌ها و مودال مربوطه با حفظ تمامی بخش‌های قبلی مجدداً فعال شد!")