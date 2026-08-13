import os
import re

app_jsx_path = os.path.join('src', 'App.jsx')
index_css_path = os.path.join('src', 'index.css')
index_html_path = 'index.html'

print("🔍 در حال بازبینی و اصلاح پروژه معراج...")

# ۱. تغییر عنوان برنامه به «معراج» در index.html
if os.path.exists(index_html_path):
    with open(index_html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    html_content = re.sub(r'<title>.*?</title>', '<title>معراج - سامانه قرآنی</title>', html_content)
    with open(index_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("✅ عنوان در index.html به «معراج» تغییر کرد.")

# ۲. اصلاح اسکرول صفحه در index.css
css_scroll_fix = """
/* اصلاح اسکرول روان و رفع قفل شدن صفحه در موبایل و PWA */
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

if os.path.exists(index_css_path):
    with open(index_css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
    if "scroll-behavior: smooth" not in css_content:
        css_content += "\n" + css_scroll_fix
        with open(index_css_path, 'w', encoding='utf-8') as f:
            f.write(css_content)
        print("✅ تنظیمات اسکرول روان به index.css اضافه شد.")

# ۳. اصلاح کامل App.jsx
if os.path.exists(app_jsx_path):
    with open(app_jsx_path, 'r', encoding='utf-8') as f:
        app_content = f.read()

    # ۳-۱. تغییر برند به «معراج»
    app_content = app_content.replace('قرآن آنلاین PWA', 'معراج')
    app_content = app_content.replace('قرآن آنلاین', 'معراج')

    # ۳-۲. اطمینان از ایمپورت کامپوننت پویش‌ها
    if "import CampaignManager" not in app_content:
        app_content = "import CampaignManager from './components/CampaignManager/CampaignManager';\n" + app_content

    # ۳-۳. اطمینان از وجود useState
    if "useState" not in app_content and "import React" in app_content:
        app_content = app_content.replace("import React", "import React, { useState }")

    # ۳-۴. افزودن state مودال پویش‌ها
    if "isCampaignOpen" not in app_content:
        app_content = re.sub(
            r'(export\s+default\s+function\s+App\s*\([^)]*\)\s*\{)',
            r'\1\n  const [isCampaignOpen, setIsCampaignOpen] = useState(false);',
            app_content
        )

    # ۳-۵. اصلاح کلیک دکمه پویش‌ها
    # جایگزینی همه دکمه‌های پویش بدون onClick به دکمه دارای onClick
    app_content = re.sub(
        r'<button([^>]*)(>\s*<span>🌐</span>\s*<span>پویش‌ها?</span>)',
        r'<button onClick={() => setIsCampaignOpen(true)}\1\2',
        app_content
    )

    # ۳-۶. اتصال مودال پویش‌ها در پایان JSX
    if "<CampaignManager" not in app_content:
        app_content = re.sub(
            r'(\s*</div\s*>\s*\);?\s*\}\s*$)',
            r'\n      <CampaignManager isOpen={isCampaignOpen} onClose={() => setIsCampaignOpen(false)} />\n\1',
            app_content
        )

    with open(app_jsx_path, 'w', encoding='utf-8') as f:
        f.write(app_content)

    print("✅ کدهای App.jsx اصلاح و دکمه پویش‌ها کاملاً فعال شد.")

print("🎉 بازبینی با موفقیت تمام شد!")