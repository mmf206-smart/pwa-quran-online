import os
import re

app_jsx_path = os.path.join('src', 'App.jsx')

if not os.path.exists(app_jsx_path):
    print("❌ فایل App.jsx پیدا نشد!")
    exit(1)

with open(app_jsx_path, 'r', encoding='utf-8') as f:
    content = f.read()

# لیست کامل قاریان برجسته
reciters_html = """<select style={{
                backgroundColor: '#0f172a',
                color: '#e2e8f0',
                border: '1px solid #334155',
                borderRadius: '6px',
                padding: '4px 6px',
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
              </select>"""

# جایگزینی select تک‌گزینه‌ای با لیست کامل قاریان
pattern = r'<select[^>]*>\s*<option>استاد شهریار پرهیزگار \(تندخوانی\)</option>\s*</select>'

if re.search(pattern, content):
    content = re.sub(pattern, reciters_html, content)
else:
    content = re.sub(
        r'<option>استاد شهریار پرهیزگار \(تندخوانی\)</option>',
        '''<option value="parhizgar_fast">استاد شهریار پرهیزگار (تندخوانی)</option>
                <option value="parhizgar">استاد شهریار پرهیزگار (ترتیل)</option>
                <option value="abdulbasit_tartil">استاد عبدالباسط عبدالصمد (ترتیل)</option>
                <option value="abdulbasit_mujawwad">استاد عبدالباسط عبدالصمد (تحقیق)</option>
                <option value="minshawi">استاد محمدصدیق منشاوی</option>
                <option value="mustafa_ismail">استاد مصطفی اسماعیل</option>
                <option value="hussary">استاد خلیل الحصری</option>
                <option value="afasy">استاد مشاری راشد العفاسی</option>
                <option value="ghamadi">استاد سعد الغامدی</option>
                <option value="maher">استاد ماهر المعیقلی</option>''',
        content
    )

with open(app_jsx_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ لیست کامل و جامع اسامی قاریان با موفقیت بازگردانده شد!")