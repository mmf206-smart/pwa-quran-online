import os
import re

app_path = os.path.join('src', 'App.jsx')
css_path = os.path.join('src', 'index.css')
html_path = 'index.html'

print("🚀 در حال اعمال تمامی تغییرات و اصلاحات بر روی پروژه معراج...")

# ۱. بروزرسانی index.html
if os.path.exists(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    html = re.sub(r'<title>.*?</title>', '<title>معراج - سامانه قرآنی</title>', html)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("  ✓ عنوان index.html به «معراج» تغییر کرد.")

# ۲. بروزرسانی index.css برای اسکرول روان
if os.path.exists(css_path):
    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()
    css_addition = """
/* اصلاح اسکرول روان و رفع قفل شدن صفحه */
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
        css += "\n" + css_addition
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css)
    print("  ✓ استایل‌های اسکرول روان به index.css اضافه شدند.")

# ۳. بازنویسی و تثبیت کامل App.jsx
if os.path.exists(app_path):
    with open(app_path, 'r', encoding='utf-8') as f:
        app_code = f.read()

    # ایمپورت‌ها
    if "import CampaignManager" not in app_code:
        app_code = "import CampaignManager from './components/CampaignManager/CampaignManager';\n" + app_code
    if "useState" not in app_code and "import React" in app_code:
        app_code = app_code.replace("import React", "import React, { useState }")

    # تعریف Stateها
    if "isCampaignOpen" not in app_code:
        app_code = re.sub(
            r'(export\s+default\s+function\s+App\s*\([^)]*\)\s*\{)',
            r'\1\n  const [isCampaignOpen, setIsCampaignOpen] = useState(false);',
            app_code
        )
    if "lang" not in app_code:
        app_code = re.sub(
            r'(export\s+default\s+function\s+App\s*\([^)]*\)\s*\{)',
            r'\1\n  const [lang, setLang] = useState("fa");',
            app_code
        )

    # ساختار کامل، شکیل و بدون تداخل هدر و نوار ابزار
    header_jsx = """
      {/* هدر و نوار ابزار معراج v1.0.0 */}
      <header style={{
        backgroundColor: '#0f172a',
        color: '#ffffff',
        padding: '12px 10px',
        borderBottom: '1px solid #1e293b',
        direction: 'rtl'
      }}>
        <div style={{
          maxWidth: '900px',
          margin: '0 auto',
          display: 'flex',
          flexDirection: 'column',
          gap: '10px'
        }}>
          {/* سطر اول: عنوان + شماره نسخه + دکمه‌های پویش و نصب */}
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            paddingBottom: '8px',
            borderBottom: '1px solid rgba(255,255,255,0.08)'
          }}>
            <h1 style={{ margin: 0, fontSize: '18px', fontWeight: 'bold', color: '#38bdf8', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span>📖</span>
              <span>معراج</span>
              <span style={{
                fontSize: '10px',
                fontWeight: 'normal',
                backgroundColor: '#334155',
                color: '#94a3b8',
                padding: '2px 6px',
                borderRadius: '4px',
                border: '1px solid #475569',
                lineHeight: '1'
              }}>v1.0.0</span>
            </h1>

            <div style={{ display: 'flex', gap: '6px' }}>
              <button 
                onClick={() => setIsCampaignOpen(true)}
                style={{
                  backgroundColor: '#10b981',
                  color: '#ffffff',
                  border: 'none',
                  padding: '6px 12px',
                  borderRadius: '6px',
                  fontSize: '12px',
                  fontWeight: 'bold',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px'
                }}
              >
                <span>🌐</span> پویش‌ها
              </button>

              <button 
                style={{
                  backgroundColor: '#0284c7',
                  color: '#ffffff',
                  border: 'none',
                  padding: '6px 12px',
                  borderRadius: '6px',
                  fontSize: '12px',
                  fontWeight: 'bold',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px'
                }}
              >
                <span>📱</span> نصب اپ
              </button>
            </div>
          </div>

          {/* سطر دوم: نوار ابزار تنظیمات (ظاهر، زبان، قاریان، سرعت) */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: '8px',
            backgroundColor: '#1e293b',
            padding: '8px 10px',
            borderRadius: '8px'
          }}>
            <div style={{ display: 'flex', gap: '6px', alignItems: 'center' }}>
              <button style={{
                backgroundColor: '#334155',
                color: '#f8fafc',
                border: '1px solid #475569',
                padding: '5px 10px',
                borderRadius: '6px',
                fontSize: '11px',
                cursor: 'pointer'
              }}>
                🎨 رنگ و ظاهر
              </button>

              <select 
                value={lang || 'fa'} 
                onChange={(e) => setLang && setLang(e.target.value)}
                style={{
                  backgroundColor: '#0f172a',
                  color: '#e2e8f0',
                  border: '1px solid #334155',
                  borderRadius: '6px',
                  padding: '5px 8px',
                  fontSize: '11px',
                  cursor: 'pointer'
                }}
              >
                <option value="fa">🌐 فارسی</option>
                <option value="ar">🌍 العربية</option>
                <option value="en">🌎 English</option>
              </select>
            </div>

            <div style={{ display: 'flex', gap: '6px', flex: '1', minWidth: '240px', justifyContent: 'flex-end' }}>
              <select style={{
                backgroundColor: '#0f172a',
                color: '#e2e8f0',
                border: '1px solid #334155',
                borderRadius: '6px',
                padding: '5px 8px',
                fontSize: '11px',
                flex: '2'
              }}>
                <option value="parhizgar_fast">استاد شهریار پرهیزگار (تندخوانی)</option>
                <option value="parhizgar">استاد شهریار پرهیزگار (ترتیل)</option>
                <option value="abdulbasit_tartil">استاد عبدالباسط عبدالصمد (ترتیل)</option>
                <option value="abdulbasit_mujawwad">استاد عبدالباسط عبدالصمد (تحقیق)</option>
                <option value="minshawi">استاد محمدصدیق منشاوی</option>
                <option value="mustafa_ismail">استاد مصطفی اسماعیل</option>
                <option value="hussary">استاد خلیل الحصری</option>
                <option value="afasy">استاد مشاری راشد العفاسی</option>
                <option value="ghamadi">استاد سعد الغامدی</option>
                <option value="maher">استاد ماهر المعیقلی</option>
              </select>

              <select style={{
                backgroundColor: '#0f172a',
                color: '#e2e8f0',
                border: '1px solid #334155',
                borderRadius: '6px',
                padding: '5px 8px',
                fontSize: '11px',
                flex: '1'
              }}>
                <option>1x (عادی)</option>
                <option>1.25x</option>
                <option>1.5x</option>
              </select>
            </div>
          </div>
        </div>
      </header>
"""

    if "<header" in app_code:
        app_code = re.sub(r'<header.*?</header>', header_jsx.strip(), app_code, flags=re.DOTALL)

    if "<CampaignManager" not in app_code:
        app_code = re.sub(
            r'(\s*</div\s*>\s*\);?\s*\}\s*$)',
            r'\n      <CampaignManager isOpen={isCampaignOpen} onClose={() => setIsCampaignOpen(false)} />\n\1',
            app_code
        )

    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(app_code)

    print("  ✓ هدر و نوار ابزار جدید به همراه تمامی قابلیت‌ها جایگزین شد.")

print("\n✨ تمامی تغییرات با موفقیت اعمال شدند!")