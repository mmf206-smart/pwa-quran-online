import { useState, useEffect, useRef } from 'react';
import './App.css';

const RECITERS = [
  { id: 'ar.alafasy', name: 'استاد مشاری العفاسی' },
  { id: 'ar.abdulbasitmurattal', name: 'استاد عبدالباسط (ترتیل)' },
  { id: 'ar.minshawi', name: 'استاد محمد صدیق منشاوی' },
  { id: 'ar.husary', name: 'استاد خلیل الحصری' },
];

function App() {
  const [surahs, setSurahs] = useState([]);
  const [viewTab, setViewTab] = useState('surah'); // 'surah' | 'juz' | 'page'
  const [selectedSelection, setSelectedSelection] = useState(null); // { type, id, title }
  const [ayahs, setAyahs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  
  const [selectedReciter, setSelectedReciter] = useState('ar.alafasy');
  const [currentAyahIndex, setCurrentAyahIndex] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef(null);

  // --- سیستم ثبت‌نام و ورود کاربران (Authentication) ---
  const [currentUser, setCurrentUser] = useState(() => {
    const savedSession = localStorage.getItem('quran_session_user');
    return savedSession ? JSON.parse(savedSession) : null;
  });

  const [authModalOpen, setAuthModalOpen] = useState(false);
  const [authMode, setAuthMode] = useState('login'); // 'login' | 'signup'

  // فرم‌های ورودی ثبت‌نام/ورود
  const [authName, setAuthName] = useState('');
  const [authEmail, setAuthEmail] = useState('');
  const [authPassword, setAuthPassword] = useState('');
  const [authConfirmPassword, setAuthConfirmPassword] = useState('');
  const [authError, setAuthError] = useState('');

  // ثبت کاربر فعال در نشست
  useEffect(() => {
    if (currentUser) {
      localStorage.setItem('quran_session_user', JSON.stringify(currentUser));
    } else {
      localStorage.removeItem('quran_session_user');
    }
  }, [currentUser]);

  // وضعیت یادداشت‌ها و سرخط کاربر جاری
  const [notes, setNotes] = useState({});
  const [bookmark, setBookmark] = useState(null);

  // بارگذاری یادداشت‌ها و سرخط مخصوص کاربر جاری
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

  // اسکرول خودکار به آیه
  const [targetGlobalAyah, setTargetGlobalAyah] = useState(null);

  // مودال‌ها
  const [editingNoteAyah, setEditingNoteAyah] = useState(null);
  const [tempNoteText, setTempNoteText] = useState('');
  const [activeTafsir, setActiveTafsir] = useState(null);
  const [tafsirLoading, setTafsirLoading] = useState(false);

  // دریافت لیست سوره‌ها
  useEffect(() => {
    fetch('https://api.alquran.cloud/v1/surah')
      .then((res) => res.json())
      .then((data) => setSurahs(data.data))
      .catch((err) => console.error('خطا در دریافت لیست سوره‌ها:', err));
  }, []);

  // اسکرول نرم به آیه مقصد
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

  // بارگذاری محتوا (سوره، جزء یا صفحه)
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
      alert('خطا در دریافت اطلاعات. لطفاً اتصال اینترنت خود را بررسی کرده و مجدداً تلاش کنید.');
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

  // --- عملیات احراز هویت (Auth Functions) ---
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

    // ورود خودکار بعد از ثبت‌نام
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

  // ثبت سرخط برای کاربر وارد شده
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

  // پرش به سرخط
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

  // ذخیره یادداشت
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

  // دریافت هوشمند و تضمین‌شده تفسیر/توضیح فارسی
  const openTafsirModal = async (surahNum, ayahNumInSurah, surahName = '') => {
    setTafsirLoading(true);
    setActiveTafsir({ surahNum, ayahNumInSurah, surahName, text: '', sourceName: '' });

    const verseKey = `${surahNum}:${ayahNumInSurah}`;

    const isEnglish = (str) => {
      if (!str) return false;
      const cleanText = str.replace(/<[^>]*>/g, '');
      const engMatches = cleanText.match(/[a-zA-Z]/g);
      return engMatches && (engMatches.length > 20 || (engMatches.length / cleanText.length) > 0.3);
    };

    let foundText = null;
    let sourceName = '';

    const sources = [
      {
        name: 'تفسیر نمونه (Quran.com)',
        url: `https://api.quran.com/api/v4/quran/tafsirs/fa-tafsir-nemoneh?verse_key=${verseKey}`,
        parse: (data) => data?.tafsirs?.[0]?.text
      },
      {
        name: 'تفسیر نمونه (مسیر دوم)',
        url: `https://api.quran.com/api/v4/tafsirs/fa-tafsir-nemoneh/by_ayah/${verseKey}`,
        parse: (data) => data?.tafsir?.text
      },
      {
        name: 'تفسیر المیزان (علامه طباطبایی)',
        url: `https://api.quran.com/api/v4/quran/tafsirs/fa-tafsir-al-mizan?verse_key=${verseKey}`,
        parse: (data) => data?.tafsirs?.[0]?.text
      },
      {
        name: 'ترجمه و توضیحات جامع (استاد مکارم)',
        url: `https://quranenc.com/api/v1/translation/ayah/persian_makarem/${surahNum}/${ayahNumInSurah}`,
        parse: (data) => data?.result?.footnote || data?.result?.translation
      }
    ];

    for (const src of sources) {
      try {
        const res = await fetch(src.url);
        if (res.ok) {
          const data = await res.json();
          const extracted = src.parse(data);
          if (extracted && typeof extracted === 'string' && extracted.trim().length > 0 && !isEnglish(extracted)) {
            foundText = extracted;
            sourceName = src.name;
            break;
          }
        }
      } catch (err) {
        console.warn('تلاش برای دریافت تفسیر ناموفق بود:', src.url, err);
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
        text: 'متن تفسیری فارسی برای این آیه در دیتابیس آنلاین یافت نشد.',
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

  return (
    <div className="app-container" dir="rtl">
      <header className="header">
        <div className="header-title-section">
          <h1>📖 قرآن آنلاین PWA</h1>
          
          {/* بخش وضعیت حساب کاربری */}
          <div className="user-auth-badge">
            {currentUser ? (
              <div className="logged-user-info">
                <span className="user-greeting">👤 {currentUser.name}</span>
                <button onClick={handleLogout} className="logout-btn" title="خروج از حساب">
                  🚪 خروج
                </button>
              </div>
            ) : (
              <button 
                onClick={() => { resetAuthForm(); setAuthMode('login'); setAuthModalOpen(true); }} 
                className="login-trigger-btn"
              >
                🔑 ورود / ثبت‌نام
              </button>
            )}
          </div>
        </div>
        
        <div className="header-actions">
          {bookmark && currentUser && (
            <button className="header-bookmark-btn" onClick={handleGoToBookmark} title="پرش مستقیم به سرخط">
              🔖 سرخط من ({bookmark.surahName} - آیه {bookmark.ayahNumber})
            </button>
          )}

          <select value={selectedReciter} onChange={handleReciterChange} className="reciter-select">
            {RECITERS.map((r) => (
              <option key={r.id} value={r.id}>{r.name}</option>
            ))}
          </select>

          {selectedSelection && (
            <button 
              className="back-btn" 
              onClick={() => { 
                setSelectedSelection(null); 
                setIsPlaying(false); 
                setCurrentAyahIndex(null); 
              }}
            >
              ← فهرست اصلی
            </button>
          )}
        </div>
      </header>

      {/* بنر سرخط کاربر جاری */}
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

      {/* مودال احراز هویت (ورود / ثبت‌نام) */}
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