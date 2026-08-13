import os
import re

app_path = os.path.join('src', 'App.jsx')

if not os.path.exists(app_path):
    print("❌ فایل App.jsx پیدا نشد!")
    exit(1)

with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# ۱. اطمینان از وجود useState و ایمپورت CampaignManager
if "useState" not in content:
    content = content.replace("import React", "import React, { useState }")

if "import CampaignManager" not in content:
    content = "import CampaignManager from './components/CampaignManager/CampaignManager';\n" + content

# ۲. اطمینان از وجود state مربوط به پویش‌ها
if "isCampaignOpen" not in content:
    content = re.sub(
        r'(export\s+default\s+function\s+App\s*\([^)]*\)\s*\{)',
        r'\1\n  const [isCampaignOpen, setIsCampaignOpen] = useState(false);',
        content
    )

# ۳. جایگزینی هدر قدیمی با نوار ابزار جدید و استاندارد
toolbar_html = """
      {/* نوار ابزار و هدر اصلی برنامه */}
      <header style={{
        backgroundColor: '#1e293b',
        color: '#ffffff',
        padding: '12px 20px',
        boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
        direction: 'rtl'
      }}>
        <div style={{
          maxWidth: '1200px',
          margin: '0 auto',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '12px'
        }}>
          {/* لوگو و عنوان */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span style={{ fontSize: '24px' }}>📖</span>
            <h1 style={{ margin: 0, fontSize: '18px', fontWeight: 'bold', color: '#38bdf8' }}>
              قرآن آنلاین PWA
            </h1>
          </div>

          {/* نوار ابزار (Toolbar Buttons) */}
          <nav style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            flexWrap: 'wrap'
          }}>
            <button 
              onClick={() => setIsCampaignOpen(true)}
              style={{
                backgroundColor: '#10b981',
                color: '#ffffff',
                border: 'none',
                padding: '8px 14px',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: 'bold',
                fontSize: '13px',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                transition: 'all 0.2s',
                boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
              }}
            >
              <span>🌐</span>
              <span>پویش‌های قرآنی</span>
            </button>

            <button 
              style={{
                backgroundColor: '#0284c7',
                color: '#ffffff',
                border: 'none',
                padding: '8px 14px',
                borderRadius: '8px',
                cursor: 'pointer',
                fontSize: '13px',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px'
              }}
            >
              <span>📱</span>
              <span>نصب اپلیکیشن</span>
            </button>

            <button 
              style={{
                backgroundColor: '#334155',
                color: '#f8fafc',
                border: '1px solid #475569',
                padding: '8px 14px',
                borderRadius: '8px',
                cursor: 'pointer',
                fontSize: '13px',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px'
              }}
            >
              <span>🎨</span>
              <span>رنگ و ظاهر</span>
            </button>

            <button 
              style={{
                backgroundColor: '#2563eb',
                color: '#ffffff',
                border: 'none',
                padding: '8px 14px',
                borderRadius: '8px',
                cursor: 'pointer',
                fontSize: '13px',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px'
              }}
            >
              <span>🔑</span>
              <span>ورود / ثبت‌نام</span>
            </button>
          </nav>
        </div>
      </header>
"""

# جاگذاری نوار ابزار جدید در ابتدای JSX
if "<header" in content:
    content = re.sub(r'<header.*?</header>', toolbar_html.strip(), content, flags=re.DOTALL)
else:
    content = re.sub(r'(return\s*\(\s*<div[^>]*>)', r'\1\n' + toolbar_html, content)

# ۴. اطمینان از وجود کامپوننت مودال در انتهای فایل
if "<CampaignManager" not in content:
    content = re.sub(
        r'(\s*</div\s*>\s*\);?\s*\}\s*$)',
        r'\n      <CampaignManager isOpen={isCampaignOpen} onClose={() => setIsCampaignOpen(false)} />\n\1',
        content
    )

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ نوار ابزار جدید و استاندارد با موفقیت جایگزین شد!")