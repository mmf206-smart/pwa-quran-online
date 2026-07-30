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
  const [selectedSurah, setSelectedSurah] = useState(null);
  const [ayahs, setAyahs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  
  // تنظیمات قاری
  const [selectedReciter, setSelectedReciter] = useState('ar.alafasy');
  
  // وضعیت‌های پخش صوت
  const [currentAyahIndex, setCurrentAyahIndex] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef(null);

  // حافظه داخلی: یادداشت‌ها و سرخط آخرین مطالعه
  const [notes, setNotes] = useState(() => JSON.parse(localStorage.getItem('quran_notes') || '{}'));
  const [bookmark, setBookmark] = useState(() => JSON.parse(localStorage.getItem('quran_bookmark') || 'null'));
  const [editingNoteAyah, setEditingNoteAyah] = useState(null);
  const [tempNoteText, setTempNoteText] = useState('');

  // مودال تفسیر آیه
  const [activeTafsir, setActiveTafsir] = useState(null);
  const [tafsirLoading, setTafsirLoading] = useState(false);

  // دریافت لیست کامل سوره‌ها
  useEffect(() => {
    fetch('https://api.alquran.cloud/v1/surah')
      .then((res) => res.json())
      .then((data) => setSurahs(data.data))
      .catch((err) => console.error('خطا در دریافت لیست سوره‌ها:', err));
  }, []);

  // بارگذاری سوره انتخاب شده با قاری فعال
  const loadSurah = (surahNumber, reciterId = selectedReciter) => {
    setLoading(true);
    setCurrentAyahIndex(null);
    setIsPlaying(false);

    fetch(`https://api.alquran.cloud/v1/surah/${surahNumber}/editions/${reciterId},fa.fooladvand,ar.tajweed`)
      .then((res) => res.json())
      .then((data) => {
        const audioSurah = data.data[0];
        const faSurah = data.data[1];
        const tajweedSurah = data.data[2];

        const combinedAyahs = audioSurah.ayahs.map((ayah, index) => ({
          ...ayah,
          faText: faSurah.ayahs[index]?.text,
          tajweedText: tajweedSurah.ayahs[index]?.text
        }));

        setSelectedSurah(audioSurah);
        setAyahs(combinedAyahs);
        setLoading(false);
      })
      .catch((err) => {
        console.error('خطا در دریافت اطلاعات سوره:', err);
        setLoading(false);
      });
  };

  const handleSelectSurah = (surahNumber) => {
    loadSurah(surahNumber, selectedReciter);
  };

  // تغییر قاری
  const handleReciterChange = (e) => {
    const newReciter = e.target.value;
    setSelectedReciter(newReciter);
    if (selectedSurah) {
      loadSurah(selectedSurah.number, newReciter);
    }
  };

  // مدیریت پخش صوت
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

  // مدیریت ذخیره سر خط یادآوری (Bookmark)
  const setBookmarkHandler = (ayah) => {
    const newBookmark = {
      surahNumber: selectedSurah.number,
      surahName: selectedSurah.name,
      ayahNumber: ayah.numberInSurah,
      globalNumber: ayah.number
    };
    setBookmark(newBookmark);
    localStorage.setItem('quran_bookmark', JSON.stringify(newBookmark));
  };

  // مدیریت ذخیره یادداشت روی آیه
  const handleSaveNote = (globalAyahNumber) => {
    const updatedNotes = { ...notes, [globalAyahNumber]: tempNoteText };
    setNotes(updatedNotes);
    localStorage.setItem('quran_notes', JSON.stringify(updatedNotes));
    setEditingNoteAyah(null);
    setTempNoteText('');
  };

  // دریافت و نمایش تفسیر آیه (تفسیر نمونه / آیت‌الله مکارم)
  const openTafsirModal = (globalAyahNumber, ayahInSurah) => {
    setTafsirLoading(true);
    setActiveTafsir({ ayahInSurah, text: '' });

    fetch(`https://api.alquran.cloud/v1/ayah/${globalAyahNumber}/fa.makarem`)
      .then((res) => res.json())
      .then((data) => {
        setActiveTafsir({
          ayahInSurah,
          text: data.data.text || 'تفسیر برای این آیه یافت نشد.'
        });
        setTafsirLoading(false);
      })
      .catch((err) => {
        console.error('خطا در دریافت تفسیر:', err);
        setActiveTafsir({ ayahInSurah, text: 'خطا در برقراری ارتباط با سرور تفسیر.' });
        setTafsirLoading(false);
      });
  };

  const filteredSurahs = surahs.filter((surah) =>
    surah.name.includes(searchQuery) ||
    surah.englishName.toLowerCase().includes(searchQuery.toLowerCase()) ||
    surah.number.toString() === searchQuery
  );

  return (
    <div className="app-container" dir="rtl">
      <header className="header">
        <h1>📖 قرآن آنلاین PWA</h1>
        
        <div className="header-actions">
          {/* انتخاب قاری */}
          <select value={selectedReciter} onChange={handleReciterChange} className="reciter-select">
            {RECITERS.map((r) => (
              <option key={r.id} value={r.id}>{r.name}</option>
            ))}
          </select>

          {selectedSurah && (
            <button 
              className="back-btn" 
              onClick={() => { 
                setSelectedSurah(null); 
                setIsPlaying(false); 
                setCurrentAyahIndex(null); 
              }}
            >
              ← لیست سوره‌ها
            </button>
          )}
        </div>
      </header>

      {/* نمایش سرخط مطالعه قبلی در صورت وجود */}
      {bookmark && !selectedSurah && (
        <div className="bookmark-banner">
          <span>🔖 آخرین سرخط مطالعه: <strong>{bookmark.surahName}</strong> (آیه {bookmark.ayahNumber})</span>
          <button onClick={() => handleSelectSurah(bookmark.surahNumber)} className="resume-btn">
            ادامه مطالعه →
          </button>
        </div>
      )}

      {!selectedSurah ? (
        <main className="main-content">
          <input
            type="text"
            placeholder="جستجوی سوره (نام یا شماره)..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
          <div className="surah-grid">
            {filteredSurahs.map((surah) => (
              <div
                key={surah.number}
                className="surah-card"
                onClick={() => handleSelectSurah(surah.number)}
              >
                <div className="surah-number">{surah.number}</div>
                <div className="surah-info">
                  <h3>{surah.name}</h3>
                  <p>{surah.englishName} • {surah.numberOfAyahs} آیه</p>
                </div>
              </div>
            ))}
          </div>
        </main>
      ) : (
        <main className="surah-detail">
          <div className="surah-header">
            <h2>{selectedSurah.name}</h2>
            <div className="meta-tags">
              <span className="tag">{selectedSurah.englishName}</span>
              <span className="tag">{selectedSurah.revelationType === 'Meccan' ? '🕋 مکی' : '🕌 مدنی'}</span>
              <span className="tag">📄 {selectedSurah.numberOfAyahs} آیه</span>
            </div>

            <div className="player-controls">
              <button className="play-all-btn" onClick={togglePlayPause}>
                {isPlaying ? '⏸ توقف پخش' : '▶ پخش پیوسته سوره'}
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
            <div className="loading">در حال دریافت آيات و تنظیمات تجوید...</div>
          ) : (
            <div className="ayahs-list">
              {ayahs.map((ayah, index) => {
                const isCurrent = currentAyahIndex === index;
                const isBookmarked = bookmark?.globalNumber === ayah.number;
                const hasNote = !!notes[ayah.number];

                return (
                  <div key={ayah.number} className={`ayah-card ${isCurrent ? 'active-ayah' : ''} ${isBookmarked ? 'bookmarked-ayah' : ''}`}>
                    <div className="ayah-top">
                      <div className="badges-group">
                        <span className="verse-badge">۝ {ayah.numberInSurah}</span>
                        <span className="juz-badge">جزء {ayah.juz}</span>
                        {ayah.sajda && <span className="sajda-badge">۩ سجده دار</span>}
                      </div>

                      <div className="ayah-actions">
                        {/* دکمه سر خط یادآوری */}
                        <button 
                          className={`icon-btn ${isBookmarked ? 'active-bookmark' : ''}`}
                          title="علامت‌گذاری به‌عنوان سرخط یادآوری"
                          onClick={() => setBookmarkHandler(ayah)}
                        >
                          🔖 {isBookmarked ? 'سرخط فعال' : 'سرخط'}
                        </button>

                        {/* دکمه یادداشت */}
                        <button 
                          className={`icon-btn ${hasNote ? 'active-note' : ''}`}
                          onClick={() => {
                            setEditingNoteAyah(ayah.number);
                            setTempNoteText(notes[ayah.number] || '');
                          }}
                        >
                          📝 {hasNote ? 'ویرایش یادداشت' : 'یادداشت'}
                        </button>

                        {/* دکمه لینک تفسیر */}
                        <button 
                          className="icon-btn tafsir-btn"
                          onClick={() => openTafsirModal(ayah.number, ayah.numberInSurah)}
                        >
                          📚 تفسیر
                        </button>

                        {/* دکمه پخش صوت */}
                        <button 
                          className={`play-ayah-btn ${isCurrent && isPlaying ? 'playing' : ''}`} 
                          onClick={() => playAyah(index)}
                        >
                          {isCurrent && isPlaying ? '🔊 در حال پخش' : '▶ پخش صوت'}
                        </button>
                      </div>
                    </div>

                    {/* متن عربی با اعراب و علامت‌های تجویدی */}
                    <p className="arabic-text">{ayah.text}</p>
                    <p className="translation-text">{ayah.faText}</p>

                    {/* نمایش یادداشت ثبت‌شده روی آیه */}
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

      {/* مودال افزودن / ویرایش یادداشت */}
      {editingNoteAyah !== null && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3>📝 ثبت یادداشت روی آیه</h3>
            <textarea
              rows="4"
              value={tempNoteText}
              onChange={(e) => setTempNoteText(e.target.value)}
              placeholder="نکات تجویدی، برداشت یا یادداشت شخصی خود را اینجا بنویسید..."
              className="note-textarea"
            />
            <div className="modal-actions">
              <button onClick={() => handleSaveNote(editingNoteAyah)} className="save-btn">ذخیره یادداشت</button>
              <button onClick={() => setEditingNoteAyah(null)} className="cancel-btn">انصراف</button>
            </div>
          </div>
        </div>
      )}

      {/* مودال نمایش تفسیر آیه */}
      {activeTafsir && (
        <div className="modal-overlay">
          <div className="modal-content tafsir-modal">
            <h3>📚 تفسیر آیه {activeTafsir.ayahInSurah} (تفسیر نمونه)</h3>
            <div className="tafsir-body">
              {tafsirLoading ? (
                <p className="loading">در حال بارگذاری متن تفسیر...</p>
              ) : (
                <p className="tafsir-text">{activeTafsir.text}</p>
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