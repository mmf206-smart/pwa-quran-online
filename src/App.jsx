import CampaignManager from './components/CampaignManager/CampaignManager';
import { useState, useEffect, useRef } from 'react';
import './App.css';

// لیست قاریان (شامل قاریان تندخوان/تحدیر و ترتیل)
const RECITERS = [
  { id: 'ar.parhizgar', name: '⚡ استاد شهریار پرهیزگار (تندخوانی)' },
  { id: 'ar.mahermuaiqly', name: '⚡ استاد ماهر المعیقلی (تندخوان)' },
  { id: 'ar.saoodshuraym', name: '⚡ استاد سعود الشریم (تندخوان)' },
  { id: 'ar.alafasy', name: 'استاد مشاری العفاسی' },
  { id: 'ar.abdulbasitmurattal', name: 'استاد عبدالباسط (ترتیل)' },
  { id: 'ar.minshawi', name: 'استاد محمد صدیق منشاوی' },
  { id: 'ar.husary', name: 'استاد خلیل الحصری' },
];

// تم‌های پیش‌فرض آماده
const PRESET_THEMES = {
  defaultDark: {
    bgColor: '#0f172a',
    cardBg: '#1e293b',
    arabicColor: '#f8fafc',
    translationColor: '#cbd5e1'
  },
  oledBlack: {
    bgColor: '#000000',
    cardBg: '#121212',
    arabicColor: '#ffffff',
    translationColor: '#a0a0a0'
  },
  sepiaPaper: {
    bgColor: '#fbf0d9',
    cardBg: '#f5e5c9',
    arabicColor: '#2d1f10',
    translationColor: '#5c4b3f'
  },
  cleanLight: {
    bgColor: '#f1f5f9',
    cardBg: '#ffffff',
    arabicColor: '#0f172a',
    translationColor: '#475569'
  }
};

