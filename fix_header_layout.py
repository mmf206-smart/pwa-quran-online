import os
import re

app_path = os.path.join('src', 'App.jsx')

with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# پاکسازی هرگونه تزریق اشتباه دکمه پویش‌ها از داخل دکمه‌های دیگر
if '<span>🌐</span>' in content and '<span>پویش‌های قرآنی</span>' in content:
    # حذف دکمه‌های تکراری یا خرابی که داخل تگ‌های دیگر رفته‌اند
    pattern = r'<button[^>]*>\s*<span>🌐</span>\s*<span>پویش‌های قرآنی</span>\s*</button>'
    content = re.sub(pattern, '', content)

# ساخت ساختار تمیز برای دکمه پویش‌های قرآنی
clean_campaign_btn = """
        <button 
          onClick={() => setIsCampaignOpen(true)}
          style={{
            backgroundColor: '#10b981',
            color: '#ffffff',
            border: 'none',
            padding: '6px 12px',
            borderRadius: '8px',
            cursor: 'pointer',
            fontWeight: 'bold',
            fontSize: '12px',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            boxShadow: '0 2px 4px rgba(0,0,0,0.15)',
            whiteSpace: 'nowrap'
          }}
        >
          <span>🌐</span>
          <span>پویش‌های قرآنی</span>
        </button>"""

# جایگذاری دکمه پویش‌ها در کانتینر اصلی هدر بدون هم‌پوشانی
if 'setIsCampaignOpen(true)' not in content or '<span>پویش‌های قرآنی</span>' not in content:
    # جایگذاری پس از دکمه نصب اپلیکیشن
    if '</button>' in content:
        # تزریق دکمه به عنوان یک آیتم مجزا
        content = re.sub(r'(\s*</button>\s*)(?=[^<]*<button|\s*</div>)', r'\1' + clean_campaign_btn + '\n', content, count=1)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ چیدمان دکمه‌های هدر با موفقیت اصلاح شد!")زمس
