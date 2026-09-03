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
  const [theme, setTheme] = useState('dark');

  // وضعیت مودال‌ها
  const [isCampaignOpen, setIsCampaignOpen] = useState(false);
  const [isAuthOpen, setIsAuthOpen] = useState(false);
  const [isInstallOpen, setIsInstallOpen] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null); // سوره یا جزء انتخابی برای مطالعه
  const [mobileNum, setMobileNum] = useState('');

  // دیکشنری ترجمه متون منو
  const t = {
    fa: { title: 'معراج', login: '🔑 ورود / ثبت‌نام', campaigns: '🌐 پویش‌های قرآنی', install: '📱 نصب اپلیکیشن', theme: '🎨 رنگ و ظاهر', surahs: '📖 سوره‌ها (۱۱۴)', juz: '⚙️ اجزاء (۳۰)', pages: '📄 صفحات (۶۰۴)', search: 'جستجو (نام یا شماره)...', close: 'بستن', play: 'پخش صوت', bismillah: 'بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ' },
    ar: { title: 'معراج', login: '🔑 تسجيل الدخول', campaigns: '🌐 الحملات القرآنية', install: '📱 تثبيت التطبيق', theme: '🎨 المظهر', surahs: '📖 السور (١١٤)', juz: '⚙️ الأجزاء (٣٠)', pages: '📄 الصفحات (٦٠٤)', search: 'البحث (بالاسم أو الرقم)...', close: 'إغلاق', play: 'تشغيل الصوت', bismillah: 'بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ' },
    en: { title: 'Meraj', login: '🔑 Login / Register', campaigns: '🌐 Campaigns', install: '📱 Install App', theme: '🎨 Theme', surahs: '📖 Surahs (114)', juz: '⚙️ Juz (30)', pages: '📄 Pages (604)', search: 'Search (name or number)...', close: 'Close', play: 'Play Audio', bismillah: 'In the name of Allah, the Beneficent, the Merciful' }
  }[lang];

  // رنگ‌بندی تم‌ها
  const themeStyles = {
    dark: { bg: '#0f172a', cardBg: '#1e293b', border: '#334155', text: '#f8fafc', accent: '#38bdf8' },
    light: { bg: '#f1f5f9', cardBg: '#ffffff', border: '#cbd5e1', text: '#0f172a', accent: '#0284c7' },
    green: { bg: '#064e3b', cardBg: '#047857', border: '#059669', text: '#ecfdf5', accent: '#34d399' }
  }[theme];

  const surahs = [
    { id: 1, name: 'سُورَةُ الْفَاتِحَةِ', english: 'Al-Faatiha', verses: 7, text: ['الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ', 'الرَّحْمَٰنِ الرَّحِيمِ', 'مَالِكِ يَوْمِ الدِّينِ', 'إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ', 'اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ', 'صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ'] },
    { id: 2, name: 'سُورَةُ البَقَرَةِ', english: 'Al-Baqara', verses: 286, text: ['الم', 'ذَٰلِكَ الْكِتَابُ لَا رَيْبَ ۛ فِيهِ ۛ هُدًى لِّلْمُتَّقِينَ', 'الَّذِينَ يُؤْمِنُونَ بِالْغَيْبِ وَيُقِيمُونَ الصَّلَاةَ وَمِمَّا رَزَقْنَاهُمْ يُنفِقُونَ'] },
    { id: 3, name: 'سُورَةُ آلِ عِمْرَانَ', english: 'Aal-i-Imraan', verses: 200, text: ['الم', 'اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ'] },
    { id: 4, name: 'سُورَةُ النِّسَاءِ', english: 'An-Nisaa', verses: 176, text: ['يَا أَيُّهَا النَّاسُ اتَّقُوا رَبَّكُمُ الَّذِي خَلَقَكُم مِّن نَّفْسٍ وَاحِدَةٍ'] },
    { id: 5, name: 'سُورَةُ الْمَائِدَةِ', english: 'Al-Maaida', verses: 120, text: ['يَا أَيُّهَا الَّذِينَ آمَنُوا أَوْفُوا بِالْعُقُودِ'] },
    { id: 6, name: 'سُورَةُ الأَنْعَامِ', english: "Al-An'aam", verses: 165, text: ['الْحَمْدُ لِلَّهِ الَّذِي خَلَقَ السَّمَاوَاتِ وَالْأَرْضَ'] },
    { id: 7, name: 'سُورَةُ الأَعْرَافِ', english: "Al-A'raaf", verses: 206, text: ['المص', 'كِتَابٌ أُنزِلَ إِلَيْكَ فَلَا يَكُن فِي صَدْرِكَ حَرَجٌ مِّنْهُ'] },
    { id: 8, name: 'سُورَةُ الأَنْفَالِ', english: 'Al-Anfaal', verses: 75, text: ['يَسْأَلُونَكَ عَنِ الْأَنفَالِ ۖ قُلِ الْأَنفَالُ لِلَّهِ وَالرَّسُولِ'] }
  ];

  const juzList = Array.from({ length: 30 }, (_, i) => ({ id: i + 1, name: `جزء ${i + 1}` }));
  const pagesList = Array.from({ length: 604 }, (_, i) => ({ id: i + 1, name: `صفحه ${i + 1}` }));

  const toggleTheme = () => {
    if (theme === 'dark') setTheme('light');
    else if (theme === 'light') setTheme('green');
    else setTheme('dark');
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: themeStyles.bg, color: themeStyles.text, direction: 'rtl', fontFamily: 'system-ui, sans-serif', transition: 'all 0.2s ease' }}>
      
      {/* هدر اصلی */}
      <header style={{ backgroundColor: themeStyles.cardBg, borderBottom: `1px solid ${themeStyles.border}`, padding: '12px 16px' }}>
        <div style={{ maxWidth: '1100px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }} onClick={() => setSelectedItem(null)}>
              <span style={{ fontSize: '22px' }}>📖</span>
              <h1 style={{ margin: 0, fontSize: '20px', fontWeight: 'bold', color: themeStyles.accent }}>{t.title}</h1>
              <span style={{ fontSize: '10px', backgroundColor: themeStyles.border, color: themeStyles.text, padding: '2px 6px', borderRadius: '4px' }}>v1.0.0</span>
            </div>
            
            {/* دکمه ورود / ثبت‌نام */}
            <button onClick={() => setIsAuthOpen(true)} style={{ backgroundColor: '#0284c7', color: '#ffffff', border: 'none', padding: '6px 14px', borderRadius: '6px', fontSize: '12px', fontWeight: 'bold', cursor: 'pointer' }}>
              {t.login}
            </button>
          </div>

          {/* نوار ابزار کامل */}
          <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'space-between', gap: '8px', backgroundColor: themeStyles.bg, padding: '8px 12px', borderRadius: '8px', border: `1px solid ${themeStyles.border}` }}>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', alignItems: 'center' }}>
              <button onClick={() => setIsCampaignOpen(true)} style={{ backgroundColor: '#10b981', color: '#ffffff', border: 'none', padding: '6px 12px', borderRadius: '6px', fontSize: '11px', fontWeight: 'bold', cursor: 'pointer' }}>
                {t.campaigns}
              </button>
              <button onClick={() => setIsInstallOpen(true)} style={{ backgroundColor: '#0284c7', color: '#ffffff', border: 'none', padding: '6px 12px', borderRadius: '6px', fontSize: '11px', fontWeight: 'bold', cursor: 'pointer' }}>
                {t.install}
              </button>
              <button onClick={toggleTheme} style={{ backgroundColor: themeStyles.cardBg, color: themeStyles.text, border: `1px solid ${themeStyles.border}`, padding: '6px 10px', borderRadius: '6px', fontSize: '11px', cursor: 'pointer' }}>
                {t.theme}
              </button>
              <select value={lang} onChange={(e) => setLang(e.target.value)} style={{ backgroundColor: themeStyles.cardBg, color: themeStyles.text, border: `1px solid ${themeStyles.border}`, borderRadius: '6px', padding: '6px 8px', fontSize: '11px', cursor: 'pointer' }}>
                <option value="fa">🌐 فارسی</option>
                <option value="ar">🌍 العربية</option>
                <option value="en">🌎 English</option>
              </select>
            </div>

            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', alignItems: 'center', flex: 1, justifyContent: 'flex-end', minWidth: '280px' }}>
              <select value={selectedReciter} onChange={(e) => setSelectedReciter(e.target.value)} style={{ backgroundColor: themeStyles.cardBg, color: themeStyles.text, border: `1px solid ${themeStyles.border}`, borderRadius: '6px', padding: '6px 8px', fontSize: '11px', flex: 2, minWidth: '180px', cursor: 'pointer' }}>
                <option value="parhizgar_fast">⚡ استاد شهریار پرهیزگار (تندخوانی)</option>
                <option value="parhizgar">استاد شهریار پرهیزگار (ترتیل)</option>
                <option value="abdulbasit">استاد عبدالباسط عبدالصمد</option>
                <option value="minshawi">استاد محمدصدیق منشاوی</option>
              </select>

              <select value={speed} onChange={(e) => setSpeed(e.target.value)} style={{ backgroundColor: themeStyles.cardBg, color: themeStyles.text, border: `1px solid ${themeStyles.border}`, borderRadius: '6px', padding: '6px 8px', fontSize: '11px', flex: 1, minWidth: '90px', cursor: 'pointer' }}>
                <option value="1">سرعت: 1x</option>
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
          <button onClick={() => { setActiveTab('surahs'); setSelectedItem(null); }} style={{ flex: 1, padding: '10px', borderRadius: '8px', border: 'none', backgroundColor: activeTab === 'surahs' ? '#0284c7' : themeStyles.cardBg, color: '#ffffff', fontWeight: 'bold', fontSize: '13px', cursor: 'pointer' }}>
            {t.surahs}
          </button>
          <button onClick={() => { setActiveTab('juz'); setSelectedItem(null); }} style={{ flex: 1, padding: '10px', borderRadius: '8px', border: 'none', backgroundColor: activeTab === 'juz' ? '#0284c7' : themeStyles.cardBg, color: '#ffffff', fontWeight: 'bold', fontSize: '13px', cursor: 'pointer' }}>
            {t.juz}
          </button>
          <button onClick={() => { setActiveTab('pages'); setSelectedItem(null); }} style={{ flex: 1, padding: '10px', borderRadius: '8px', border: 'none', backgroundColor: activeTab === 'pages' ? '#0284c7' : themeStyles.cardBg, color: '#ffffff', fontWeight: 'bold', fontSize: '13px', cursor: 'pointer' }}>
            {t.pages}
          </button>
        </div>

        {/* کادر جستجو */}
        <div style={{ marginBottom: '20px' }}>
          <input 
            type="text" 
            placeholder={t.search}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{ width: '100%', padding: '12px 16px', borderRadius: '8px', backgroundColor: themeStyles.cardBg, border: `1px solid ${themeStyles.border}`, color: themeStyles.text, fontSize: '13px', boxSizing: 'border-box' }}
          />
        </div>

        {/* نمایش متن سوره انتخابی (Quran Reader) */}
        {selectedItem ? (
          <div style={{ backgroundColor: themeStyles.cardBg, border: `1px solid ${themeStyles.border}`, borderRadius: '12px', padding: '24px', textAlign: 'center' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <button onClick={() => setSelectedItem(null)} style={{ backgroundColor: '#0284c7', color: '#fff', border: 'none', padding: '6px 14px', borderRadius: '6px', cursor: 'pointer' }}>➜ بازگشت</button>
              <h2 style={{ margin: 0, color: themeStyles.accent }}>{selectedItem.name}</h2>
              <span style={{ fontSize: '12px', opacity: 0.8 }}>قاری: {selectedReciter} | {speed}x</span>
            </div>
            
            <div style={{ fontSize: '20px', color: '#10b981', margin: '20px 0', fontFamily: 'serif' }}>{t.bismillah}</div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', textAlign: 'right', marginTop: '20px' }}>
              {(selectedItem.text || ['متن آیات این بخش به زودی بارگذاری می‌شود...']).map((verse, idx) => (
                <div key={idx} style={{ padding: '12px', borderBottom: `1px solid ${themeStyles.border}`, fontSize: '18px', lineHeight: '2.2', fontFamily: 'serif' }}>
                  <span style={{ color: themeStyles.accent, marginLeft: '8px' }}>﴿{idx + 1}﴾</span> {verse}
                </div>
              ))}
            </div>
          </div>
        ) : (
          /* شبکه‌بندی آیتم‌ها با امکان کلیک و باز شدن سوره */
          <div>
            {activeTab === 'surahs' && (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '12px' }}>
                {surahs.filter(s => s.name.includes(searchQuery) || s.english.toLowerCase().includes(searchQuery.toLowerCase()) || s.id.toString() === searchQuery).map(surah => (
                  <div key={surah.id} onClick={() => setSelectedItem(surah)} style={{ backgroundColor: themeStyles.cardBg, border: `1px solid ${themeStyles.border}`, borderRadius: '8px', padding: '14px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', cursor: 'pointer', transition: 'transform 0.1s' }}>
                    <div>
                      <div style={{ fontSize: '15px', fontWeight: 'bold', color: themeStyles.text, marginBottom: '4px' }}>{surah.name}</div>
                      <div style={{ fontSize: '11px', opacity: 0.7 }}>{surah.english} • {surah.verses} آیه</div>
                    </div>
                    <div style={{ width: '28px', height: '28px', borderRadius: '6px', backgroundColor: themeStyles.bg, color: themeStyles.accent, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '12px', fontWeight: 'bold' }}>
                      {surah.id}
                    </div>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'juz' && (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(140px, 1fr))', gap: '12px' }}>
                {juzList.filter(j => j.name.includes(searchQuery) || j.id.toString() === searchQuery).map(juz => (
                  <div key={juz.id} onClick={() => setSelectedItem({ name: juz.name, text: [`آیات مربوط به ${juz.name}`] })} style={{ backgroundColor: themeStyles.cardBg, border: `1px solid ${themeStyles.border}`, borderRadius: '8px', padding: '16px', textAlign: 'center', cursor: 'pointer' }}>
                    <div style={{ fontSize: '16px', fontWeight: 'bold', color: themeStyles.accent }}>{juz.name}</div>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'pages' && (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(110px, 1fr))', gap: '10px' }}>
                {pagesList.filter(p => p.name.includes(searchQuery) || p.id.toString() === searchQuery).slice(0, 60).map(page => (
                  <div key={page.id} onClick={() => setSelectedItem({ name: page.name, text: [`آیات مربوط به ${page.name}`] })} style={{ backgroundColor: themeStyles.cardBg, border: `1px solid ${themeStyles.border}`, borderRadius: '8px', padding: '12px', textAlign: 'center', cursor: 'pointer' }}>
                    <div style={{ fontSize: '14px', color: themeStyles.text }}>{page.name}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </main>

      {/* مودال پویش‌ها */}
      <CampaignManager isOpen={isCampaignOpen} onClose={() => setIsCampaignOpen(false)} />

      {/* مودال ورود / ثبت‌نام */}
      {isAuthOpen && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.8)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 9999 }}>
          <div style={{ backgroundColor: themeStyles.cardBg, border: `1px solid ${themeStyles.border}`, padding: '24px', borderRadius: '12px', width: '90%', maxWidth: '360px', textAlign: 'center' }}>
            <h3 style={{ color: themeStyles.accent, marginTop: 0 }}>ورود به سامانه معراج</h3>
            <p style={{ fontSize: '12px', opacity: 0.8 }}>شماره همراه خود را وارد کنید:</p>
            <input type="text" placeholder="09123456789" value={mobileNum} onChange={e => setMobileNum(e.target.value)} style={{ width: '100%', padding: '10px', borderRadius: '6px', border: `1px solid ${themeStyles.border}`, marginBottom: '12px', textAlign: 'center', boxSizing: 'border-box' }} />
            <div style={{ display: 'flex', gap: '8px' }}>
              <button onClick={() => { alert('کد تایید ارسال شد'); setIsAuthOpen(false); }} style={{ flex: 1, backgroundColor: '#10b981', color: '#fff', border: 'none', padding: '8px', borderRadius: '6px', cursor: 'pointer' }}>ارسال کد</button>
              <button onClick={() => setIsAuthOpen(false)} style={{ flex: 1, backgroundColor: '#64748b', color: '#fff', border: 'none', padding: '8px', borderRadius: '6px', cursor: 'pointer' }}>{t.close}</button>
            </div>
          </div>
        </div>
      )}

      {/* مودال نصب اپلیکیشن */}
      {isInstallOpen && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.8)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 9999 }}>
          <div style={{ backgroundColor: themeStyles.cardBg, border: `1px solid ${themeStyles.border}`, padding: '24px', borderRadius: '12px', width: '90%', maxWidth: '400px', textAlign: 'center' }}>
            <h3 style={{ color: themeStyles.accent, marginTop: 0 }}>نصب نرم‌افزار معراج (PWA)</h3>
            <p style={{ fontSize: '13px', lineHeight: '1.6' }}>برای نصب، در مرورگر Chrome دکمه <b>Install</b> یا گزینه <b>Add to Home Screen</b> را بزنید.</p>
            <button onClick={() => setIsInstallOpen(false)} style={{ backgroundColor: '#0284c7', color: '#fff', border: 'none', padding: '8px 20px', borderRadius: '6px', cursor: 'pointer', marginTop: '12px' }}>متوجه شدم</button>
          </div>
        </div>
      )}

    </div>
  );
}
"""

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(app_code)

print("✨ تمامی منوها، مودال‌ها و عملکرد کلیک کارت‌ها با موفقیت فعال شدند!")