function App() {
  const [surahs, setSurahs] = useState([]);
  const [viewTab, setViewTab] = useState('surah'); // 'surah' | 'juz' | 'page'
  const [selectedSelection, setSelectedSelection] = useState(null); // { type, id, title }
  const [ayahs, setAyahs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  
  const [selectedReciter, setSelectedReciter] = useState('ar.parhizgar');
  const [currentAyahIndex, setCurrentAyahIndex] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackRate, setPlaybackRate] = useState(1); // سرعت تندخوانی
  const audioRef = useRef(null);

  // --- سیستم تنظیمات رنگ سفارشی ---
  const [theme, setTheme] = useState(() => {
    const saved = localStorage.getItem('quran_theme_colors');
    return saved ? JSON.parse(saved) : PRESET_THEMES.defaultDark;
  });
  const [settingsModalOpen, setSettingsModalOpen] = useState(false);

  useEffect(() => {
    localStorage.setItem('quran_theme_colors', JSON.stringify(theme));
  }, [theme]);

  const updateThemeColor = (key, value) => {
    setTheme(prev => ({ ...prev, [key]: value }));
  };

  const applyPresetTheme = (presetKey) => {
    if (PRESET_THEMES[presetKey]) {
      setTheme(PRESET_THEMES[presetKey]);
    }
  };

  // --- مدیریت دکمه نصب PWA ---
  const [installPrompt, setInstallPrompt] = useState(null);

  useEffect(() => {
    const handleBeforeInstall = (e) => {
      e.preventDefault();
      setInstallPrompt(e);
    };
    window.addEventListener('beforeinstallprompt', handleBeforeInstall);
    return () => window.removeEventListener('beforeinstallprompt', handleBeforeInstall);
  }, []);

  const handleInstallClick = async () => {
    if (installPrompt) {
      installPrompt.prompt();
      const { outcome } = await installPrompt.userChoice;
      if (outcome === 'accepted') {
        setInstallPrompt(null);
      }
    } else {
      alert('برای نصب روی سیستم/گوشی، از منوی ۳ نقطه مرورگر گزینه Install یا Add to Home Screen را بزنید.');
    }
  };

  // --- سیستم ثبت‌نام و ورود کاربران ---
  const [currentUser, setCurrentUser] = useState(() => {
    const savedSession = localStorage.getItem('quran_session_user');
    return savedSession ? JSON.parse(savedSession) : null;
  });

  const [authModalOpen, setAuthModalOpen] = useState(false);
  const [authMode, setAuthMode] = useState('login'); // 'login' | 'signup'

  const [authName, setAuthName] = useState('');
  const [authEmail, setAuthEmail] = useState('');
  const [authPassword, setAuthPassword] = useState('');
  const [authConfirmPassword, setAuthConfirmPassword] = useState('');
  const [authError, setAuthError] = useState('');

  useEffect(() => {
    if (currentUser) {
      localStorage.setItem('quran_session_user', JSON.stringify(currentUser));
    } else {
      localStorage.removeItem('quran_session_user');
    }
  }, [currentUser]);

  const [notes, setNotes] = useState({});
  const [bookmark, setBookmark] = useState(null);

  useEffect(() => {
    if (currentUser) {
      const userNotes = localStorage.getItem(`quran_notes_${currentUser.id}`);
      setNotes(userNotes ? JSON.parse(userNotes) : {});

      const userBookmark = localStorage.getItem(`quran_bookmark_${currentUser.id}`);
      setBookmark(userBookmark ? JSON.parse(userBookmark) : null);
    } else {
      setNotes({});
      setBookmark(null);
    }
  }, [currentUser]);

  const [targetGlobalAyah, setTargetGlobalAyah] = useState(null);

  // مودال‌ها
  const [editingNoteAyah, setEditingNoteAyah] = useState(null);
  const [tempNoteText, setTempNoteText] = useState('');
  const [activeTafsir, setActiveTafsir] = useState(null);
  const [tafsirLoading, setTafsirLoading] = useState(false);

  useEffect(() => {
    fetch('https://api.alquran.cloud/v1/surah')
      .then((res) => res.json())
      .then((data) => setSurahs(data.data))
      .catch((err) => console.error('خطا در دریافت لیست سوره‌ها:', err));
  }, []);

  useEffect(() => {
    if (targetGlobalAyah && ayahs.length > 0 && !loading) {
      setTimeout(() => {
        const element = document.getElementById(`ayah-global-${targetGlobalAyah}`);
        if (element) {
          element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        setTargetGlobalAyah(null);
      }, 400);
    }
  }, [ayahs, loading, targetGlobalAyah]);

  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.playbackRate = playbackRate;
    }
  }, [playbackRate, currentAyahIndex, isPlaying]);

  const loadContent = async (type, id, title, reciterId = selectedReciter, scrollToGlobalAyah = null) => {
    setLoading(true);
    setCurrentAyahIndex(null);
    setIsPlaying(false);

    if (scrollToGlobalAyah) {
      setTargetGlobalAyah(scrollToGlobalAyah);
    }

    try {
      const [audioRes, faRes] = await Promise.all([
        fetch(`https://api.alquran.cloud/v1/${type}/${id}/${reciterId}`).then((res) => res.json()),
        fetch(`https://api.alquran.cloud/v1/${type}/${id}/fa.fooladvand`).then((res) => res.json())
      ]);

      if (audioRes.code !== 200 || faRes.code !== 200 || !audioRes.data?.ayahs) {
        throw new Error('پاسخ نامعتبر از سرور');
      }

      const audioAyahs = audioRes.data.ayahs;
      const faAyahs = faRes.data.ayahs;

      const combinedAyahs = audioAyahs.map((ayah, index) => ({
        ...ayah,
        faText: faAyahs[index]?.text || ''
      }));

      setSelectedSelection({ type, id, title });
      setAyahs(combinedAyahs);
    } catch (err) {
      console.error('خطا در بارگذاری محتوا:', err);
      alert('خطا در دریافت اطلاعات. لطفاً اتصال اینترنت خود را بررسی کنید.');
    } finally {
      setLoading(false);
    }
  };

  const handleReciterChange = (e) => {
    const newReciter = e.target.value;
    setSelectedReciter(newReciter);
    if (selectedSelection) {
      loadContent(selectedSelection.type, selectedSelection.id, selectedSelection.title, newReciter);
    }
  };

  const playAyah = (index) => {
    setCurrentAyahIndex(index);
    setIsPlaying(true);
  };

  const handleAudioEnded = () => {
    if (currentAyahIndex !== null && currentAyahIndex < ayahs.length - 1) {
      setCurrentAyahIndex((prevIndex) => prevIndex + 1);
    } else {
      setIsPlaying(false);
      setCurrentAyahIndex(null);
    }
  };

  useEffect(() => {
    if (audioRef.current && currentAyahIndex !== null) {
      audioRef.current.playbackRate = playbackRate;
      audioRef.current.play().catch((err) => console.error('خطا در پخش صوت:', err));
    }
  }, [currentAyahIndex]);

  const togglePlayPause = () => {
    if (!audioRef.current && currentAyahIndex === null) {
      playAyah(0);
      return;
    }

    if (isPlaying) {
      audioRef.current.pause();
      setIsPlaying(false);
    } else {
      if (currentAyahIndex === null) {
        playAyah(0);
      } else {
        audioRef.current.play();
        setIsPlaying(true);
      }
    }
  };

  const handleSignup = (e) => {
    e.preventDefault();
    setAuthError('');

    if (!authName.trim() || !authEmail.trim() || !authPassword.trim()) {
      setAuthError('لطفاً تمام فیلدها را پر کنید.');
      return;
    }

    if (authPassword.length < 4) {
      setAuthError('رمز عبور باید حداقل ۴ کاراکتر باشد.');
      return;
    }

    if (authPassword !== authConfirmPassword) {
      setAuthError('رمز عبور و تکرار آن یکسان نیستند.');
      return;
    }

    const registeredUsers = JSON.parse(localStorage.getItem('quran_registered_users') || '[]');
    const emailExists = registeredUsers.some(u => u.email.toLowerCase() === authEmail.trim().toLowerCase());

    if (emailExists) {
      setAuthError('حسابی با این ایمیل/نام‌کاربری قبلاً ثبت شده است.');
      return;
    }

    const newUser = {
      id: 'usr_' + Date.now(),
      name: authName.trim(),
      email: authEmail.trim().toLowerCase(),
      password: authPassword
    };

    registeredUsers.push(newUser);
    localStorage.setItem('quran_registered_users', JSON.stringify(registeredUsers));

    setCurrentUser({ id: newUser.id, name: newUser.name, email: newUser.email });
    setAuthModalOpen(false);
    resetAuthForm();
  };

  const handleLogin = (e) => {
    e.preventDefault();
    setAuthError('');

    if (!authEmail.trim() || !authPassword.trim()) {
      setAuthError('لطفاً ایمیل/نام‌کاربری و رمز عبور را وارد کنید.');
      return;
    }

    const registeredUsers = JSON.parse(localStorage.getItem('quran_registered_users') || '[]');
    const user = registeredUsers.find(
      u => u.email.toLowerCase() === authEmail.trim().toLowerCase() && u.password === authPassword
    );

    if (!user) {
      setAuthError('اطلاعات ورود اشتباه است یا حسابی یافت نشد.');
      return;
    }

    setCurrentUser({ id: user.id, name: user.name, email: user.email });
    setAuthModalOpen(false);
    resetAuthForm();
  };

  const handleLogout = () => {
    if (window.confirm('آیا قصد خروج از حساب کاربری خود را دارید؟')) {
      setCurrentUser(null);
      setNotes({});
      setBookmark(null);
    }
  };

  const resetAuthForm = () => {
    setAuthName('');
    setAuthEmail('');
    setAuthPassword('');
    setAuthConfirmPassword('');
    setAuthError('');
  };

  const setBookmarkHandler = (ayah) => {
    if (!currentUser) {
      setAuthModalOpen(true);
      return;
    }

    const sName = ayah.surah?.name || selectedSelection.title;
    const newBookmark = {
      type: selectedSelection.type,
      id: selectedSelection.id,
      title: selectedSelection.title,
      surahName: sName,
      ayahNumber: ayah.numberInSurah,
      globalNumber: ayah.number
    };
    setBookmark(newBookmark);
    localStorage.setItem(`quran_bookmark_${currentUser.id}`, JSON.stringify(newBookmark));
  };

  const handleGoToBookmark = () => {
    if (!bookmark) return;
    loadContent(
      bookmark.type || 'surah',
      bookmark.id || 1,
      bookmark.title || 'سوره',
      selectedReciter,
      bookmark.globalNumber
    );
  };

  const handleSaveNote = (globalAyahNumber) => {
    if (!currentUser) {
      setAuthModalOpen(true);
      return;
    }

    const updatedNotes = { ...notes, [globalAyahNumber]: tempNoteText };
    setNotes(updatedNotes);
    localStorage.setItem(`quran_notes_${currentUser.id}`, JSON.stringify(updatedNotes));
    setEditingNoteAyah(null);
    setTempNoteText('');
  };

  // دریافت هوشمند تفسیر
  const openTafsirModal = async (surahNum, ayahNumInSurah, surahName = '') => {
    setTafsirLoading(true);
    setActiveTafsir({ surahNum, ayahNumInSurah, surahName, text: '', sourceName: '' });

    const verseKey = `${surahNum}:${ayahNumInSurah}`;

    let foundText = null;
    let sourceName = '';

    const sources = [
      {
        name: 'تفسیر نور (استاد قرائتی)',
        url: `https://api.alquran.cloud/v1/ayah/${verseKey}/fa.gharaati`,
        parse: (data) => data?.data?.text
      },
      {
        name: 'تفسیر نمونه (آیت‌الله مکارم شیرازی)',
        url: `https://api.quran.com/api/v4/quran/tafsirs/169?verse_key=${verseKey}`,
        parse: (data) => data?.tafsirs?.[0]?.text
      },
      {
        name: 'تفسیر المیزان (علامه طباطبایی)',
        url: `https://api.quran.com/api/v4/quran/tafsirs/170?verse_key=${verseKey}`,
        parse: (data) => data?.tafsirs?.[0]?.text
      },
      {
        name: 'توضیحات و ترجمه روان (استاد مکارم)',
        url: `https://api.alquran.cloud/v1/ayah/${verseKey}/fa.makarem`,
        parse: (data) => data?.data?.text
      }
    ];

    for (const src of sources) {
      try {
        const res = await fetch(src.url);
        if (res.ok) {
          const data = await res.json();
          const extracted = src.parse(data);
          if (extracted && typeof extracted === 'string' && extracted.trim().length > 0) {
            foundText = extracted;
            sourceName = src.name;
            break;
          }
        }
      } catch (err) {
        console.warn('خطا در دریافت تفسیر:', src.url, err);
      }
    }

    if (foundText) {
      setActiveTafsir({
        surahNum,
        ayahNumInSurah,
        surahName,
        text: foundText,
        sourceName
      });
    } else {
      setActiveTafsir({
        surahNum,
        ayahNumInSurah,
        surahName,
        text: 'متأسفانه دریافت آنلاین تفسیر برای این آیه با خطا مواجه شد. لطفاً اتصال اینترنت خود را بررسی کنید.',
        sourceName: ''
      });
    }
    setTafsirLoading(false);
  };

  const filteredSurahs = surahs.filter((surah) =>
    surah.name.includes(searchQuery) ||
    surah.englishName.toLowerCase().includes(searchQuery.toLowerCase()) ||
    surah.number.toString() === searchQuery
  );

  const juzList = Array.from({ length: 30 }, (_, i) => i + 1);
  const filteredJuzs = juzList.filter((juz) =>
    juz.toString().includes(searchQuery) || `جزء ${juz}`.includes(searchQuery)
  );

  const pageList = Array.from({ length: 604 }, (_, i) => i + 1);
  const filteredPages = pageList.filter((page) =>
    page.toString().includes(searchQuery) || `صفحه ${page}`.includes(searchQuery)
  );

  // استایل‌های پویای متغیرهای رنگی
  const dynamicStyle = {
    '--app-bg': theme.bgColor,
    '--card-bg': theme.cardBg,
    '--arabic-color': theme.arabicColor,
    '--translation-color': theme.translationColor,
  };

  return (
    <div className="app-container" dir="rtl" style={dynamicStyle}>
      {/* نوار ابزار و هدر اصلی برنامه */}
      {/* نوار ابزار و هدر اصلی برنامه */}
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

      {bookmark && currentUser && !selectedSelection && (
        <div className="bookmark-banner">
          <div className="bookmark-info">
            <span className="bookmark-title">🔖 آخرین سرخط مطالعه ({currentUser.name})</span>
            <span className="bookmark-sub">{bookmark.surahName} - آیه {bookmark.ayahNumber}</span>
          </div>
          <button onClick={handleGoToBookmark} className="resume-btn">
            ادامه مطالعه 🚀
          </button>
        </div>
      )}

      {!selectedSelection ? (
        <main className="main-content">
          <div className="tab-navigation">
            <button 
              className={`tab-btn ${viewTab === 'surah' ? 'active' : ''}`}
              onClick={() => { setViewTab('surah'); setSearchQuery(''); }}
            >
              📖 سوره‌ها (۱۱۴)
            </button>
            <button 
              className={`tab-btn ${viewTab === 'juz' ? 'active' : ''}`}
              onClick={() => { setViewTab('juz'); setSearchQuery(''); }}
            >
              ۞ اجزاء (۳۰)
            </button>
            <button 
              className={`tab-btn ${viewTab === 'page' ? 'active' : ''}`}
              onClick={() => { setViewTab('page'); setSearchQuery(''); }}
            >
              📄 صفحات (۶۰۴)
            </button>
          </div>

          <input
            type="text"
            placeholder={
              viewTab === 'surah' ? "جستجوی سوره (نام یا شماره)..." :
              viewTab === 'juz' ? "جستجوی جزء (۱ تا ۳۰)..." :
              "جستجوی شماره صفحه (۱ تا ۶۰۴)..."
            }
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />

          {viewTab === 'surah' && (
            <div className="surah-grid">
              {filteredSurahs.map((surah) => (
                <div
                  key={surah.number}
                  className="surah-card"
                  onClick={() => loadContent('surah', surah.number, surah.name)}
                >
                  <div className="surah-number">{surah.number}</div>
                  <div className="surah-info">
                    <h3>{surah.name}</h3>
                    <p>{surah.englishName} • {surah.numberOfAyahs} آیه</p>
                  </div>
                </div>
              ))}
            </div>
          )}

          {viewTab === 'juz' && (
            <div className="juz-grid">
              {filteredJuzs.map((juz) => (
                <div
                  key={juz}
                  className="juz-card"
                  onClick={() => loadContent('juz', juz, `جزء ${juz}`)}
                >
                  <div className="juz-icon">۞</div>
                  <div className="juz-info">
                    <h3>جزء {juz}</h3>
                    <p>نمایش کامل آیات جزء {juz}</p>
                  </div>
                </div>
              ))}
            </div>
          )}

          {viewTab === 'page' && (
            <div className="page-grid">
              {filteredPages.map((page) => (
                <div
                  key={page}
                  className="page-card"
                  onClick={() => loadContent('page', page, `صفحه ${page}`)}
                >
                  <div className="page-number">{page}</div>
                  <p className="page-label">صفحه {page}</p>
                </div>
              ))}
            </div>
          )}
        </main>
      ) : (
        <main className="surah-detail">
          <div className="surah-header">
            <h2>{selectedSelection.title}</h2>
            <div className="meta-tags">
              <span className="tag">📄 {ayahs.length} آیه</span>
              <span className="tag">
                {selectedSelection.type === 'surah' ? 'سوره' : selectedSelection.type === 'juz' ? 'جزء کامل' : 'صفحه کامل'}
              </span>
              {currentUser && <span className="tag user-tag">👤 {currentUser.name}</span>}
              <span className="tag speed-tag">⚡ سرعت پخش: {playbackRate}x</span>
            </div>

            <div className="player-controls">
              <button className="play-all-btn" onClick={togglePlayPause}>
                {isPlaying ? '⏸ توقف پخش' : '▶ پخش پیوسته'}
              </button>
            </div>
          </div>

          {currentAyahIndex !== null && (
            <audio
              ref={audioRef}
              src={ayahs[currentAyahIndex]?.audio}
              onEnded={handleAudioEnded}
              onPlay={() => setIsPlaying(true)}
              onPause={() => setIsPlaying(false)}
            />
          )}

          {loading ? (
            <div className="loading">در حال بارگذاری اطلاعات آیات...</div>
          ) : (
            <div className="ayahs-list">
              {ayahs.map((ayah, index) => {
                const isCurrent = currentAyahIndex === index;
                const isBookmarked = bookmark?.globalNumber === ayah.number;
                const hasNote = !!notes[ayah.number];
                const surahNum = ayah.surah?.number || 1;
                const surahName = ayah.surah?.name || selectedSelection.title;

                return (
                  <div 
                    key={ayah.number} 
                    id={`ayah-global-${ayah.number}`}
                    className={`ayah-card ${isCurrent ? 'active-ayah' : ''} ${isBookmarked ? 'bookmarked-ayah' : ''}`}
                  >
                    <div className="ayah-top">
                      <div className="badges-group">
                        <span className="verse-badge">۝ {ayah.numberInSurah}</span>
                        {ayah.surah && <span className="surah-badge">{ayah.surah.name}</span>}
                        <span className="juz-badge">جزء {ayah.juz}</span>
                        {ayah.page && <span className="page-badge">صفحه {ayah.page}</span>}
                        {ayah.sajda && <span className="sajda-badge">۩ سجده دار</span>}
                      </div>

                      <div className="ayah-actions">
                        <button 
                          className={`icon-btn ${isBookmarked ? 'active-bookmark' : ''}`}
                          title="علامت‌گذاری سرخط"
                          onClick={() => setBookmarkHandler(ayah)}
                        >
                          🔖 {isBookmarked ? 'سرخط فعال' : 'ثبت سرخط'}
                        </button>

                        <button 
                          className={`icon-btn ${hasNote ? 'active-note' : ''}`}
                          onClick={() => {
                            if (!currentUser) {
                              setAuthModalOpen(true);
                              return;
                            }
                            setEditingNoteAyah(ayah.number);
                            setTempNoteText(notes[ayah.number] || '');
                          }}
                        >
                          📝 {hasNote ? 'ویرایش یادداشت' : 'یادداشت'}
                        </button>

                        <button 
                          className="icon-btn tafsir-btn"
                          onClick={() => openTafsirModal(surahNum, ayah.numberInSurah, surahName)}
                        >
                          📚 تفسیر
                        </button>

                        <button 
                          className={`play-ayah-btn ${isCurrent && isPlaying ? 'playing' : ''}`} 
                          onClick={() => playAyah(index)}
                        >
                          {isCurrent && isPlaying ? '🔊 در حال پخش' : '▶ پخش صوت'}
                        </button>
                      </div>
                    </div>

                    <p className="arabic-text">{ayah.text}</p>
                    <p className="translation-text">{ayah.faText}</p>

                    {hasNote && currentUser && (
                      <div className="saved-note-box">
                        📌 <strong>یادداشت شما:</strong> {notes[ayah.number]}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </main>
      )}

      {/* مودال تنظیمات رنگ و ظاهر */}
      {settingsModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content color-settings-modal">
            <h3>🎨 تنظیمات سفارشی رنگ و تم</h3>

            <div className="presets-box">
              <label>تم‌های آماده سریع:</label>
              <div className="preset-buttons">
                <button onClick={() => applyPresetTheme('defaultDark')} className="preset-btn dark">تاریک کلاسیک</button>
                <button onClick={() => applyPresetTheme('oledBlack')} className="preset-btn oled">مشکی کامل (AMOLED)</button>
                <button onClick={() => applyPresetTheme('sepiaPaper')} className="preset-btn sepia">کاغذی / سپیا</button>
                <button onClick={() => applyPresetTheme('cleanLight')} className="preset-btn light">روشن</button>
              </div>
            </div>

            <hr className="divider" />

            <div className="color-pickers-grid">
              <div className="color-picker-item">
                <label>رنگ پس‌زمینه اصلی:</label>
                <input 
                  type="color" 
                  value={theme.bgColor} 
                  onChange={(e) => updateThemeColor('bgColor', e.target.value)} 
                />
              </div>

              <div className="color-picker-item">
                <label>رنگ پس‌زمینه کارت‌ها:</label>
                <input 
                  type="color" 
                  value={theme.cardBg} 
                  onChange={(e) => updateThemeColor('cardBg', e.target.value)} 
                />
              </div>

              <div className="color-picker-item">
                <label>رنگ فونت متن عربی:</label>
                <input 
                  type="color" 
                  value={theme.arabicColor} 
                  onChange={(e) => updateThemeColor('arabicColor', e.target.value)} 
                />
              </div>

              <div className="color-picker-item">
                <label>رنگ فونت ترجمه فارسی:</label>
                <input 
                  type="color" 
                  value={theme.translationColor} 
                  onChange={(e) => updateThemeColor('translationColor', e.target.value)} 
                />
              </div>
            </div>

            <div className="modal-actions">
              <button onClick={() => setSettingsModalOpen(false)} className="save-btn">تأیید و بستن</button>
            </div>
          </div>
        </div>
      )}

      {/* مودال یادداشت */}
      {editingNoteAyah !== null && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3>📝 ثبت یادداشت شخصی</h3>
            <textarea
              rows="4"
              value={tempNoteText}
              onChange={(e) => setTempNoteText(e.target.value)}
              placeholder="نکات تجویدی، برداشت یا یادداشت شخصی خود را بنویسید..."
              className="note-textarea"
            />
            <div className="modal-actions">
              <button onClick={() => handleSaveNote(editingNoteAyah)} className="save-btn">ذخیره یادداشت</button>
              <button onClick={() => setEditingNoteAyah(null)} className="cancel-btn">انصراف</button>
            </div>
          </div>
        </div>
      )}

      {/* مودال نمایش کامل تفسیر */}
      {activeTafsir && (
        <div className="modal-overlay">
          <div className="modal-content tafsir-modal">
            <h3>📚 {activeTafsir.sourceName || 'تفسیر آیات'} - {activeTafsir.surahName} (آیه {activeTafsir.ayahNumInSurah})</h3>
            <div className="tafsir-body">
              {tafsirLoading ? (
                <p className="loading">در حال بارگذاری متن تفسیر فارسی...</p>
              ) : (
                <div 
                  className="tafsir-text"
                  dangerouslySetInnerHTML={{ __html: activeTafsir.text }}
                />
              )}
            </div>
            <div className="modal-actions">
              <button onClick={() => setActiveTafsir(null)} className="cancel-btn">بستن تفسیر</button>
            </div>
          </div>
        </div>
      )}

      {/* مودال احراز هویت */}
      {authModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content auth-modal">
            <div className="auth-tab-nav">
              <button 
                className={`auth-tab ${authMode === 'login' ? 'active' : ''}`}
                onClick={() => { setAuthMode('login'); resetAuthForm(); }}
              >
                🔑 ورود به حساب
              </button>
              <button 
                className={`auth-tab ${authMode === 'signup' ? 'active' : ''}`}
                onClick={() => { setAuthMode('signup'); resetAuthForm(); }}
              >
                👤 ثبت‌نام کاربر جدید
              </button>
            </div>

            {authError && <div className="auth-error-box">⚠️ {authError}</div>}

            {authMode === 'login' ? (
              <form onSubmit={handleLogin} className="auth-form">
                <label>ایمیل یا نام کاربری:</label>
                <input
                  type="text"
                  value={authEmail}
                  onChange={(e) => setAuthEmail(e.target.value)}
                  placeholder="مثلاً: ali@gmail.com"
                  className="auth-input"
                />

                <label>رمز عبور:</label>
                <input
                  type="password"
                  value={authPassword}
                  onChange={(e) => setAuthPassword(e.target.value)}
                  placeholder="••••••••"
                  className="auth-input"
                />

                <div className="modal-actions">
                  <button type="submit" className="save-btn">ورود به حساب</button>
                  <button type="button" onClick={() => setAuthModalOpen(false)} className="cancel-btn">انصراف</button>
                </div>
              </form>
            ) : (
              <form onSubmit={handleSignup} className="auth-form">
                <label>نام و نام خانوادگی:</label>
                <input
                  type="text"
                  value={authName}
                  onChange={(e) => setAuthName(e.target.value)}
                  placeholder="مثلاً: علی محمدی"
                  className="auth-input"
                />

                <label>ایمیل یا شناسه کاربری:</label>
                <input
                  type="text"
                  value={authEmail}
                  onChange={(e) => setAuthEmail(e.target.value)}
                  placeholder="مثلاً: ali@gmail.com"
                  className="auth-input"
                />

                <label>رمز عبور:</label>
                <input
                  type="password"
                  value={authPassword}
                  onChange={(e) => setAuthPassword(e.target.value)}
                  placeholder="حداقل ۴ کاراکتر"
                  className="auth-input"
                />

                <label>تکرار رمز عبور:</label>
                <input
                  type="password"
                  value={authConfirmPassword}
                  onChange={(e) => setAuthConfirmPassword(e.target.value)}
                  placeholder="تکرار رمز عبور"
                  className="auth-input"
                />

                <div className="modal-actions">
                  <button type="submit" className="save-btn">ایجاد حساب و ورود</button>
                  <button type="button" onClick={() => setAuthModalOpen(false)} className="cancel-btn">انصراف</button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;