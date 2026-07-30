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

  // حافظه داخلی: یادداشت‌ها و سرخط
  const [notes, setNotes] = useState(() => JSON.parse(localStorage.getItem('quran_notes') || '{}'));
  const [bookmark, setBookmark] = useState(() => JSON.parse(localStorage.getItem('quran_bookmark') || 'null'));
  
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
  const loadContent = (type, id, title, reciterId = selectedReciter, scrollToGlobalAyah = null) => {
    setLoading(true);
    setCurrentAyahIndex(null);
    setIsPlaying(false);

    if (scrollToGlobalAyah) {
      setTargetGlobalAyah(scrollToGlobalAyah);
    }

    let endpoint = '';
    if (type === 'surah') {
      endpoint = `https://api.alquran.cloud/v1/surah/${id}/editions/${reciterId},fa.fooladvand`;
    } else if (type === 'juz') {
      endpoint = `https://api.alquran.cloud/v1/juz/${id}/editions/${reciterId},fa.fooladvand`;
    } else if (type === 'page') {
      endpoint = `https://api.alquran.cloud/v1/page/${id}/editions/${reciterId},fa.fooladvand`;
    }

    fetch(endpoint)
      .then((res) => res.json())
      .then((data) => {
        if (!data.data || !Array.isArray(data.data)) {
          throw new Error('داده دریافت نشد');
        }

        const audioData = data.data[0];
        const faData = data.data[1];

        const combinedAyahs = audioData.ayahs.map((ayah, index) => ({
          ...ayah,
          faText: faData.ayahs[index]?.text
        }));

        setSelectedSelection({ type, id, title });
        setAyahs(combinedAyahs);
        setLoading(false);
      })
      .catch((err) => {
        console.error('خطا در بارگذاری محتوا:', err);
        alert('خطا در دریافت اطلاعات. لطفاً مجدداً تلاش کنید.');
        setLoading(false);
      });
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

  // ثبت سرخط
  const setBookmarkHandler = (ayah) => {
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
    localStorage.setItem('quran_bookmark', JSON.stringify(newBookmark));
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

  // یادداشت‌نویسی
  const handleSaveNote = (globalAyahNumber) => {
    const updatedNotes = { ...notes, [globalAyahNumber]: tempNoteText };
    setNotes(updatedNotes);
    localStorage.setItem('quran_notes', JSON.stringify(updatedNotes));
    setEditingNoteAyah(null);
    setTempNoteText('');
  };

  // دریافت متن واقعی تفسیر نمونه (Tafseer Nemoneh API)
  const openTafsirModal = (surahNum, ayahNumInSurah, ayahGlobalNum) => {
    setTafsirLoading(true);
    setActiveTafsir({ surahNum, ayahNumInSurah, text: '' });

    // وب‌سرویس اختصاصی تفسیر نمونه (کد ۱۶۹)
    fetch(`https://api.quran.com/api/v4/tafsirs/169/by_key/${surahNum}:${ayahNumInSurah}`)
      .then((res) => res.json())
      .then((data) => {
        let tafsirContent = data.tafsir?.text || 'متن تفسیری برای این آیه یافت نشد.';
        setActiveTafsir({
          surahNum,
          ayahNumInSurah,
          text: tafsirContent
        });
        setTafsirLoading(false);
      })
      .catch((err) => {
        console.error('خطا در دریافت تفسیر:', err);
        setActiveTafsir({ surahNum, ayahNumInSurah, text: 'خطا در برقراری ارتباط با سرور تفسیر.' });
        setTafsirLoading(false);
      });
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
        <h1>📖 قرآن آنلاین PWA</h1>
        
        <div className="header-actions">
          {bookmark && (
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

      {/* بنر سرخط */}
      {bookmark && !selectedSelection && (
        <div className="bookmark-banner">
          <div className="bookmark-info">
            <span className="bookmark-title">🔖 آخرین سرخط مطالعه شما</span>
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
                const surahNum = ayah.surah?.number || selectedSelection.id;

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
                          title="علامت‌گذاری به‌عنوان سرخط یادآوری"
                          onClick={() => setBookmarkHandler(ayah)}
                        >
                          🔖 {isBookmarked ? 'سرخط فعال' : 'ثبت سرخط'}
                        </button>

                        <button 
                          className={`icon-btn ${hasNote ? 'active-note' : ''}`}
                          onClick={() => {
                            setEditingNoteAyah(ayah.number);
                            setTempNoteText(notes[ayah.number] || '');
                          }}
                        >
                          📝 {hasNote ? 'ویرایش یادداشت' : 'یادداشت'}
                        </button>

                        <button 
                          className="icon-btn tafsir-btn"
                          onClick={() => openTafsirModal(surahNum, ayah.numberInSurah, ayah.number)}
                        >
                          📚 تفسیر نمونه
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

                    {hasNote && (
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
            <h3>📝 ثبت یادداشت روی آیه</h3>
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

      {/* مودال نمایش کامل تفسیر نمونه */}
      {activeTafsir && (
        <div className="modal-overlay">
          <div className="modal-content tafsir-modal">
            <h3>📚 تفسیر نمونه - آیه {activeTafsir.ayahNumInSurah}</h3>
            <div className="tafsir-body">
              {tafsirLoading ? (
                <p className="loading">در حال بارگذاری متن کامل تفسیر نمونه...</p>
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
    </div>
  );
}

export default App;