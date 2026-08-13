import os
import re

app_path = os.path.join('src', 'App.jsx')

if not os.path.exists(app_path):
    print("❌ فایل App.jsx پیدا نشد!")
    exit(1)

with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# ۱. اطمینان از وجود state مودال پویش‌ها
if "isCampaignOpen" not in content:
    content = re.sub(
        r'(export\s+default\s+function\s+App\s*\([^)]*\)\s*\{)',
        r'\1\n  const [isCampaignOpen, setIsCampaignOpen] = useState(false);',
        content
    )

# ۲. ساخت کد CSS و JSX نوار ابزار و هدر جدید برای موبایل و دسکتاپ
clean_header_jsx = """
      {/* هدر و نوار ابزار یکپارچه */}
      <header style={{
        backgroundColor: '#0f172a',
        color: '#ffffff',
        padding: '12px 10px',
        borderBottom: '1px solid #1e293b',
        direction: 'rtl'
      }}>
        <div style={{
          maxWidth: '800px',
          margin: '0 auto',
          display: 'flex',
          flexDirection: 'column',
          gap: '10px'
        }}>
          {/* سطر اول: عنوان برنامه و دکمه‌های اصلی */}
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            paddingBottom: '6px',
            borderBottom: '1px solid rgba(255,255,255,0.08)'
          }}>
            <h1 style={{ margin: 0, fontSize: '17px', fontWeight: 'bold', color: '#38bdf8', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span>📖</span> قرآن آنلاین PWA
            </h1>

            <div style={{ display: 'flex', gap: '6px' }}>
              <button 
                onClick={() => setIsCampaignOpen(true)}
                style={{
                  backgroundColor: '#10b981',
                  color: '#ffffff',
                  border: 'none',
                  padding: '5px 10px',
                  borderRadius: '6px',
                  fontSize: '11px',
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
                  padding: '5px 10px',
                  borderRadius: '6px',
                  fontSize: '11px',
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

          {/* سطر دوم: نوار ابزار ابزارها و تنظیمات سریع */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: '8px',
            backgroundColor: '#1e293b',
            padding: '8px',
            borderRadius: '8px'
          }}>
            {/* دکمه‌های تنظیمات ظاهری و حساب */}
            <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
              <button style={{
                backgroundColor: '#334155',
                color: '#f8fafc',
                border: '1px solid #475569',
                padding: '4px 8px',
                borderRadius: '6px',
                fontSize: '11px',
                cursor: 'pointer'
              }}>
                🎨 رنگ و ظاهر
              </button>
            </div>

            {/* بخش انتخاب قاری و سرعت به صورت فشرده کنار هم */}
            <div style={{ display: 'flex', gap: '6px', flex: '1', minWidth: '220px', justifyContent: 'flex-end' }}>
              <select style={{
                backgroundColor: '#0f172a',
                color: '#e2e8f0',
                border: '1px solid #334155',
                borderRadius: '6px',
                padding: '4px 6px',
                fontSize: '11px',
                flex: '2'
              }}>
                <option>استاد شهریار پرهیزگار (تندخوانی)</option>
              </select>

              <select style={{
                backgroundColor: '#0f172a',
                color: '#e2e8f0',
                border: '1px solid #334155',
                borderRadius: '6px',
                padding: '4px 6px',
                fontSize: '11px',
                flex: '1'
              }}>
                <option>1x (عادی)</option>
              </select>
            </div>
          </div>
        </div>
      </header>
"""

# جاگذاری ساختار جدید
if "<header" in content:
    content = re.sub(r'<header.*?</header>', clean_header_jsx.strip(), content, flags=re.DOTALL)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ هدر و نوار ابزار فشرده ویژه موبایل با موفقیت اصلاح شد!")