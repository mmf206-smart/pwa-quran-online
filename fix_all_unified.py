import os

print("🚀 در حال بازسازی یکپارچه و نهایی پروژه معراج...")

# ۱. ساخت یا بروزرسانی کامپوننت پویش‌ها با منطق کامل و تعاملی
campaign_dir = os.path.join('src', 'components', 'CampaignManager')
os.makedirs(campaign_dir, exist_ok=True)
campaign_file = os.path.join(campaign_dir, 'CampaignManager.jsx')

campaign_code = """import React, { useState, useEffect } from 'react';

export default function CampaignManager({ isOpen, onClose }) {
  const [campaigns, setCampaigns] = useState(() => {
    const saved = localStorage.getItem('meraj_campaigns');
    return saved ? JSON.parse(saved) : [
      { id: 1, title: 'ختم سراسری قرآن کریم (دوره ۴۵)', target: 604, current: 412, unit: 'صفحه', icon: '📖' },
      { id: 2, title: 'پویش هدیه سوره یس به روح اموات', target: 1000, current: 680, unit: 'بار', icon: '✨' },
      { id: 3, title: 'پویش صلوات جهت تعجیل در فرج', target: 100000, current: 74200, unit: 'صلوات', icon: '📿' }
    ];
  });

  const [selectedCampaign, setSelectedCampaign] = useState(1);
  const [contribution, setContribution] = useState(1);
  const [successMsg, setSuccessMsg] = useState('');

  useEffect(() => {
    localStorage.setItem('meraj_campaigns', JSON.stringify(campaigns));
  }, [campaigns]);

  if (!isOpen) return null;

  const handleContribute = (e) => {
    e.preventDefault();
    const count = parseInt(contribution) || 1;
    setCampaigns(prev => prev.map(c => {
      if (c.id === selectedCampaign) {
        return { ...c, current: Math.min(c.target, c.current + count) };
      }
      return c;
    }));
    setSuccessMsg('✅ سهم شما با موفقیت ثبت شد. التماس دعا');
    setTimeout(() => setSuccessMsg(''), 3000);
  };

  const activeC = campaigns.find(c => c.id === selectedCampaign);

  return (
    <div style={{
      position: 'fixed',
      top: 0, left: 0, right: 0, bottom: 0,
      backgroundColor: 'rgba(15, 23, 42, 0.85)',
      backdropFilter: 'blur(4px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 9999,
      padding: '16px',
      direction: 'rtl'
    }}>
      <div style={{
        backgroundColor: '#1e293b',
        border: '1px solid #334155',
        borderRadius: '12px',
        width: '100%',
        maxWidth: '520px',
        color: '#f8fafc',
        boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.5)',
        overflow: 'hidden'
      }}>
        {/* هدر مودال */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          padding: '16px 20px',
          borderBottom: '1px solid #334155',
          backgroundColor: '#0f172a'
        }}>
          <h2 style={{ margin: 0, fontSize: '16px', color: '#38bdf8', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span>🌐</span> پویش‌های فعال معراج
          </h2>
          <button onClick={onClose} style={{
            background: 'none',
            border: 'none',
            color: '#94a3b8',
            fontSize: '20px',
            cursor: 'pointer'
          }}>✕</button>
        </div>

        {/* بدنه مودال */}
        <div style={{ padding: '20px' }}>
          {/* انتخاب پویش */}
          <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
            {campaigns.map(c => (
              <button
                key={c.id}
                onClick={() => setSelectedCampaign(c.id)}
                style={{
                  flex: 1,
                  padding: '8px',
                  borderRadius: '6px',
                  border: selectedCampaign === c.id ? '1px solid #38bdf8' : '1px solid #334155',
                  backgroundColor: selectedCampaign === c.id ? '#0284c7' : '#0f172a',
                  color: '#ffffff',
                  fontSize: '11px',
                  cursor: 'pointer',
                  fontWeight: selectedCampaign === c.id ? 'bold' : 'normal'
                }}
              >
                {c.icon} {c.title.split(' ')[0]} {c.title.split(' ')[1]}
              </button>
            ))}
          </div>

          {/* اطلاعات و درصد پیشرفت */}
          {activeC && (
            <div style={{ backgroundColor: '#0f172a', padding: '16px', borderRadius: '8px', marginBottom: '16px' }}>
              <h3 style={{ margin: '0 0 8px 0', fontSize: '14px', color: '#f1f5f9' }}>{activeC.title}</h3>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: '#94a3b8', marginBottom: '6px' }}>
                <span>پیشرفت پویش: {activeC.current.toLocaleString('fa-IR')} از {activeC.target.toLocaleString('fa-IR')} {activeC.unit}</span>
                <span>{Math.round((activeC.current / activeC.target) * 100)}٪</span>
              </div>
              <div style={{ width: '100%', height: '8px', backgroundColor: '#334155', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{
                  width: `${(activeC.current / activeC.target) * 100}%`,
                  height: '100%',
                  backgroundColor: '#10b981',
                  transition: 'width 0.3s ease'
                }} />
              </div>
            </div>
          )}

          {/* فرم ثبت مشارکت */}
          <form onSubmit={handleContribute} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <label style={{ fontSize: '12px', color: '#cbd5e1' }}>تعداد سهم شما جهت مشارکت ({activeC?.unit}):</label>
            <div style={{ display: 'flex', gap: '8px' }}>
              <input
                type="number"
                min="1"
                value={contribution}
                onChange={(e) => setContribution(e.target.value)}
                style={{
                  flex: 1,
                  backgroundColor: '#0f172a',
                  border: '1px solid #334155',
                  borderRadius: '6px',
                  padding: '8px 12px',
                  color: '#ffffff',
                  fontSize: '14px'
                }}
              />
              <button type="submit" style={{
                backgroundColor: '#10b981',
                color: '#ffffff',
                border: 'none',
                borderRadius: '6px',
                padding: '8px 20px',
                fontWeight: 'bold',
                fontSize: '13px',
                cursor: 'pointer'
              }}>
                ثبت سهم
              </button>
            </div>
          </form>

          {successMsg && (
            <div style={{ marginTop: '12px', padding: '8px 12px', backgroundColor: 'rgba(16, 185, 129, 0.2)', border: '1px solid #10b981', borderRadius: '6px', color: '#34d399', fontSize: '12px', textAlign: 'center' }}>
              {successMsg}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
"""

