import { useState, useEffect, useRef } from 'react';
import './App.css';

function App() {
  const [surahs, setSurahs] = useState([]);
  const [selectedSurah, setSelectedSurah] = useState(null);
  const [ayahs, setAyahs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  // وضعیت‌های پخش پیوسته و خودکار
  const [currentAyahIndex, setCurrentAyahIndex] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef(null);

  useEffect(() => {
    fetch('https://api.alquran.cloud/v1/surah')
      .then((res) => res.json())
      .then((data) => setSurahs(data.data))
      .catch((err) => console.error('خطا در دریافت لیست سوره‌ها:', err));
  }, []);

  const handleSelectSurah = (surahNumber) => {
    setLoading(true);
    setCurrentAyahIndex(null);
    setIsPlaying(false);
    fetch(`https://api.alquran.cloud/v1/surah/${surahNumber}/ar.alafasy`)
      .then((res) => res.json())
      .then((data) => {
        setSelectedSurah(data.data);
        setAyahs(data.data.ayahs);
        setLoading(false);
      })
      .catch((err) => {
        console.error('خطا در دریافت آیات:', err);
        setLoading(false);
      });
  };

  // پخش یک آیه خاص
  const playAyah = (index) => {
    setCurrentAyahIndex(index);
    setIsPlaying(true);
  };

  // با تمام شدن آیه، آیه بعدی خودکار پخش می‌شود
  const handleAudioEnded = () => {
    if (currentAyahIndex !== null && currentAyahIndex < ayahs.length - 1) {
      setCurrentAyahIndex((prevIndex) => prevIndex + 1);
    } else {
      setIsPlaying(false);
      setCurrentAyahIndex(null);
    }
  };

  // اجرای پخش پس از تغییر آیه فعال
  useEffect(() => {
    if (audioRef.current && currentAyahIndex !== null) {
      audioRef.current.play().catch((err) => console.error('خطا در پخش صوت:', err));
    }
  }, [currentAyahIndex]);

  // کنترل دکمه پخش/توقف کل سوره
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

  const filteredSurahs = surahs.filter((surah) =>
    surah.name.includes(searchQuery) ||
    surah.englishName.toLowerCase().includes(searchQuery.toLowerCase()) ||
    surah.number.toString() === searchQuery
  );

  return (
    <div className="app-container" dir="rtl">
      <header className="header">
        <h1>📖 قرآن آنلاین PWA</h1>
        {selectedSurah && (
          <button 
            className="back-btn" 
            onClick={() => { 
              setSelectedSurah(null); 
              setIsPlaying(false); 
              setCurrentAyahIndex(null); 
            }}
          >
            ← بازگشت به لیست سوره‌ها
          </button>
        )}
      </header>

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
            <p className="meta-info">
              {selectedSurah.englishName} | {selectedSurah.revelationType === 'Meccan' ? 'مکی' : 'مدنی'} | {selectedSurah.numberOfAyahs} آیه
            </p>

            <div className="player-controls">
              <button className="play-all-btn" onClick={togglePlayPause}>
                {isPlaying ? '⏸ توقف پخش' : '▶ پخش پیوسته سوره'}
              </button>
            </div>
          </div>

          {/* تگ صوتی اصلی برای مدیریت پخش پیوسته */}
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
            <div className="loading">در حال دریافت آیات...</div>
          ) : (
            <div className="ayahs-list">
              {ayahs.map((ayah, index) => {
                const isCurrent = currentAyahIndex === index;
                return (
                  <div key={ayah.number} className={`ayah-card ${isCurrent ? 'active-ayah' : ''}`}>
                    <div className="ayah-top">
                      <span className="ayah-badge">آیه {ayah.numberInSurah}</span>
                      <button 
                        className={`play-ayah-btn ${isCurrent && isPlaying ? 'playing' : ''}`} 
                        onClick={() => playAyah(index)}
                      >
                        {isCurrent && isPlaying ? '🔊 در حال پخش...' : '▶ پخش این آیه'}
                      </button>
                    </div>
                    <p className="arabic-text">{ayah.text}</p>
                  </div>
                );
              })}
            </div>
          )}
        </main>
      )}
    </div>
  );
}

export default App;