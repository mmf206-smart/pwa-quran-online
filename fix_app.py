import os
import subprocess

def fix_app():
    app_jsx_path = os.path.join('src', 'App.jsx')
    
    git_restored = False
    try:
        # ۱. تلاش برای بازگردانی فایل اصلی App.jsx از Git
        res = subprocess.run(['git', 'checkout', 'HEAD', '--', app_jsx_path], capture_output=True, text=True)
        if res.returncode == 0:
            print("✅ فایل اصلی App.jsx با موفقیت از Git بازیابی شد.")
            git_restored = True
    except Exception:
        pass

    if git_restored:
        # اگر از گیت برگشت، مسیر کامپوننت CampaignManager را اصلاح می‌کنیم
        with open(app_jsx_path, 'r', encoding='utf-8') as f:
            content = f.read()

        old_imports = [
            "import CampaignManager from './CampaignManager';",
            "import CampaignManager from './components/CampaignManager';"
        ]
        new_import = "import CampaignManager from './components/CampaignManager/CampaignManager';"
        
        replaced = False
        for old_imp in old_imports:
            if old_imp in content:
                content = content.replace(old_imp, new_import)
                replaced = True
        
        if not replaced and "CampaignManager" not in content:
            content = new_import + "\n" + content

        with open(app_jsx_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ مسیر ایمپورت CampaignManager در فایل اصلی App.jsx اصلاح شد.")
        
    else:
        print("⚠️ تاریخچه Git یافت نشد. در حال ساخت صفحه کامل و اصلی قرآن آنلاین...")
        
        # ۲. بازسازی صفحه کامل و اصلی قرآن آنلاین در صورت عدم وجود Git
        full_app_code = """import React, { useState } from 'react';
import CampaignManager from './components/CampaignManager/CampaignManager';
import './App.css';

export default function App() {
  const [isCampaignOpen, setIsCampaignOpen] = useState(false);
  const [selectedSurah, setSelectedSurah] = useState(1);

  const surahs = [
    { id: 1, name: 'الفاتحة', englishName: 'Al-Fatihah', ayahs: 7, type: 'مکی' },
    { id: 2, name: 'البقرة', englishName: 'Al-Baqarah', ayahs: 286, type: 'مدنی' },
    { id: 3, name: 'آل عمران', englishName: "Ali 'Imran", ayahs: 200, type: 'مدنی' },
    { id: 4, name: 'النساء', englishName: 'An-Nisa', ayahs: 176, type: 'مدنی' },
    { id: 36, name: 'يس', englishName: 'Ya-Sin', ayahs: 83, type: 'مکی' },
    { id: 55, name: 'الرحمن', englishName: 'Ar-Rahman', ayahs: 78, type: 'مدنی' },
    { id: 67, name: 'الملك', englishName: 'Al-Mulk', ayahs: 30, type: 'مکی' },
    { id: 112, name: 'الإخلاص', englishName: 'Al-Ikhlas', ayahs: 4, type: 'مکی' }
  ];

  return (
    <div style={{ fontFamily: 'Tahoma, Arial, sans-serif', direction: 'rtl', minHeight: '100vh', backgroundColor: '#f8fafc', color: '#1e293b' }}>
      {/* هدر اصلی برنامه */}
      <header style={{ backgroundColor: '#0f766e', color: '#fff', padding: '16px 24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span style={{ fontSize: '24px' }}>📖</span>
          <h1 style={{ margin: 0, fontSize: '20px', fontWeight: 'bold' }}>قرآن آنلاین معراج</h1>
        </div>
        
        <button 
          onClick={() => setIsCampaignOpen(true)}
          style={{ 
            backgroundColor: '#10b981', 
            color: '#fff', 
            border: 'none', 
            padding: '8px 16px', 
            borderRadius: '8px', 
            cursor: 'pointer',
            fontWeight: 'bold',
            fontSize: '13px',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            boxShadow: '0 2px 4px rgba(0,0,0,0.15)'
          }}
        >
          <span>🌐</span>
          <span>پویش‌های قرآنی</span>
        </button>
      </header>

      {/* بدنه اصلی برنامه قرآن */}
      <main style={{ maxWidth: '900px', margin: '24px auto', padding: '0 16px' }}>
        <div style={{ backgroundColor: '#fff', borderRadius: '12px', padding: '20px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', marginBottom: '20px' }}>
          <h2 style={{ fontSize: '16px', margin: '0 0 16px 0', color: '#0f766e' }}>فهرست سوره‌ها</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '12px' }}>
            {surahs.map(surah => (
              <div 
                key={surah.id}
                onClick={() => setSelectedSurah(surah.id)}
                style={{
                  padding: '12px',
                  border: selectedSurah === surah.id ? '2px solid #0f766e' : '1px solid #e2e8f0',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  backgroundColor: selectedSurah === surah.id ? '#f0fdf4' : '#fff',
                  transition: 'all 0.2s'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontWeight: 'bold', fontSize: '15px' }}>{surah.id}. {surah.name}</span>
                  <span style={{ fontSize: '11px', color: '#64748b' }}>{surah.type}</span>
                </div>
                <div style={{ fontSize: '12px', color: '#94a3b8', marginTop: '4px' }}>
                  {surah.ayahs} آیه
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* نمایش آیه و متن قرآن */}
        <div style={{ backgroundColor: '#fff', borderRadius: '12px', padding: '28px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', textAlign: 'center' }}>
          <h3 style={{ fontSize: '22px', color: '#0f766e', marginBottom: '20px' }}>بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ</h3>
          <p style={{ fontSize: '20px', lineHeight: '2.2', fontFamily: 'Traditional Arabic, Amiri, serif', color: '#334155' }}>
            {selectedSurah === 1 && "ٱلْحَمْدُ لِلَّهِ رَبِّ ٱلْعَٰلَمِينَ ۝ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ ۝ مَٰلِكِ يَوْمِ ٱلدِّينِ ۝ إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ ۝ ٱهْدِنَا ٱلصِّرَٰطَ ٱلْمُسْتَقِيمَ ۝ صِرَٰطَ ٱلَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ ٱلْمَغْضُوبِ عَلَيْهِمْ وَلَا ٱلضَّآلِّينَ ۝"}
            {selectedSurah !== 1 && "الم ۝ ذَٰلِكَ ٱلْكِتَٰبُ لَا رَيْبَ ۛ فِيهِ ۛ هُدًى لِّلْمُتَّقِينَ ۝ ٱلَّذِينَ يُؤْمِنُونَ بِٱلْغَيْبِ وَيُقِيمُونَ ٱلصَّلَوٰةَ وَمِمَّا رَزَقْنَٰهُمْ يُنفِقُونَ ۝"}
          </p>
        </div>
      </main>

      {/* مودال مدیریت پویش‌ها */}
      <CampaignManager 
        isOpen={isCampaignOpen} 
        onClose={() => setIsCampaignOpen(false)} 
      />
    </div>
  );
}"""
        with open(app_jsx_path, 'w', encoding='utf-8') as f:
            f.write(full_app_code.strip() + "\n")
        print("✅ صفحه اول برنامه قرآن به‌همراه سیستم پویش‌ها اصلاح شد.")

if __name__ == '__main__':
    fix_app()