with open(campaign_file, 'w', encoding='utf-8') as f:
    f.write(campaign_code)
print("  ✓ منطق کامل پویش‌ها در CampaignManager.jsx آماده شد.")

# ۲. بازنویسی یکپارچه و کامل App.jsx
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

  // لیست سوره‌های نمونه جهت رندر کامل
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
      {/* هدر اصلی */}
      <header style={{
        backgroundColor: '#0f172a',
        borderBottom: '1px solid #1e293b',
        padding: '12px 16px'
      }}>
        <div style={{ maxWidth: '1100px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          
          {/* سطر اول هدر: عنوان + نسخه + ورود */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ fontSize: '22px' }}>📖</span>
              <h1 style={{ margin: 0, fontSize: '20px', fontWeight: 'bold', color: '#38bdf8' }}>معراج</h1>
              <span style={{
                fontSize: '10px',
                backgroundColor: '#334155',
                color: '#94a3b8',
                padding: '2px 6px',
                borderRadius: '4px',
                border: '1px solid #475569'
              }}>v1.0.0</span>
            </div>

            <button style={{
              backgroundColor: '#0284c7',
              color: '#ffffff',
              border: 'none',
              padding: '6px 14px',
              borderRadius: '6px',
              fontSize: '12px',
              fontWeight: 'bold',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}>
              🔑 ورود / ثبت‌نام
            </button>
          </div>

          {/* سطر دوم: نوار ابزار یکپارچه (تست شده و بدون هم‌پوشانی) */}
          <div style={{
            display: 'flex',
            flexWrap: 'wrap',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '8px',
            backgroundColor: '#1e293b',
            padding: '8px 12px',
            borderRadius: '8px',
            border: '1px solid #334155'
          }}>
            {/* گروه دکمه‌های عملیاتی */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', alignItems: 'center' }}>
              <button 
                onClick={() => setIsCampaignOpen(true)}
                style={{
                  backgroundColor: '#10b981',
                  color: '#ffffff',
                  border: 'none',
                  padding: '6px 12px',
                  borderRadius: '6px',
                  fontSize: '11px',
                  fontWeight: 'bold',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px'
                }}
              >
                <span>🌐</span> پویش‌های قرآنی
              </button>

              <button style={{
                backgroundColor: '#0284c7',
                color: '#ffffff',
                border: 'none',
                padding: '6px 12px',
                borderRadius: '6px',
                fontSize: '11px',
                fontWeight: 'bold',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '4px'
              }}>
                <span>📱</span> نصب اپلیکیشن
              </button>

              <button 
                onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
                style={{
                  backgroundColor: '#334155',
                  color: '#f8fafc',
                  border: '1px solid #475569',
                  padding: '6px 10px',
                  borderRadius: '6px',
                  fontSize: '11px',
                  cursor: 'pointer'
                }}
              >
                🎨 رنگ و ظاهر
              </button>

              <select 
                value={lang} 
                onChange={(e) => setLang(e.target.value)}
                style={{
                  backgroundColor: '#0f172a',
                  color: '#e2e8f0',
                  border: '1px solid #334155',
                  borderRadius: '6px',
                  padding: '6px 8px',
                  fontSize: '11px',
                  cursor: 'pointer'
                }}
              >
                <option value="fa">🌐 فارسی</option>
                <option value="ar">🌍 العربية</option>
                <option value="en">🌎 English</option>
              </select>
            </div>

            {/* گروه انتخاب قاری و سرعت */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', alignItems: 'center', flex: 1, justifyContent: 'flex-end', minWidth: '280px' }}>
              <select 
                value={selectedReciter} 
                onChange={(e) => setSelectedReciter(e.target.value)}
                style={{
                  backgroundColor: '#0f172a',
                  color: '#e2e8f0',
                  border: '1px solid #334155',
                  borderRadius: '6px',
                  padding: '6px 8px',
                  fontSize: '11px',
                  flex: 2,
                  minWidth: '180px',
                  cursor: 'pointer'
                }}
              >
                <option value="parhizgar_fast">⚡ استاد شهریار پرهیزگار (تندخوانی)</option>
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

              <select 
                value={speed} 
                onChange={(e) => setSpeed(e.target.value)}
                style={{
                  backgroundColor: '#0f172a',
                  color: '#e2e8f0',
                  border: '1px solid #334155',
                  borderRadius: '6px',
                  padding: '6px 8px',
                  fontSize: '11px',
                  flex: 1,
                  minWidth: '90px',
                  cursor: 'pointer'
                }}
              >
                <option value="1">سرعت: 1x (عادی)</option>
                <option value="0.75">سرعت: 0.75x</option>
                <option value="1.25">سرعت: 1.25x</option>
                <option value="1.5">سرعت: 1.5x</option>
              </select>
            </div>
          </div>
        </div>
      </header>

      {/* بدنه اصلی برنامه */}
      <main style={{ maxWidth: '1100px', margin: '20px auto', padding: '0 16px' }}>
        
        {/* تب‌های انتخاب نوع نمایش */}
        <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
          <button 
            onClick={() => setActiveTab('surahs')}
            style={{
              flex: 1,
              padding: '10px',
              borderRadius: '8px',
              border: 'none',
              backgroundColor: activeTab === 'surahs' ? '#0284c7' : '#1e293b',
              color: '#ffffff',
              fontWeight: 'bold',
              fontSize: '13px',
              cursor: 'pointer'
            }}
          >
            📖 سوره‌ها (۱۱۴)
          </button>
          <button 
            onClick={() => setActiveTab('juz')}
            style={{
              flex: 1,
              padding: '10px',
              borderRadius: '8px',
              border: 'none',
              backgroundColor: activeTab === 'juz' ? '#0284c7' : '#1e293b',
              color: '#ffffff',
              fontWeight: 'bold',
              fontSize: '13px',
              cursor: 'pointer'
            }}
          >
            ⚙️ اجزاء (۳۰)
          </button>
          <button 
            onClick={() => setActiveTab('pages')}
            style={{
              flex: 1,
              padding: '10px',
              borderRadius: '8px',
              border: 'none',
              backgroundColor: activeTab === 'pages' ? '#0284c7' : '#1e293b',
              color: '#ffffff',
              fontWeight: 'bold',
              fontSize: '13px',
              cursor: 'pointer'
            }}
          >
            📄 صفحات (۶۰۴)
          </button>
        </div>

        {/* کادر جستجو */}
        <div style={{ marginBottom: '20px' }}>
          <input 
            type="text" 
            placeholder="جستجوی سوره (نام یا شماره)..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{
              width: '100%',
              padding: '12px 16px',
              borderRadius: '8px',
              backgroundColor: '#1e293b',
              border: '1px solid #334155',
              color: '#ffffff',
              fontSize: '13px',
              boxSizing: 'border-box'
            }}
          />
        </div>

        {/* شبکه‌بندی سوره‌ها */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))',
          gap: '12px'
        }}>
          {filteredSurahs.map(surah => (
            <div key={surah.id} style={{
              backgroundColor: '#1e293b',
              border: '1px solid #334155',
              borderRadius: '8px',
              padding: '14px',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              cursor: 'pointer',
              transition: 'transform 0.1s ease',
            }}>
              <div>
                <div style={{ fontSize: '15px', fontWeight: 'bold', color: '#f8fafc', marginBottom: '4px' }}>{surah.name}</div>
                <div style={{ fontSize: '11px', color: '#94a3b8' }}>{surah.english} • {surah.verses} آیه</div>
              </div>
              <div style={{
                width: '28px',
                height: '28px',
                borderRadius: '6px',
                backgroundColor: '#0f172a',
                color: '#38bdf8',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '12px',
                fontWeight: 'bold'
              }}>
                {surah.id}
              </div>
            </div>
          ))}
        </div>
      </main>

      {/* مودال تعاملی پویش‌ها */}
      <CampaignManager isOpen={isCampaignOpen} onClose={() => setIsCampaignOpen(false)} />
    </div>
  );
}
"""

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(app_code)

print("  ✓ فایل App.jsx به‌صورت کامل و یکپارچه بازسازی شد.")
print("✨ ساختار کامل نوار ابزار و پویش‌ها با موفقیت تثبیت شد!")