import os
import re

app_path = os.path.join('src', 'App.jsx')

with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# ۱. افزودن ایمپورت CampaignManager در صورت عدم وجود
if "import CampaignManager" not in content:
    content = "import CampaignManager from './components/CampaignManager/CampaignManager';\n" + content

# ۲. افزودن State مدیریت باز/بسته بودن مودال
if "isCampaignOpen" not in content:
    content = re.sub(
        r'(export\s+default\s+function\s+App\s*\([^)]*\)\s*\{)',
        r'\1\n  const [isCampaignOpen, setIsCampaignOpen] = useState(false);',
        content
    )

# ۳. کد دکمه جدید پویش‌ها
campaign_btn_html = """
        <button 
          onClick={() => setIsCampaignOpen(true)}
          style={{
            backgroundColor: '#10b981',
            color: '#ffffff',
            border: 'none',
            padding: '6px 14px',
            borderRadius: '8px',
            cursor: 'pointer',
            fontWeight: 'bold',
            fontSize: '12px',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '5px',
            boxShadow: '0 2px 4px rgba(0,0,0,0.15)',
            marginLeft: '6px',
            marginRight: '6px'
          }}
        >
          <span>🌐</span>
          <span>پویش‌های قرآنی</span>
        </button>"""

# ۴. تزریق دکمه به هدر اصلی کنار دکمه‌های قبلی
if "setIsCampaignOpen(true)" not in content:
    if 'نصب اپلیکیشن' in content:
        content = content.replace('نصب اپلیکیشن', 'نصب اپلیکیشن' + campaign_btn_html)
    elif 'ورود / ثبت‌نام' in content:
        content = content.replace('ورود / ثبت‌نام', 'ورود / ثبت‌نام' + campaign_btn_html)

# ۵. تزریق کامپوننت مودال CampaignManager در انتهای JSX
if "<CampaignManager" not in content:
    content = re.sub(
        r'(\s*</div\s*>\s*\);?\s*\}\s*$)',
        r'\n      <CampaignManager isOpen={isCampaignOpen} onClose={() => setIsCampaignOpen(false)} />\n\1',
        content
    )

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ دکمه «پویش‌های قرآنی» با موفقیت به هدر صفحه اول اضافه شد!")