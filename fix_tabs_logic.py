import os

app_path = os.path.join('src', 'App.jsx')

app_code = """import React, { useState } from 'react';
import CampaignManager from './components/CampaignManager/CampaignManager';

export default function App() {
  const [activeTab, setActiveTab] = useState('surahs');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedReciter, setSelectedReciter] = useState('parhizgar_fast');
  const [speed, setSpeed] = useState('1');
  const [lang, setLang] = useState('fa');
  const [isCampaignOpen, setIsCampaignOpen] = useState(false);
  const [theme, setTheme] = useState('dark');

  // داده‌های نمونه برای سوره‌ها، اجزاء و صفحات
  const surahs = [
    { id: 1, name: 'سُورَةُ الْفَاتِحَةِ', english: 'Al-Faatiha', verses: 7 },
    { id: 2, name: 'سُورَةُ البَقَرَةِ', english: 'Al-Baqara', verses: 286 },
    { id: 3, name: 'سُورَةُ آلِ عِمْرَانَ', english: 'Aal-i-Imraan', verses: 200 },
    { id: 4, name: 'سُورَةُ النِّسَاءِ', english: 'An-Nisaa', verses: 176 },
    { id: 5, name: 'سُورَةُ الْمَائِدَةِ', english: 'Al-Maaida', verses: 120 },
    { id: 6, name: 'سُورَةُ الأَنْعَامِ', english: "Al-An'aam", verses: 165 },
    { id: 7, name: 'سُورَةُ الأَعْرَافِ', english: "Al-A'raaf", verses: 206 },
    { id: 8, name: 'سُورَةُ الأَنْفَالِ', english: 'Al-Anfaal', verses: 75 },
    { id: 9, name: 'سُورَةُ التَّوْبَةِ', english: 'At-Tawba', verses: 129 },
    { id: 10, name: 'سُورَةُ يُونُسَ', english: 'Yunus', verses: 109 },
    { id: 11, name: 'سُورَةُ هُودٍ', english: 'Hud', verses: 123 },
    { id: 12, name: 'سُورَةُ يُوسُفَ', english: 'Yusuf', verses: 111 },
    { id: 13, name: 'سُورَةُ الرَّعْدِ', english: "Ar-Ra'd", verses: 43 },
    { id: 14, name: 'سُورَةُ إِبْرَاهِيمَ', english: 'Ibrahim', verses: 52 },
    { id: 15, name: 'سُورَةُ الْحِجْرِ', english: 'Al-Hijr', verses: 99 },
    { id: 16, name: 'سُورَةُ النَّحْلِ', english: 'An-Nahl', verses: 128 }
  ];

  const juzList = Array.from({ length: 30 }, (_, i) => ({ id: i + 1, name: `جزء ${i + 1}` }));
  const pagesList = Array.from({ length: 604 }, (_, i) => ({ id: i + 1, name: `صفحه ${i + 1}` }));

  const filteredSurahs = surahs.filter(s => 
    s.name.includes(searchQuery) || s.english.toLowerCase().includes(searchQuery.toLowerCase()) || s.id.toString() === searchQuery
  );

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: theme === 'dark' ? '#0f172a' : '#f8fafc',
      color: theme === 'dark' ? '#f8fafc' : '#0f172a',
      direction: 'rtl',
      fontFamily: 'system-ui, -apple-system, sans-serif'
    }}>
      {/* هدر */}
      <header style={{ backgroundColor: '#0f172a', borderBottom: '1px solid #1e293b', padding: '12px 16px' }}>
        <div style={{ maxWidth: '1100px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ fontSize: '22px' }}>📖</span>
              <h1 style={{ margin: 0, fontSize: '20px', fontWeight: 'bold', color: '#38bdf8' }}>معراج</h1>
              <span style={{ fontSize: '10px', backgroundColor: '#334155', color: '#94a3b8', padding: '2px 6px', borderRadius: '4px' }}>v1.0.0</span>
            </div>
            <button style={{ backgroundColor: '#0284c7', color: '#ffffff', border: 'none', padding: '6px 14px', borderRadius: '6px', fontSize: '12px', fontWeight: 'bold', cursor: 'pointer' }}>
              🔑 ورود / ثبت‌نام
            </button>
          </div>

          <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'space-between', gap: '8px', backgroundColor: '#1e293b', padding: '8px 12px', borderRadius: '8px', border: '1px solid #334155' }}>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', alignItems: 'center' }}>
              <button onClick={() => setIsCampaignOpen(true)} style={{ backgroundColor: '#10b981', color: '#ffffff', border: 'none', padding: '6px 12px', borderRadius: '6px', fontSize: '11px', fontWeight: 'bold', cursor: 'pointer' }}>
                🌐 پویش‌های قرآنی
              </button>
              <button style={{ backgroundColor: '#0284c7', color: '#ffffff', border: 'none', padding: '6px 12px', borderRadius: '6px', fontSize: '11px', fontWeight: 'bold', cursor: 'pointer' }}>
                📱 نصب اپلیکیشن
              </button>
              <button onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')} style={{ backgroundColor: '#334155', color: '#f8fafc', border: '1px solid #475569', padding: '6px 10px', borderRadius: '6px', fontSize: '11px', cursor: 'pointer' }}>
                🎨 رنگ و ظاهر
              </button>
              <select value={lang} onChange={(e) => setLang(e.target.value)} style={{ backgroundColor: '#0f172a', color: '#e2e8f0', border: '1px solid #334155', borderRadius: '6px', padding: '6px 8px', fontSize: '11px' }}>
                <option value="fa">🌐 فارسی</option>
                <option value="ar">🌍 العربية</option>
                <option value="en">🌎 English</option>
              </select>
            </div>

            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', alignItems: 'center', flex: 1, justifyContent: 'flex-end', minWidth: '280px' }}>
              <select value={selectedReciter} onChange={(e) => setSelectedReciter(e.target.value)} style={{ backgroundColor: '#0f172a', color: '#e2e8f0', border: '1px solid #334155', borderRadius: '6px', padding: '6px 8px', fontSize: '11px', flex: 2, minWidth: '180px' }}>
                <option value="parhizgar_fast">⚡ استاد شهریار پرهیزگار (تندخوانی)</option>
                <option value="parhizgar">استاد شهریار پرهیزگار (ترتیل)</option>
                <option value="abdulbasit_tartil">استاد عبدالباسط عبدالصمد (ترتیل)</option>
                <option value="minshawi">استاد محمدصدیق منشاوی</option>
              </select>

              <select value={speed} onChange={(e) => setSpeed(e.target.value)} style={{ backgroundColor: '#0f172a', color: '#e2e8f0', border: '1px solid #334155', borderRadius: '6px', padding: '6px 8px', fontSize: '11px', flex: 1, minWidth: '90px' }}>
                <option value="1">سرعت: 1x (عادی)</option>
                <option value="0.75">سرعت: 0.75x</option>
                <option value="1.25">سرعت: 1.25x</option>
                <option value="1.5">سرعت: 1.5x</option>
              </select>
            </div>
          </div>
        </div>
      </header>

      {/* بدنه اصلی */}
      <main style={{ maxWidth: '1100px', margin: '20px auto', padding: '0 16px' }}>
        
        {/* تب‌ها */}
        <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
          <button onClick={() => setActiveTab('surahs')} style={{ flex: 1, padding: '10px', borderRadius: '8px', border: 'none', backgroundColor: activeTab === 'surahs' ? '#0284c7' : '#1e293b', color: '#ffffff', fontWeight: 'bold', fontSize: '13px', cursor: 'pointer' }}>
            📖 سوره‌ها (۱۱۴)
          </button>
          <button onClick={() => setActiveTab('juz')} style={{ flex: 1, padding: '10px', borderRadius: '8px', border: 'none', backgroundColor: activeTab === 'juz' ? '#0284c7' : '#1e293b', color: '#ffffff', fontWeight: 'bold', fontSize: '13px', cursor: 'pointer' }}>
            ⚙️ اجزاء (۳۰)
          </button>
          <button onClick={() => setActiveTab('pages')} style={{ flex: 1, padding: '10px', borderRadius: '8px', border: 'none', backgroundColor: activeTab === 'pages' ? '#0284c7' : '#1e293b', color: '#ffffff', fontWeight: 'bold', fontSize: '13px', cursor: 'pointer' }}>
            📄 صفحات (۶۰۴)
          </button>
        </div>

        {/* کادر جستجو */}
        <div style={{ marginBottom: '20px' }}>
          <input 
            type="text" 
            placeholder={activeTab === 'surahs' ? 'جستجوی سوره (نام یا شماره)...' : activeTab === 'juz' ? 'جستجوی جزء...' : 'جستجوی شماره صفحه...'}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{ width: '100%', padding: '12px 16px', borderRadius: '8px', backgroundColor: '#1e293b', border: '1px solid #334155', color: '#ffffff', fontSize: '13px', boxSizing: 'border-box' }}
          />
        </div>

        {/* نمایش متناسب با تب انتخاب‌شده */}
        {activeTab === 'surahs' && (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '12px' }}>
            {filteredSurahs.map(surah => (
              <div key={surah.id} style={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '14px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', cursor: 'pointer' }}>
                <div>
                  <div style={{ fontSize: '15px', fontWeight: 'bold', color: '#f8fafc', marginBottom: '4px' }}>{surah.name}</div>
                  <div style={{ fontSize: '11px', color: '#94a3b8' }}>{surah.english} • {surah.verses} آیه</div>
                </div>
                <div style={{ width: '28px', height: '28px', borderRadius: '6px', backgroundColor: '#0f172a', color: '#38bdf8', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '12px', fontWeight: 'bold' }}>
                  {surah.id}
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'juz' && (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(140px, 1fr))', gap: '12px' }}>
            {juzList.filter(j => j.name.includes(searchQuery) || j.id.toString() === searchQuery).map(juz => (
              <div key={juz.id} style={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '16px', textAlign: 'center', cursor: 'pointer' }}>
                <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#38bdf8' }}>{juz.name}</div>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'pages' && (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(110px, 1fr))', gap: '10px' }}>
            {pagesList.filter(p => p.name.includes(searchQuery) || p.id.toString() === searchQuery).slice(0, 100).map(page => (
              <div key={page.id} style={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '12px', textAlign: 'center', cursor: 'pointer' }}>
                <div style={{ fontSize: '14px', color: '#f8fafc' }}>{page.name}</div>
              </div>
            ))}
          </div>
        )}
      </main>

      <CampaignManager isOpen={isCampaignOpen} onClose={() => setIsCampaignOpen(false)} />
    </div>
  );
}
"""

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(app_code)

print("  ✓ منطق تب‌های سوره‌ها، اجزاء و صفحات اصلاح شد.")