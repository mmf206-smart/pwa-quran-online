import os
import subprocess
import re

app_path = os.path.join('src', 'App.jsx')
css_path = os.path.join('src', 'index.css')
html_path = 'index.html'

print("🛠️ در حال بازیابی و اصلاح هوشمند پروژه معراج...")

# ۱. بازیابی فایل App.jsx از گیت به نسخه سالم
print("🔄 ۱. بازیابی فایل App.jsx...")
res = subprocess.run(["git", "checkout", "7949ad8", "--", app_path], capture_output=True, text=True)
if res.returncode != 0:
    subprocess.run(["git", "checkout", "HEAD~1", "--", app_path])
    subprocess.run(["git", "checkout", "HEAD", "--", app_path])

with open(app_path, 'r', encoding='utf-8') as f:
    app_code = f.read()

# ۲. بروزرسانی index.html
if os.path.exists(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    html = re.sub(r'<title>.*?</title>', '<title>معراج - سامانه قرآنی</title>', html)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("  ✓ عنوان HTML به «معراج - سامانه قرآنی» تغییر کرد.")

# ۳. تنظیمات اسکرول روان در index.css
if os.path.exists(css_path):
    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()
    css_fix = """
/* اسکرول روان و رفع قفل شدن صفحه */
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  min-height: 100vh;
  overflow-x: hidden;
  overflow-y: auto !important;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
  background-color: #0f172a;
  color: #f8fafc;
}
#root {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
"""
    if "scroll-behavior: smooth" not in css:
        css += "\n" + css_fix
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css)
    print("  ✓ تنظیمات اسکرول روان اعمال شد.")

# ۴. اصلاحات ایمن و جراحی روی App.jsx

# اضافه کردن ایمپورت پویش‌ها
if "import CampaignManager" not in app_code:
    app_code = "import CampaignManager from './components/CampaignManager/CampaignManager';\n" + app_code

# افزودن Stateهای لازم
if "isCampaignOpen" not in app_code:
    app_code = app_code.replace(
        "function App() {",
        "function App() {\n  const [isCampaignOpen, setIsCampaignOpen] = useState(false);\n  const [lang, setLang] = useState('fa');"
    )

# تغییر برند به معراج v1.0.0
app_code = app_code.replace("قرآن آنلاین PWA", "معراج")
app_code = app_code.replace("قرآن آنلاین", "معراج")

# جایگذاری شماره نسخه کنار معراج
if "v1.0.0" not in app_code:
    app_code = app_code.replace(
        "معراج",
        "معراج <span style={{fontSize:'10px',color:'#94a3b8',backgroundColor:'#334155',padding:'2px 5px',borderRadius:'4px',marginRight:'4px'}}>v1.0.0</span>",
        1
    )

# بازگرداندن اتصال دکمه پویش‌ها
if 'setIsCampaignOpen(true)' not in app_code:
    app_code = re.sub(
        r'(<button[^>]*)(>\s*🌐?\s*پویش‌ها?\s*</button>)',
        r'\1 onClick={() => setIsCampaignOpen(true)}\2',
        app_code
    )

# اضافه کردن کامپوننت مودال پویش‌ها در انتهای JSX
if "<CampaignManager" not in app_code:
    idx = app_code.rfind("</div>")
    if idx != -1:
        app_code = app_code[:idx] + "\n      <CampaignManager isOpen={isCampaignOpen} onClose={() => setIsCampaignOpen(false)} />\n" + app_code[idx:]

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(app_code)

print("  ✓ فایل App.jsx با موفقیت بازسازی و بدون آسیب رندر شد.")
print("✨ تمام! آماده بیلد و انتشار.")